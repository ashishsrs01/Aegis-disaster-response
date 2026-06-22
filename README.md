# Aegis Disaster Response System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aegis-disaster-response-ka9chjfkrlwwdxgvbzwappr.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)

An interactive **disaster response simulator** built as a first-year B.Sc. project. It models a city as a graph, finds shortest ambulance routes with **A\*** search, assigns ambulances to victims using the **Hungarian algorithm**, and applies a simple **START triage** rules engine.

**[Live demo on Streamlit Cloud](https://aegis-disaster-response-ka9chjfkrlwwdxgvbzwappr.streamlit.app)**

---

## Features

| Module | What it does |
|--------|----------------|
| **City graph** | Synthetic grid or real streets from [OpenStreetMap](https://www.openstreetmap.org/) via OSMnx |
| **Pathfinding** | A* search with road weights (travel time) |
| **Dispatch** | SciPy `linear_sum_assignment` — optimal ambulance–victim pairing |
| **Triage** | START-style priority tags (RED / YELLOW / GREEN / BLACK) from victim vitals |
| **Hazard model** | Bayesian network (pgmpy) for flood probability from sensor data |
| **Dashboard** | Streamlit web app with map visualization |

---

## Quick start

### Requirements

- Python 3.10 or newer
- Internet connection (only when loading real maps)

### Install

```bash
git clone https://github.com/ashishsrs01/Aegis-disaster-response.git
cd Aegis-disaster-response
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

### Run tests

```bash
pytest tests/
```

---

## Using the dashboard

1. **Synthetic grid (default)** — adjust grid size in the sidebar and click **Run Simulation**.
2. **Real map** — enable *Use Real Map (OpenStreetMap)*, pick a preset city or choose **Custom**.
3. **Custom location** — enter a specific address with city and country, for example:
   - `Connaught Place, New Delhi, India`
   - `Marine Drive, Mumbai, India`
   - `Times Square, New York, USA`

Custom places are downloaded as a **2 km radius** around the geocoded address (needed when the place is a point, not a city boundary).

> **Note:** The first download for a new area can take 10–30 seconds depending on your connection.

---

## Project structure

```
Aegis-disaster-response/
├── app.py                  # Streamlit dashboard (main entry point)
├── requirements.txt
├── src/
│   ├── core/               # CityGraph, Victim models
│   ├── navigation/         # A* pathfinder
│   ├── optimization/       # Hungarian dispatch optimizer
│   ├── reasoning/          # START triage engine
│   └── perception/         # Bayesian hazard tracker
├── data/
│   ├── osm/                # Cached map files
│   └── scenarios/          # Sample scenario JSON
├── tests/                  # Unit and integration tests
├── scripts/
│   └── download_osm.py     # Pre-download maps for offline use
└── docs/adr/               # Architecture decision records
```

---

## How the AI pipeline works

```
City map (grid or OSM)
        │
        ▼
   A* pathfinding  ──►  cost matrix (each ambulance × each victim)
        │
        ▼
 Hungarian algorithm  ──►  optimal assignments
        │
        ▼
  Map + dispatch results (+ triage tags)
```

**Hazard handling (backend):** road weights can be increased when a flood probability is high, forcing A* to reroute. The Bayesian module in `src/perception/hazard_tracker.py` estimates flood probability from drone sensor readings.

---

## Pre-download maps (optional)

To save a map for offline use:

```bash
python scripts/download_osm.py --location "Piedmont, California, USA" --output "data/osm/piedmont.graphml"
```

Load it in code with `CityGraph(filepath="data/osm/piedmont.graphml")`.

---

## Tech stack

- [Streamlit](https://streamlit.io/) — web UI
- [NetworkX](https://networkx.org/) — graph data structure
- [OSMnx](https://osmnx.readthedocs.io/) — OpenStreetMap street networks
- [SciPy](https://scipy.org/) — linear sum assignment (Hungarian algorithm)
- [pgmpy](https://pgmpy.org/) — Bayesian networks
- [Matplotlib](https://matplotlib.org/) — map plotting

---

## Author

**Ashish Sharma** — B.Sc. Applied AI and Data science (Year 1)  
GitHub: [@ashishsrs01](https://github.com/ashishsrs01)

---

## License

This project was created for academic purposes. Feel free to use and modify it for learning.
