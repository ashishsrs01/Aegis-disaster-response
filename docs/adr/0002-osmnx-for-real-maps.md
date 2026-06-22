# ADR 0002: Use OSMnx for Real-World OpenStreetMap Integration

## Status
Accepted

## Context
Originally, the simulator used synthetic grid-based graphs. To make the tool useful for real-world scenarios, we needed a way to import actual city streets and road networks.

## Decision
We decided to use the `osmnx` library to fetch and process OpenStreetMap (OSM) data.

## Consequences
### Positive
- `osmnx` directly builds `networkx` graphs, meaning it drops perfectly into our existing `CityGraph` without rewriting the core pathfinding logic.
- It automatically handles complex geospatial queries (e.g., filtering out walking paths to only keep drivable roads).
- It allows users to simply type a neighborhood name (like "Manhattan, New York") to fetch real maps instantly.

### Negative
- `osmnx` requires internet access to fetch new areas via the Overpass API. (Mitigated by providing an offline `.graphml` download script).
- Real-world graphs are messy (one-way streets, complex intersections) compared to clean synthetic grids, which can sometimes result in ambulances getting stuck if paths are entirely blocked by hazards.
