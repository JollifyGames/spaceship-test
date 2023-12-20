import subprocess
import threading
import time


def run_single_script(script_path, i):
    print("Starting script...")
    process = subprocess.Popen(["venv/Scripts/python.exe", script_path])
    process.wait()
    print(f"{i} Script finished.")


def run_script_concurrently(script_path, times, delay):
    threads = []
    for i in range(times):
        print(f"Starting script {i + 1}/{times} in a new thread")
        thread = threading.Thread(target=run_single_script, args=(script_path, i + 1))
        thread.start()
        threads.append(thread)
        time.sleep(delay)

    for thread in threads:
        thread.join()

    print("Tests are completed")


if __name__ == "__main__":
    SCRIPT_PATH = "main.py"
    TIMES = 49
    DELAY = 5

    run_script_concurrently(SCRIPT_PATH, TIMES, DELAY)
