def measure_execution_time(code: str, execution_command: str, file_extension) -> float:
    import subprocess
    import time
    import os

    # Ensure the 'improvements' folder and 'temp' subfolder exist
    improvements_folder = "improvements"
    temp_folder = os.path.join(improvements_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    # Generate the filename and path for the temporary code file
    filename = "temp_code" + file_extension
    filepath = os.path.join(temp_folder, filename)

    # Write the code to the temporary file
    with open(filepath, "w") as f:
        f.write(code)

    # Measure execution time
    start_time = time.perf_counter()

    # Replace <filepath> in the execution_command with the actual file path
    execution_command = execution_command.replace("<filepath>", filepath)

    # Use shell=True if execution_command is a string
    result = subprocess.run(execution_command, shell=True)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if result.returncode == 0:
        print("Execution finished successfully.")
    else:
        print(f"Execution failed with return code {result.returncode}.")
        execution_time = 0  # Return 0 if execution failed

    print(f"Execution time: {execution_time} seconds")

    os.remove(filepath)

    return execution_time
