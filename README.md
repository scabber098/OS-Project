<div align="center">

# 👻 GhostSched v2
### Neural CPU Scheduler — Real-Time System Monitor

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![psutil](https://img.shields.io/badge/psutil-live_data-00C896?style=for-the-badge)](https://psutil.readthedocs.io)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4.1-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **A real-time OS process monitor and CPU scheduling visualizer** — streams live system data, simulates scheduling algorithms, and visualizes performance metrics with a dark cyberpunk UI.

---

![GhostSched Dashboard](https://placehold.co/900x420/02030a/00f5ff?text=GhostSched+v2+%E2%80%94+Real-Time+Monitor&font=monospace)

</div>

---

## 📋 Table of Contents

- [What Is GhostSched?](#-what-is-ghostsched)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Dashboard Tabs](#-dashboard-tabs)
- [Scheduling Algorithms](#-scheduling-algorithms)
- [Key Concepts](#-key-concepts)
- [How It Works](#️-how-it-works)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)

---

## 🧠 What Is GhostSched?

**GhostSched** is an educational + practical tool built to:

1. **Monitor your real system** — streams live CPU, memory, and process data from your machine every 1–2 seconds using `psutil`.
2. **Visualize CPU scheduling algorithms** — simulates and compares Round Robin, SJF, Priority, and the custom GhostSched algorithm side-by-side.
3. **Predict future workloads** — uses an **Exponential Moving Average (EMA)** predictor to anticipate CPU burst spikes before they happen.
4. **Teach OS concepts** — includes a Research tab with real-world connections to embedded systems, cloud computing, and modern CPU architecture.

> Inspired by concepts from Linux CFS, big.LITTLE ARM architecture, and Google Borg.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔴 **Live Process Table** | Real process list sorted by CPU usage, updated every second |
| 📊 **CPU Core Monitor** | Per-core load, frequency (MHz), voltage, and power (mW) |
| 🧮 **Algorithm Simulator** | Simulates GhostSched, Round Robin, SJF, and Priority scheduling |
| ⚡ **Energy Dashboard** | Tracks cumulative energy usage and compares it to Round Robin |
| 🌡️ **Thermal Monitor** | Color-coded core temperature map (cool → warm → hot) |
| 📈 **Gantt Chart** | Scrollable real-time Gantt chart of process scheduling |
| 🔮 **EMA Predictor** | Predicts next CPU burst — pre-scales cores before spikes |
| 📡 **Radar Comparison** | Multi-metric radar chart comparing all scheduling algorithms |
| 📚 **Research Panel** | Real-world applications: mobile SoCs, IoT, cloud, HPC |
| 🎨 **Cyberpunk UI** | Animated scanlines, glow effects, glassmorphism cards |

---

## 🛠 Tech Stack

**Backend**
- **Python 3.8+** — core language
- **Flask** — lightweight REST API server
- **psutil** — cross-platform process & system data
- **flask-cors** — enables frontend on any port/origin

**Frontend**
- **Vanilla HTML/CSS/JS** — zero framework dependencies
- **Chart.js 4.4.1** — all charts (line, bar, radar, doughnut)
- **Google Fonts** — Orbitron, Share Tech Mono, Rajdhani
- **CSS Custom Properties** — fully themed cyberpunk color system

---

## 📁 Project Structure

```
ghostsched/
│
├── app.py                  # Flask backend — REST API server
└── index_realtime.html     # Frontend — single-file dashboard
```

> The entire frontend is a single self-contained HTML file. No build step, no npm, no frameworks.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ghostsched.git
cd ghostsched
```

### 2. Install Dependencies

```bash
pip install flask flask-cors psutil
```

### 3. Start the Backend

```bash
python app.py
```

You should see:

```
====================================================
  GhostSched Real-Time Monitor  —  Backend
====================================================
  Processes  →  http://127.0.0.1:5000/processes
  System     →  http://127.0.0.1:5000/system
  Health     →  http://127.0.0.1:5000/health
====================================================
```

### 4. Open the Frontend

Open `index_realtime.html` directly in your browser:

```bash
# macOS
open index_realtime.html

# Linux
xdg-open index_realtime.html

# Windows
start index_realtime.html
```

> The frontend auto-polls `http://127.0.0.1:5000` every ~1 second. Make sure the backend is running first.

---

## 🌐 API Endpoints

### `GET /processes`
Returns the full live process list plus overall system stats.

```json
{
  "timestamp": 1713000000.0,
  "total": 142,
  "processes": [
    {
      "pid": 1234,
      "name": "chrome",
      "cpu": 12.4,
      "memory": 320.5,
      "status": "running",
      "threads": 18
    }
  ],
  "system": {
    "cpu_total": 34.2,
    "cores": [
      { "id": 0, "load": 42.1, "freq": 3600, "maxFreq": 4800, "type": "P-CORE" }
    ],
    "mem_percent": 61.0,
    "mem_used_mb": 9830.4,
    "mem_total_mb": 16384.0,
    "sched_mode": "BALANCED",
    "fairness": 0.9312,
    "active_procs": 8
  }
}
```

### `GET /system`
Lightweight endpoint — CPU and memory only (no process list).

### `GET /health`
Health check. Returns `{ "status": "ok", "ts": <timestamp> }`.

---

## 🗂 Dashboard Tabs

| Tab | What You See |
|---|---|
| **◈ DASHBOARD** | Key stats (CPU, memory, processes, fairness index), CPU history chart, performance rings |
| **◫ CPU CORES** | Per-core load grid, temperature heatmap, frequency/voltage/power charts |
| **⊞ SCHEDULER** | Current scheduling mode (IDLE/BALANCED/LOADED/SATURATED), GhostSched algorithm breakdown |
| **⊟ COMPARISON** | Live table comparing GhostSched vs Round Robin vs SJF vs Priority, radar chart |
| **⚡ ENERGY** | Cumulative energy savings vs Round Robin, core temperature over time |
| **▤ GANTT** | Scrollable real-time Gantt chart of scheduled processes |
| **◉ PREDICTOR** | EMA workload predictor — actual vs predicted CPU burst, spike detection |
| **◎ RESEARCH** | Real-world applications: mobile SoCs, IoT, cloud, HPC, and algorithm limitations |

---

## ⚙️ Scheduling Algorithms

GhostSched simulates and compares four scheduling strategies:

### 👻 GhostSched *(Custom)*
The star of the show. Combines multiple techniques:
- **DVFS** (Dynamic Voltage & Frequency Scaling) — scales core voltage/freq to match workload
- **Thermal-Aware Placement** — migrates tasks away from hot cores
- **EMA Prediction** — anticipates next CPU burst, pre-scales before the spike arrives
- **big.LITTLE Placement** — assigns heavy tasks to P-cores, light tasks to E-cores

### 🔄 Round Robin
Classic time-sliced fairness. Each process gets a fixed time quantum. High fairness (`0.95`), but wastes energy when cores could be idle.

### ⚡ SJF (Shortest Job First)
Prioritizes shortest burst times. Best average wait time, but starves long tasks (`fairness ≈ 0.55`).

### 🎖 Priority Scheduling
Tasks ranked by priority level. Efficient but risks starvation of low-priority processes (`fairness ≈ 0.70`).

---

## 🔢 Key Concepts

### Jain's Fairness Index
A measure of how evenly CPU time is shared among active processes. Ranges from `0` (totally unfair) to `1.0` (perfectly fair).

```
J = (Σxᵢ)² / (n · Σxᵢ²)
```

GhostSched is computed live over all processes with CPU usage > 0.5%.

### Scheduling Modes
The backend automatically classifies the current load:

| Mode | CPU Total | Meaning |
|---|---|---|
| `IDLE` | < 15% | System mostly idle |
| `BALANCED` | 15–50% | Normal workload |
| `LOADED` | 50–80% | High activity |
| `SATURATED` | > 80% | Near-max capacity |

### EMA Predictor
Uses an Exponential Moving Average over recent CPU readings to predict the next burst. When a spike is detected, it triggers a pre-scaling event — cores ramp up *before* the workload hits.

---

## ⚙️ How It Works

```
┌───────────────────────────────────────────────────┐
│              index_realtime.html                  │
│  (Browser polls every ~1s via fetch())            │
└──────────────────┬────────────────────────────────┘
                   │  GET /processes
                   ▼
┌───────────────────────────────────────────────────┐
│                  app.py (Flask)                   │
│  psutil scans all running processes               │
│  Computes: CPU%, RAM, threads, status             │
│  Calculates: Jain fairness, sched_mode, cores     │
└──────────────────┬────────────────────────────────┘
                   │  JSON response
                   ▼
┌───────────────────────────────────────────────────┐
│              Dashboard Updates                    │
│  Charts update in-place (Chart.js)                │
│  Gantt chart appends new ticks                    │
│  EMA predictor feeds new data point               │
│  Algorithm simulator re-runs with new load        │
└───────────────────────────────────────────────────┘
```

**Performance note:** The backend uses `proc.oneshot()` to batch all process attribute reads into a single syscall — this makes scanning hundreds of processes fast and non-blocking.

---

## 📸 Screenshots

> *(Add your own screenshots here after running the project)*

| Dashboard | CPU Cores | Comparison |
|---|---|---|
| ![dashboard](https://placehold.co/280x160/060810/00f5ff?text=Dashboard&font=monospace) | ![cores](https://placehold.co/280x160/060810/b44fff?text=CPU+Cores&font=monospace) | ![compare](https://placehold.co/280x160/060810/ff2d78?text=Comparison&font=monospace) |

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas from the Research tab itself:

- [ ] Replace EMA predictor with an **LSTM neural network** for better burst prediction
- [ ] Add **real thermal sensor** data (via `sensors` on Linux)
- [ ] Implement as a **Linux kernel scheduler class** (`sched_class`) alongside CFS
- [ ] Add **WebSocket streaming** instead of polling
- [ ] Build a **process kill / renice** control panel
- [ ] Export metrics as **Prometheus** endpoints

### Steps to Contribute
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

<div align="center">

Made with 🖤 and way too much `psutil`



</div>
