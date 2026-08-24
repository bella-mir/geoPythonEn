# Course Modules

The course is organised into **six thematic modules**, each containing several sections.

Each module comes with a practice assignment — a stage of a larger project in which you assess the everyday accessibility of a city of your choice through the lens of the 15-minute city concept.

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
- spatial joins
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

All datasets used in the notebooks live in a single `data/` folder at the root of the repository, so no file is stored twice. Notebooks read them through a relative path:

```python
gdf = gpd.read_file("../../data/spb/spb_metro.geojson")
```

### `data/spb/` — Saint Petersburg (modules 1–3)

| File | Content | Source |
| --- | --- | --- |
| `spb_admin.gpkg` | boundaries of districts and municipal units (layers `district` and `okrug`) | course materials for "Methods of Spatial Analysis", HSE University (R. Goncharov) |
| `spb_metro.geojson` | metro stations, 2023 | [Saint Petersburg Open Data Portal](https://data.gov.spb.ru/) |
| `spb_theaters.csv` | theatres, with coordinates in the `latitude` and `longitude` columns | [Saint Petersburg Open Data Portal](https://data.gov.spb.ru/) |
| `spb_mkd.csv` | apartment buildings, 2020 | [Saint Petersburg Open Data Portal](https://data.gov.spb.ru/) |
| `spb_dtp_shp/` | road accidents, January 2023 (shapefile) | [Road Accident Map](https://dtp-stat.ru) |

### `data/tula/` — Tula Oblast (module 5)

| File | Content | Source |
| --- | --- | --- |
| `tula_region_population.tif` | population raster clipped to the Tula Oblast; each pixel holds a population count | [WorldPop](https://hub.worldpop.org), Global 2000–2020 Constrained, Russia, 2020 |
| `tula_cropped_population.tif` | the same raster clipped to the city of Tula | generated in [Raster Data Format](../module_5/rasters_1.ipynb) |
| `tula_cropped_population_utm.tif` | the clipped raster reprojected into UTM | generated in [Raster Data Format](../module_5/rasters_1.ipynb) |

### `data/vasilyevsky/` — Vasilyevsky Island (module 6)

A small case study prepared in advance, so that the final module is about mapping rather than data collection.

| File | Content | Source |
| --- | --- | --- |
| `area.geojson` | boundary of the Vasileostrovsky District | OpenStreetMap |
| `landuse.geojson` | land use polygons | OpenStreetMap |
| `metro.geojson` | metro stations | OpenStreetMap |
| `isochrones.geojson` | walking isochrones of 5, 10 and 15 minutes from the stations | built with [OpenRouteService](https://openrouteservice.org) |

### Images and cache

Illustrations used in the text are kept next to the notebooks that reference them, in `notebooks/module_*/images/`.

Data downloaded from OpenStreetMap is cached in a `cache/` folder at the root of the repository (git-ignored): the notebooks point `ox.settings.cache_folder` at it, so repeated queries are served from disk instead of hitting the OSM servers again.
