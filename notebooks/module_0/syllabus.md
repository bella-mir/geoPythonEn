# Course Modules

The course is organised into **six thematic modules**, each containing several sections.

Each module comes with a practice assignment – a stage of a larger project in which you assess the everyday accessibility of a city of your choice through the lens of the 15-minute city concept.

## [Module 1. Spatial Data](../module_1/spData_0.ipynb)

- spatial data models: vector and raster
- spatial data formats
- structure and properties of `GeoDataFrame`
- reading and writing data
- retrieving data from OpenStreetMap

Libraries: `pandas`, `geopandas`, `shapely`, `osmnx`, `numpy`, `rasterio`

_Interactive previews via `.explore()` also need `folium` and `mapclassify`._

## [Module 2. Projections and Coordinate Reference Systems (CRS)](../module_2/projections_0.ipynb)

- theoretical foundations of map projections
- Universal Transverse Mercator (UTM)
- geographic and projected coordinate systems
- EPSG codes
- reprojecting spatial data
- measuring distances and areas

Libraries: `geopandas`, `pandas`, `osmnx`

_Coordinate systems are handled by `pyproj`, which GeoPandas uses under the hood._

## [Module 3. Core Geoprocessing Tools](../module_3/geoprocessing_0.ipynb)

- basic geometry operations: buffer, dissolve, clip
- spatial predicates
- spatial joins: by containment and to the nearest feature
- aggregating point data by polygon (feature counts and attribute statistics)

Libraries: `geopandas`, `pandas`, `shapely`, `osmnx`, `matplotlib`

## [Module 4. Fundamentals of Network Analysis](../module_4/networkAnalysis_0.ipynb)

- representing a transport network as a graph
- retrieving street networks from OpenStreetMap
- computing centrality metrics
- shortest paths and distance matrices
- isochrones
- working with external routing APIs: OSRM, OpenRouteService, GraphHopper

Libraries: `osmnx`, `networkx`, `geopandas`, `pandas`, `shapely`, `matplotlib`, `requests`, `polyline`

## [Module 5. Raster Analysis](../module_5/rasters_0.ipynb)

- the raster spatial data model
- raster data structure (cells, resolution, extent)
- reading raster data
- clipping and reprojecting rasters
- zonal statistics

Libraries: `rasterio`, `rasterstats`, `geopandas`, `numpy`, `matplotlib`, `osmnx`

## [Module 6. Interactive Visualisation](../module_6/map_0.ipynb)

- interactive maps with Folium: layers, styles, tooltips, legend
- map controls
- publishing to GitHub Pages

Libraries: `folium`, `geopandas`

## Data

All datasets used in the notebooks live in a single `data/` folder at the root of the repository. Notebooks read them through a relative path:

```python
gdf = gpd.read_file("../../data/vienna/vienna_metro.geojson")
```

Almost everything comes from the City of Vienna's open data portal, [data.wien.gv.at](https://data.wien.gv.at/), under a **CC BY 4.0** licence that asks for the attribution _Datenquelle: Stadt Wien – data.wien.gv.at_. The `ogdwien:` names in the tables below are its WFS layer names, and [`scripts/build_vienna_data.py`](https://github.com/bella-mir/geoPythonEn/blob/main/scripts/build_vienna_data.py) is the script that downloads every file.

### `data/vienna/` – Vienna (modules 1–3)

| File | Content | Source |
| --- | --- | --- |
| `vienna_admin.gpkg` | boundaries of the 23 districts and the 250 census districts (layers `district` and `zaehlbezirk`) | [Bezirksgrenzen Wien](https://www.data.gv.at/katalog/dataset/stadt-wien_bezirksgrenzenwien) (`ogdwien:BEZIRKSGRENZEOGD`) and Zählbezirke Wien (`ogdwien:ZAEHLBEZIRKOGD`) |
| `vienna_metro.geojson` | U-Bahn stations, with line number and year of opening | U-Bahnhaltestellen Wien (`ogdwien:UBAHNHALTOGD`) |
| `vienna_top_locations.csv` | ~135 well-known places to visit – museums, cafés, concert halls, shops – with coordinates in `geo_latitude` and `geo_longitude` | [Top Locations Wien](https://www.data.gv.at/katalog/dataset/45d684ca-6ad7-4c5e-a721-64aa31795824) |
| `vienna_buildings.csv` | the city's building register: year of construction, storeys, type of use, architect; geometry as WKT text in the `SHAPE` column | Gebäudeinfo Wien (`ogdwien:GEBAEUDEINFOOGD`) |
| `vienna_playgrounds_shp/` | public playgrounds, as a shapefile | Spielplätze Wien (`ogdwien:SPIELPLATZPUNKTOGD`) |

The published files use European conventions that Python does not assume by default: `vienna_top_locations.csv` is semicolon-separated, with a comma as the decimal mark.

### `data/austria/` – Austria (module 5)

| File | Content | Source |
| --- | --- | --- |
| `austria_population.tif` | population raster covering Austria; each pixel holds a population count | [WorldPop](https://hub.worldpop.org), Global 2000–2020 Constrained, Austria, 2020, UN-adjusted |
| `vienna_cropped_population.tif` | the same raster clipped to the city of Vienna | generated in [Raster Data Format](../module_5/rasters_1.ipynb) |
| `vienna_cropped_population_utm.tif` | the clipped raster reprojected into UTM | generated in [Raster Data Format](../module_5/rasters_1.ipynb) |

### `data/leopoldstadt/` – Leopoldstadt (module 6)

A small case study prepared in advance, so that the final module is about mapping rather than data collection. Leopoldstadt is the second district of Vienna, an island between the Danube and the Danube Canal.

| File | Content | Source |
| --- | --- | --- |
| `area.geojson` | boundary of the district | OpenStreetMap |
| `landuse.geojson` | land use polygons, classified at three levels (`LEV1`/`LEV2`/`LEV3`) | Realnutzungskartierung Wien 2024 (`ogdwien:REALNUT2024OGD`) |
| `metro.geojson` | U-Bahn stations | OpenStreetMap |
| `isochrones.geojson` | walking isochrones of 5, 10 and 15 minutes from the stations, each carrying the number of residents it reaches | zones from [OpenRouteService](https://openrouteservice.org), population from WorldPop |

The land use layer is the one file here that is not from OpenStreetMap – in Vienna the OSM `landuse` tag covers only about two thirds of the district.

These four files are rebuilt by [`scripts/build_leopoldstadt.py`](https://github.com/bella-mir/geoPythonEn/blob/main/scripts/build_leopoldstadt.py); changing one constant in it produces the same set for any other district.

### Cache

Data downloaded from OpenStreetMap is cached in a `cache/` folder at the root of the repository (git-ignored): the notebooks point `ox.settings.cache_folder` at it, so repeated queries are served from disk instead of hitting the OSM servers again.
