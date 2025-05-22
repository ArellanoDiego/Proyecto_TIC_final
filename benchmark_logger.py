import os
import subprocess
import psutil
from datetime import datetime

RESULTS_DIR = "../results-vm"
os.makedirs(RESULTS_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join(RESULTS_DIR, f"benchmark_{timestamp}.txt")

def run_sysbench():
    try:
        result = subprocess.run(
            ["sysbench", "cpu", "--cpu-max-prime=20000", "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        return "Sysbench not found. Skipping benchmark.\n"
    except subprocess.CalledProcessError as e:
        return f"Sysbench execution failed:\n{e.stderr}\n"

print("Running sysbench CPU benchmark...")
sysbench_output = run_sysbench()

print("Collecting system metrics...")
cpu_percent = psutil.cpu_percent(interval=1)
virtual_mem = psutil.virtual_memory()
mem_percent = virtual_mem.percent
total_mem = virtual_mem.total // (1024 * 1024)
available_mem = virtual_mem.available // (1024 * 1024)

with open(filename, "w") as f:
    f.write("=== Sysbench CPU Benchmark ===\n")
    f.write(sysbench_output)
    f.write("\n=== System Metrics ===\n")
    f.write(f"CPU Usage: {cpu_percent}%\n")
    f.write(f"Memory Usage: {mem_percent}%\n")
    f.write(f"Total Memory: {total_mem} MB\n")
    f.write(f"Available Memory: {available_mem} MB\n")

print(f"Results saved to {filename}")
