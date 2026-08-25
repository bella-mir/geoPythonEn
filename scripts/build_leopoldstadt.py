"""Build the module 6 case-study datasets for Leopoldstadt (2nd district of Vienna).

Builds the four layers that notebooks/module_6/map_1.ipynb reads:

    area.geojson        district boundary                       (OpenStreetMap)
    landuse.geojson     land use polygons                       (City of Vienna)
    metro.geojson       U-Bahn stations                         (OpenStreetMap)
    isochrones.geojson  5/10/15-minute walking isochrones       (OpenRouteService),
                        each carrying the population it reaches  (WorldPop)

The OpenRouteService key is read from notebooks/module_4/.env (git-ignored).
"""

import io
import time
import warnings
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import rasterio
import pandas as pd
import requests
from rasterio.mask import mask

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "leopoldstadt"
OUT.mkdir(parents=True, exist_ok=True)

ox.settings.cache_folder = str(ROOT / "cache")

AREA_NAME = "Leopoldstadt, Vienna, Austria"
AREA_LABEL = "Leopoldstadt"
DISTRICT_CODE = "02"   # the two-digit district number the city's own layers are keyed on
RANGES = [300, 600, 900]  # 5, 10, 15 minutes


# --- 1. district boundary ----------------------------------------------------
boundary = ox.geocode_to_gdf(AREA_NAME)
area = gpd.GeoDataFrame(
    {"name": [AREA_LABEL]}, geometry=[boundary.geometry.iloc[0]], crs="EPSG:4326"
)
area.to_file(OUT / "area.geojson", driver="GeoJSON")
print(f"area.geojson       {len(area)} feature")

polygon = area.geometry.iloc[0]


# --- 2. land use -------------------------------------------------------------
# OpenStreetMap maps land use in Vienna only patchily — it covers about two thirds
# of this district, and seven polygons in eight are an individual lawn or flowerbed.
# The city's own survey (Realnutzungskartierung) is a complete partition of the
# area with a three-level classification, so we take the layer from there.
REALNUT = "https://data.wien.gv.at/daten/geo"
response = requests.get(
    REALNUT,
    params={
        "service": "WFS",
        "request": "GetFeature",
        "version": "1.1.0",
        "typeName": "ogdwien:REALNUT2024OGD",
        "srsName": "EPSG:4326",
        "outputFormat": "json",
    },
    timeout=600,
)
response.raise_for_status()

landuse = gpd.read_file(io.BytesIO(response.content))
landuse = landuse[landuse["BEZ"] == DISTRICT_CODE]           # the survey is filed by district
landuse = landuse[["LEV1", "LEV2", "LEV3", "FLAECHE", "geometry"]]
landuse = landuse.sort_values("LEV2").reset_index(drop=True)
landuse.to_file(OUT / "landuse.geojson", driver="GeoJSON")
print(f"landuse.geojson    {len(landuse)} features, "
      f"{landuse['LEV2'].nunique()} categories")


# --- 3. U-Bahn stations ------------------------------------------------------
metro = ox.features_from_polygon(polygon, tags={"station": "subway"}).reset_index()
metro = metro[metro.geometry.geom_type == "Point"]
# Praterstern carries one node per line; one point per station is enough here
metro = metro.drop_duplicates(subset="name").sort_values("name")
metro = metro[["element", "id", "name", "geometry"]].reset_index(drop=True)

# The line number is not on the OSM node, so we take it from the city's own station
# layer (data/vienna/vienna_metro.geojson, written by build_vienna_data.py), matching
# on position rather than on name: the two sources spell some stations differently —
# "Messe - Prater" in OSM against "Messe Prater" in the city register.
city = gpd.read_file(ROOT / "data" / "vienna" / "vienna_metro.geojson")[["line", "geometry"]]
utm = metro.estimate_utm_crs()
metro = (
    gpd.sjoin_nearest(metro.to_crs(utm), city.to_crs(utm), how="left")
    .drop(columns="index_right")
    .to_crs("EPSG:4326")
)
metro = metro[["element", "id", "name", "line", "geometry"]]
metro.to_file(OUT / "metro.geojson", driver="GeoJSON")
print(f"metro.geojson      {len(metro)} stations: {', '.join(metro['name'])}")


# --- 4. walking isochrones (OpenRouteService) --------------------------------
def ors_key() -> str:
    env = ROOT / "notebooks" / "module_4" / ".env"
    for line in env.read_text().splitlines():
        if line.startswith("ORS_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("ORS_API_KEY not found in notebooks/module_4/.env")


url = "https://api.openrouteservice.org/v2/isochrones/foot-walking"
headers = {"Authorization": ors_key(), "Content-Type": "application/json"}

frames = []
batch_size = 5  # the free plan accepts at most 5 locations per request

for start in range(0, len(metro), batch_size):
    batch = metro.iloc[start:start + batch_size]
    body = {
        "locations": [[p.x, p.y] for p in batch.geometry],
        "range": RANGES,
    }
    response = requests.post(url, json=body, headers=headers, timeout=120)
    if response.status_code != 200:
        raise SystemExit(f"ORS {response.status_code}: {response.text[:400]}")

    part = gpd.GeoDataFrame.from_features(response.json()["features"], crs="EPSG:4326")
    # group_index is local to each request — shift it onto the global station index
    part["station_id"] = part["group_index"].astype(int) + start
    frames.append(part)

    if start + batch_size < len(metro):
        time.sleep(3)  # stay inside the free-plan rate limit

isochrones = pd.concat(frames, ignore_index=True)
isochrones["station_name"] = isochrones["station_id"].map(metro["name"])
isochrones["group_index"] = isochrones["station_id"]
isochrones = gpd.GeoDataFrame(
    isochrones[["group_index", "value", "center", "station_id", "station_name",
                "geometry"]],
    crs="EPSG:4326",
)
# --- 5. how many people each zone reaches -----------------------------------
# The project's question is about people, not area, so each isochrone carries the
# population it covers. The zones are clipped to the district first: they spill
# well past its boundary, and uncut they would count residents of other districts.
raster = ROOT / "data" / "austria" / "austria_population.tif"

with rasterio.open(raster) as population:
    zones = (
        isochrones[["value", "geometry"]]
        .dissolve(by="value")                       # one shape per threshold
        .reset_index()
        .to_crs(population.crs)
    )
    district = polygon_gdf = area.to_crs(population.crs).geometry.iloc[0]

    def people_in(geometry):
        counts, _ = mask(population, [geometry], crop=True, filled=False)
        return round(float(counts.sum()))

    reached = {
        row["value"]: people_in(row.geometry.intersection(district))
        for _, row in zones.iterrows()
    }

isochrones["population"] = isochrones["value"].map(reached)

isochrones.to_file(OUT / "isochrones.geojson", driver="GeoJSON")
print(f"isochrones.geojson {len(isochrones)} features "
      f"({len(metro)} stations x {len(RANGES)} thresholds), "
      f"reaching {reached[max(reached)]:,} of the district's residents")
