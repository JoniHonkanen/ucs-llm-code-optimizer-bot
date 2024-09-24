import os
import datetime
from schemas import (
    AgentState,
    OriginalCodeAnalyze,
    CodeImprovement,
    FinalReport,
    FixExecutionCommand,
)
from prompts.prompts import (
    CODE_ANALYSIS_PROMPT,
    CODE_OPTIMIZATION_SUGGESTION_PROMPT,
    OPTIMIZE_OPTIMIZED_CODE_PROMPT,
    FINAL_REPORT_AGENT_PROMPT,
    FIX_EXECUTION_COMMAND_PROMPT,
)
from utils.measure_execution import measure_execution_time


# Analyzes the code and provides suggestions for improvement
def code_analyzer_agent(state: AgentState, llm) -> AgentState:
    print("\n** CODE ANALYZER AGENT **")
    structured_llm = llm.with_structured_output(OriginalCodeAnalyze)
    prompt = CODE_ANALYSIS_PROMPT.format(original_code=state["original_code"])
    res = structured_llm.invoke(prompt)
    state["orginal_analyze"] = res
    state["code_execution_command"] = res.run_command
    state["file_extension"] = res.file_extension
    return state


# Executes the code and measures the time it takes to run
def code_measurer_agent(state: AgentState) -> AgentState:
    print("\n** CODE MEASURER AGENT **")

    # Ensure 'top_improvements' exists in state
    state.setdefault("top_improvements", [])

    # Define the log file path
    log_directory = "improvements"
    log_file_name = "improvements.log"
    log_file_path = os.path.join(log_directory, log_file_name)

    # Ensure the 'improvements' directory exists
    os.makedirs(log_directory, exist_ok=True)

    # Initialize 'new_optimization_logged' flag if not present
    if "new_optimization_logged" not in state:
        state["new_optimization_logged"] = False

    # Get the improved code from the state
    improved_code = state.get("improved_code")

    # If there is improved code available, measure its execution time
    if improved_code:
        # Measure the execution time of the improved code
        improved_code.run_time = measure_execution_time(
            improved_code.updated_code,
            improved_code.run_command,
            state["file_extension"],
        )

        # Update top improvements if necessary
        top_improvements = state["top_improvements"]
        if len(top_improvements) < 5:
            top_improvements.append(improved_code)
        elif improved_code.run_time < top_improvements[-1].run_time:
            top_improvements[-1] = improved_code

        # Sort the top improvements by run_time
        top_improvements.sort(key=lambda x: x.run_time)

        # Prepare the log entry
        timestamp = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        log_entry = (
            f"Iteration {state['iteration']} ({timestamp}):\n"
            f"Execution Time: {improved_code.run_time:.6f} seconds\n"
            f"Description: {improved_code.changes_summary}\n"
            f"{improved_code.updated_code}\n\n\n"
        )

        # Add the "New Optimization Starts" message only once, after the first iteration's log entry
        if state["iteration"] == 1 and not state["new_optimization_logged"]:
            log_entry += "=== New Optimization Starts ===\n\n"
            state["new_optimization_logged"] = True

        # Read existing log entries if any
        existing_logs = ""
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                existing_logs = log_file.read()

        # Write the new log entry followed by existing logs
        with open(log_file_path, "w") as log_file:
            log_file.write(log_entry + existing_logs)

    else:
        # Measure the original code's execution time
        measure = measure_execution_time(
            state["original_code"],
            state["code_execution_command"],
            state["file_extension"],
        )
        if measure > 0:
            state["original_run_time"] = measure
            state["original_execution_success"] = True
        else:
            print("Execution failed.")
            state["original_run_time"] = 0
            state["original_execution_success"] = False

    # Increment the iteration count
    state["iteration"] += 1

    return state


def code_improver_agent(state: AgentState, llm) -> AgentState:
    print("\n** CODE IMPROVER AGENT **")
    structured_llm = llm.with_structured_output(CodeImprovement)
    if "improved_code" in state and state["improved_code"] is not None:
        print("OPTIMOIDAAAN!")
        # if not first loop, improved code is the improved code from previous loop
        prompt = OPTIMIZE_OPTIMIZED_CODE_PROMPT.format(
            optimized_code=state["improved_code"].updated_code,
            original_code_execution=state["code_execution_command"],
            optimized_code_run_time=state["improved_code"].run_time,
            summary_of_last_change=state["improved_code"].changes_summary,
            tested_improvements=state["tested_improvements"],
            code=state["original_code"],
            original_run_time=state["original_run_time"],
        )
    else:
        print("EKA LOOPPI")
        # if first loop, improved code is the original code
        prompt = CODE_OPTIMIZATION_SUGGESTION_PROMPT.format(
            code=state["original_code"],
            original_run_time=state["original_run_time"],
            original_code_execution=state["code_execution_command"],
        )

    res = structured_llm.invoke(prompt)
    state["improved_code"] = res
    # Ensure 'tested_improvements' key exists
    if "tested_improvements" not in state:
        state["tested_improvements"] = []
    state["tested_improvements"].append(res.test_description)

    return state


def final_report_agent(state: AgentState, llm) -> AgentState:
    print("\n\n** FINAL REPORT AGENT **")
    bestImprovements = state["top_improvements"]
    bestImprovementsForLLM = []

    # Improvements for better format, easier to read (LLM)
    for index, improvement in enumerate(bestImprovements, start=1):
        bestImprovementsForLLM.append(
            f"Improvement {index}:\n"
            f"Description: {improvement.description}\n"
            f"Changes Summary: {improvement.changes_summary}\n"
            f"Execution Time: {improvement.run_time} seconds\n"
            f"Updated Code:\n{improvement.updated_code}\n"
        )

    structured_llm = llm.with_structured_output(FinalReport)
    prompt = FINAL_REPORT_AGENT_PROMPT.format(
        top_improvements=bestImprovementsForLLM,
        original_code=state["original_code"],
        original_purpose=state["orginal_analyze"].context_and_purpose,
    )
    res = structured_llm.invoke(prompt)
    print(res)
    state["final"] = res

    # Ensure the 'improvements' folder exists
    improvements_folder = "improvements"
    os.makedirs(improvements_folder, exist_ok=True)

    # Save the final report to the improvements folder using res.filename
    filepath = os.path.join(improvements_folder, res.filename)

    # save the final report to a programming file using res.filename
    with open(filepath, "w") as f:
        # Add comments at the beginning of the file
        f.write(f"{res.best_improvement_description}\n")
        f.write(f"{res.performance_gain}\n\n")
        # Add the purpose consistency check as a comment
        f.write(f"# Optimization purpose consistency: {res.purpose_consistency}\n\n")
        f.write(res.selected_code)

    return state


def fix_execution_agent(state: AgentState, llm) -> AgentState:
    print("\n\n** FIX EXECUTION AGENT **")
    structured_llm = llm.with_structured_output(FixExecutionCommand)
    prompt = FIX_EXECUTION_COMMAND_PROMPT.format(
        runnable_code=state["code_execution_command"]
    )
    res = structured_llm.invoke(prompt)
    state["code_execution_command"] = res.new_execution_command

    return state
