# ADR 0001: Use NetworkX for Core City Graph Representation

## Status
Accepted

## Context
The Aegis AI system needs a way to mathematically represent the roads and intersections of a city to perform pathfinding algorithms (like A*) and simulate disaster hazards. We need a data structure that is fast, flexible, and easy for beginners to understand.

## Decision
We decided to use the `networkx` Python library as the core graph representation for the `CityGraph` class.

## Consequences
### Positive
- `networkx` is the industry standard for graph theory in Python.
- It is highly readable and beginner-friendly.
- It integrates seamlessly with `matplotlib` for visualization.
- It supports assigning metadata (like travel time or hazard probabilities) directly to edges (roads).

### Negative
- It is implemented in pure Python, making it slower than C++ backed libraries (like `igraph`) for extremely massive graphs (e.g., routing across an entire country). However, for city-scale disaster response simulations, the performance is well within acceptable limits.
