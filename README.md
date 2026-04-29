# 🚑 Aegis Disaster Response AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aegis-disaster-response-ka9chjfkrlwwdxgvbzwappr.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-lightgrey.svg)
![NetworkX](https://img.shields.io/badge/NetworkX-Graph-green.svg)
![pgmpy](https://img.shields.io/badge/pgmpy-Probabilistic_Reasoning-orange.svg)

An intelligent, multi-agent fleet optimization and pathfinding system designed to simulate emergency response logistics in dynamic, uncertain environments. 

**[🔴 Try the Live Interactive Dashboard Here](https://aegis-disaster-response-ka9chjfkrlwwdxgvbzwappr.streamlit.app)**

## 🧠 Core AI Architecture

Unlike standard routing applications, Aegis handles the fog-of-war inherent in disaster scenarios. It bridges several sub-fields of Artificial Intelligence to create a robust, context-aware dispatch system:

### 1. Search & Navigation (Dynamic Pathfinding)
* Uses the **A* (A-Star) Search Algorithm** over a custom `NetworkX` graph representation of a city. 
* Implements dynamic graph weighting where road traversal costs are updated in real-time based on simulated traffic and environmental hazards, triggering automatic re-planning when paths become sub-optimal.

### 2. Perception Under Uncertainty (Bayesian Inference)
* Agents do not blindly trust sensor data. The system utilizes **Bayesian Networks** (`pgmpy`) to evaluate noisy drone/sensor feeds.
* It calculates the true posterior probability of an environmental hazard (e.g., a flooded route) by fusing contextual priors (like weather forecasts) with the known false-positive/false-negative rates of the sensors.

### 3. Knowledge Representation (Logic-Based Triage)
* Employs a **Propositional Logic Engine** to implement the real-world S.T.A.R.T. (Simple Triage and Rapid Treatment) medical protocol.
* The system dynamically categorizes victims into priority tiers (RED, YELLOW, GREEN, BLACK) based on an evaluation of their live vital signs, separating the knowledge base from the inference execution.

### 4. Multi-Agent Optimization (Operations Research)
* Abandons greedy, localized agent behavior in favor of global optimization. 
* The system dynamically generates an A* cost matrix representing the exact travel time from *every* ambulance to *every* victim. This matrix is fed into **SciPy's linear sum assignment solver (Hungarian Algorithm)** to calculate the deployment strategy that minimizes the total aggregate fleet action time.

### project Structure
```
aegis-disaster-response/
├── src/
│   ├── core/           # Graph environment setup and Victim/Agent entity models
│   ├── navigation/     # A* Search and pathfinding heuristics
│   ├── perception/     # Bayesian Networks and hazard trackers
│   ├── reasoning/      # Triage engine and propositional logic
│   └── optimization/   # Multi-agent SciPy dispatchers
├── app.py              # Streamlit frontend application
└── requirements.txt    # Pinned dependencies for cloud deployment
```

### Future development
```
├── data/                       # OpenStreetMap (OSM) graphs and synthetic scenario configs
├── tests/                      # Automated unit/integration tests (pytest)
├── docs/                       # Architecture Decision Records (ADRs)
└── .github/workflows/          # CI/CD pipeline automation
```

## 🚀 Installation & Local Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ashishsrs01/Aegis-disaster-response.git]
   cd aegis-disaster-response
