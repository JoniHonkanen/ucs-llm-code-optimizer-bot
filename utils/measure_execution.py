def measure_execution_time(code: str, execution_command: str) -> float:
    import subprocess
    import time

    # Measure execution time
    start_time = time.time()
    result = subprocess.run(execution_command)
    end_time = time.time()

    execution_time = end_time - start_time

    if result.returncode == 0:
        print("Execution finished successfully.")
    else:
        print(f"Execution failed with return code {result.returncode}.")

    print(f"Execution time: {execution_time} seconds")

    return execution_time
