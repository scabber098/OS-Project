"""
GhostSched — Real-Time System Monitor Backend
=============================================
Flask server that streams REAL process data via REST.
No simulation. No artificial end. Runs forever.

Install:  pip install flask flask-cors psutil
Run:      python app.py
"""

import time
import psutil
from flask import Flask, jsonify
from flask_cors import CORS

# ── GPU support (optional) ────────────────────────────────────────────────────
try:
    import GPUtil
    _GPU_AVAILABLE = True
except ImportError:
    _GPU_AVAILABLE = False

def get_gpu_stats():
    """Return overall GPU usage and memory %, or 'N/A' if unavailable."""
    if not _GPU_AVAILABLE:
        return {"gpu_usage": "N/A", "gpu_memory": "N/A"}
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"gpu_usage": "N/A", "gpu_memory": "N/A"}
        # Average across all GPUs if multiple present
        avg_load = round(sum(g.load * 100 for g in gpus) / len(gpus), 1)
        avg_mem  = round(sum(g.memoryUtil * 100 for g in gpus) / len(gpus), 1)
        return {"gpu_usage": avg_load, "gpu_memory": avg_mem}
    except Exception:
        return {"gpu_usage": "N/A", "gpu_memory": "N/A"}

app = Flask(__name__)
CORS(app)  # Allow frontend on any port/origin

# ── Warm up psutil CPU counters on startup ──────────────────────────────────
# First call always returns 0.0 — prime it now so the first /processes
# response already has meaningful values.
psutil.cpu_percent(interval=None)
for _p in psutil.process_iter():
    try:
        _p.cpu_percent(interval=None)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.route("/processes")
def get_processes():
    """
    Returns live process list + overall system stats.
    Called by the frontend every 1–2 seconds.
    cpu_percent(interval=None) is non-blocking; it uses the delta since the
    last call, so accuracy improves as the poll rate stabilises.
    """
    processes = []

    for proc in psutil.process_iter(["pid", "name", "status"]):
        try:
            with proc.oneshot():          # single syscall batch — much faster
                pid     = proc.pid
                name    = proc.name() or "unknown"
                cpu_pct = proc.cpu_percent(interval=None)   # non-blocking
                mem_mb  = proc.memory_info().rss / (1024 * 1024)
                status  = proc.status()
                threads = proc.num_threads()

            processes.append({
                "pid":     pid,
                "name":    name,
                "cpu":     round(cpu_pct, 1),
                "memory":  round(mem_mb, 2),   # RSS in MB
                "status":  status,
                "threads": threads,
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass   # process disappeared or we lack permission — skip silently

    # Sort by CPU descending so the busiest processes surface first
    processes.sort(key=lambda p: p["cpu"], reverse=True)

    # ── Overall system stats ─────────────────────────────────────────────────
    vm          = psutil.virtual_memory()
    cpu_all     = psutil.cpu_percent(percpu=True, interval=None)
    cpu_total   = round(sum(cpu_all) / max(1, len(cpu_all)), 1)

    # Per-core info
    try:
        freq_list = psutil.cpu_freq(percpu=True) or []
    except Exception:
        freq_list = []

    cores = []
    for i, pct in enumerate(cpu_all):
        freq_obj = freq_list[i] if i < len(freq_list) else None
        cores.append({
            "id":      i,
            "load":    round(pct, 1),
            "freq":    round(freq_obj.current) if freq_obj else 0,
            "maxFreq": round(freq_obj.max)     if freq_obj else 0,
            "type":    "P-CORE" if i < (len(cpu_all) // 2) or len(cpu_all) <= 4 else "E-CORE",
        })

    # ── Jain's fairness index over active processes ──────────────────────────
    active_loads = [p["cpu"] for p in processes if p["cpu"] > 0.5]
    if len(active_loads) >= 2:
        n    = len(active_loads)
        jain = (sum(active_loads) ** 2) / (n * sum(x ** 2 for x in active_loads))
    else:
        jain = 1.0

    # ── Scheduling mode ───────────────────────────────────────────────────────
    if cpu_total < 15:
        mode = "IDLE"
    elif cpu_total < 50:
        mode = "BALANCED"
    elif cpu_total < 80:
        mode = "LOADED"
    else:
        mode = "SATURATED"

    gpu = get_gpu_stats()

    return jsonify({
        "timestamp":  time.time(),
        "processes":  processes,
        "total":      len(processes),
        "system": {
            "cpu_total":   cpu_total,
            "cores":       cores,
            "mem_percent": vm.percent,
            "mem_used_mb": round(vm.used  / (1024 * 1024), 1),
            "mem_total_mb":round(vm.total / (1024 * 1024), 1),
            "sched_mode":  mode,
            "fairness":    round(jain, 4),
            "active_procs":len(active_loads),
            "gpu_usage":   gpu["gpu_usage"],
            "gpu_memory":  gpu["gpu_memory"],
        },
    })


@app.route("/system")
def system_info():
    """Lightweight endpoint — overall CPU/mem only."""
    vm      = psutil.virtual_memory()
    cpu_all = psutil.cpu_percent(percpu=True, interval=None)
    return jsonify({
        "cpu_total":    round(sum(cpu_all) / max(1, len(cpu_all)), 1),
        "cores":        [round(p, 1) for p in cpu_all],
        "mem_percent":  vm.percent,
        "mem_used_mb":  round(vm.used  / (1024 * 1024), 1),
        "mem_total_mb": round(vm.total / (1024 * 1024), 1),
        "timestamp":    time.time(),
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "ts": time.time()})


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 52)
    print("  GhostSched Real-Time Monitor  —  Backend")
    print("=" * 52)
    print("  Processes  →  http://127.0.0.1:5000/processes")
    print("  System     →  http://127.0.0.1:5000/system")
    print("  Health     →  http://127.0.0.1:5000/health")
    print("=" * 52)
    # threaded=True so concurrent frontend polls don't queue up
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
