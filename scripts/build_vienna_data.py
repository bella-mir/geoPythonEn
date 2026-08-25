"""Download the Vienna datasets the notebooks use.

Everything here comes from the City of Vienna's open data portal, served by a
single WFS endpoint, plus one population raster from WorldPop:

    data/vienna/vienna_admin.gpkg          district and census-district boundaries
    data/vienna/vienna_metro.geojson       U-Bahn stations
    data/vienna/vienna_top_locations.csv   tourist POIs, re-encoded to UTF-8
    data/vienna/vienna_buildings.csv       buildings with year of construction
    data/vienna/vienna_playgrounds_shp/    playgrounds, as a shapefile
    data/austria/austria_population.tif    population raster (WorldPop)

Run it from the repository root:  python scripts/build_vienna_data.py
"""

import io
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
VIENNA = ROOT / "data" / "vienna"
AUSTRIA = ROOT / "data" / "austria"
VIENNA.mkdir(parents=True, exist_ok=True)
AUSTRIA.mkdir(parents=True, exist_ok=True)

WFS = "https://data.wien.gv.at/daten/geo"


def wfs(layer: str, fmt: str = "json") -> gpd.GeoDataFrame | pd.DataFrame:
    """Fetch one layer from the City of Vienna WFS in EPSG:4326."""
    params = {
        "service": "WFS",
        "request": "GetFeature",
        "version": "1.1.0",
        "typeName": f"ogdwien:{layer}",
        "srsName": "EPSG:4326",
        "outputFormat": fmt,
    }
    response = requests.get(WFS, params=params, timeout=600)
    response.raise_for_status()
    if fmt == "csv":
        return pd.read_csv(io.BytesIO(response.content), encoding="utf-8")
    return gpd.read_file(io.BytesIO(response.content))


# --- districts and census districts -----------------------------------------
districts = wfs("BEZIRKSGRENZEOGD")
districts = districts.rename(columns={"NAMEK": "NAME"})
districts = districts[["NAME", "BEZ", "BEZNR", "FLAECHE", "geometry"]]
districts = districts.sort_values("BEZNR").reset_index(drop=True)

zaehlbezirke = wfs("ZAEHLBEZIRKOGD")
zaehlbezirke = zaehlbezirke[["ZBEZ", "BEZ", "BEZNR", "ZBEZNR", "FLAECHE", "geometry"]]
zaehlbezirke = zaehlbezirke.sort_values("ZBEZ").reset_index(drop=True)

admin = VIENNA / "vienna_admin.gpkg"
admin.unlink(missing_ok=True)
districts.to_file(admin, layer="district", driver="GPKG")
zaehlbezirke.to_file(admin, layer="zaehlbezirk", driver="GPKG")
print(f"vienna_admin.gpkg       district={len(districts)}, "
      f"zaehlbezirk={len(zaehlbezirke)}")


# --- U-Bahn stations ---------------------------------------------------------
metro = wfs("UBAHNHALTOGD")
metro = metro.rename(columns={
    "HTXT": "name",
    "LINFO": "line",
    "EROEFFNUNG_JAHR": "opened_year",
    "EROEFFNUNG_MONAT": "opened_month",
})
metro = metro[["name", "line", "opened_year", "opened_month", "geometry"]]
metro = metro.sort_values(["line", "name"]).reset_index(drop=True)
metro.to_file(VIENNA / "vienna_metro.geojson", driver="GeoJSON")
print(f"vienna_metro.geojson    {len(metro)} stations on "
      f"{metro['line'].nunique()} lines")


# --- tourist POIs ------------------------------------------------------------
# The published file is semicolon-separated, cp1252-encoded, and writes decimals
# with a comma. We keep the layout but save it as UTF-8 so it reads anywhere.
raw = requests.get("https://data.wien.gv.at/csv/top-locations-wien.csv", timeout=120)
raw.raise_for_status()
locations = pd.read_csv(
    io.BytesIO(raw.content), sep=";", decimal=",", encoding="cp1252"
)
locations = locations[[
    "title", "category", "Beschreibung", "address", "zip", "city",
    "geo_latitude", "geo_longitude", "tel_1", "email", "web_url",
]]
locations.to_csv(
    VIENNA / "vienna_top_locations.csv", sep=";", decimal=",",
    index=False, encoding="utf-8",
)
print(f"vienna_top_locations.csv {len(locations)} POIs, "
      f"{locations['category'].nunique()} categories")


# --- buildings ---------------------------------------------------------------
# Point geometry arrives as a WKT string in the SHAPE column, which is what the
# notebooks turn back into geometry.
buildings = wfs("GEBAEUDEINFOOGD", fmt="csv")
buildings = buildings.rename(columns={"STRNAML": "street", "VONN": "house_number"})
buildings = buildings[[
    "street", "house_number", "BEZ", "HA_NAME", "BAUJAHR", "ARCHITEKT",
    "GESCH_ANZ", "L_NUTZUNG", "L_BAUTYP", "L_BAUJ", "SHAPE",
]]
buildings.to_csv(VIENNA / "vienna_buildings.csv", index=False, encoding="utf-8")
print(f"vienna_buildings.csv    {len(buildings)} buildings, "
      f"BAUJAHR {buildings['BAUJAHR'].min():.0f}-{buildings['BAUJAHR'].max():.0f}")


# --- playgrounds (as a shapefile) -------------------------------------------
playgrounds = wfs("SPIELPLATZPUNKTOGD")
playgrounds = playgrounds.rename(columns={
    "ANL_NAME": "name",
    "BEZIRK": "district",
    "SPIELPLATZ_DETAIL": "equipment",
    "TYP_DETAIL": "type",
})
playgrounds = playgrounds[["name", "district", "equipment", "type", "geometry"]]
shp_dir = VIENNA / "vienna_playgrounds_shp"
shp_dir.mkdir(exist_ok=True)
playgrounds.to_file(shp_dir / "vienna_playgrounds.shp", encoding="utf-8")
print(f"vienna_playgrounds_shp  {len(playgrounds)} playgrounds")


# --- population raster -------------------------------------------------------
raster_url = (
    "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A"
    "/2025/AUT/v1/100m/constrained/aut_pop_2025_CN_100m_R2025A_v1.tif"
)
target = AUSTRIA / "austria_population.tif"
with requests.get(raster_url, stream=True, timeout=600) as response:
    response.raise_for_status()
    with open(target, "wb") as handle:
        for chunk in response.iter_content(chunk_size=1 << 20):
            handle.write(chunk)
print(f"austria_population.tif  {target.stat().st_size / 1e6:.1f} MB")
