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
