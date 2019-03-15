# geoSubscription-Server
### About
The geoSubscription-Server is a python based web-service that can take in a variety of geogrpahic data. Each dataset is imported into a postgreSQL table. These datasets can then be filtered by eitheir attirbutes or geographies by the user. After the data is imported into a table we can perform a variety of different analytics on each table that are listed below. In return they will get a variety of tables generated inside postgreSQL.

### Tool Services
Inputs
* ArcGIS
  * FeatureService
  * MapService
* Web
  * JSON
  * GeoJSON
* Portal
    * Your Datasets

Input Filters
* Column
* Geographic

Analytics
* Buffer
* Count Within (Your datasets, pre-defined)
* Intersect (Your datasets, pre-defined)
* Select Within (Your datasets, pre-defined)
* Bounding Box
* Concave Hull
* Dissolve
* Dissolve By Attribute
* Concave Hull
* Find Center
* Center of Each Polygon
* Point to Point Distance
* Select outside
* Column Calculations
* Join to Table (Your datasets, pre-defined)
* Add XY Values
* Union
* Merge Tables
