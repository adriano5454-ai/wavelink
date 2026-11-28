# Fleet basemap

The map of manually reported positions uses a locally bundled Natural Earth 5.1.2 land layer. The browser does not contact a tile service to display it. The world land geometry is 1:50m, generalized for a small browser payload; when zoomed into the Rio coast the app layers in a clipped 1:10m coastline. The Natural Earth source files and their SHA-256 digests are recorded in deploy/fleet_map_land.json. Source: https://github.com/nvkelso/natural-earth-vector/tree/v5.1.2/geojson. Public-domain terms: https://www.naturalearthdata.com/about/terms-of-use/.

Positions are the last manually reported values, not AIS or an electronic navigational chart. Demo positions off Rio de Janeiro, Cabo Frio and Macae are fictional and are created only in isolated public Demo sessions. Private workspace records are unchanged. Natural Earth is the in-app basemap. OpenStreetMap is an explicit per-position external link that sends only that selected location to the provider.
