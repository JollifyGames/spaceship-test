import subprocess
import time


def run_script(script_path, times, delay):
    processes = []
    for i in range(times):
        print(f"Starting script {i + 1}/{times}")
        process = subprocess.Popen(["venv/Scripts/python.exe", script_path])
        processes.append(process)
        time.sleep(delay)

    for i, process in enumerate(processes):
        print(f"Waiting for script {i + 1} to finish...")
        process.wait()
        print(f"Script {i + 1} finished.")


if __name__ == "__main__":
    SCRIPT_PATH = "main.py"
    TIMES = 50
    DELAY = 3

    run_script(SCRIPT_PATH, TIMES, DELAY)
