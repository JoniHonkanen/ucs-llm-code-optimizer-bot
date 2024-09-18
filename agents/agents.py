import os
from schemas import AgentState, OriginalCodeAnalyze, CodeImprovement, FinalReport
from prompts.prompts import (
    CODE_ANALYSIS_PROMPT,
    CODE_OPTIMIZATION_SUGGESTION_PROMPT,
    OPTIMIZE_OPTIMIZED_CODE_PROMPT,
    FINAL_REPORT_AGENT_PROMPT,
)
from utils.measure_execution import measure_execution_time


#
def code_analyzer_agent(state: AgentState, llm) -> AgentState:
    print("\n** CODE ANALYZER AGENT **")
    structured_llm = llm.with_structured_output(OriginalCodeAnalyze)
    prompt = CODE_ANALYSIS_PROMPT.format(original_code=state["original_code"])
    res = structured_llm.invoke(prompt)
    state["code_execution_command"] = res.run_command
    return state


# Executes the code and measures the time it takes to run
def code_measurer_agent(state: AgentState) -> AgentState:
    print("\n** CODE MEASURER AGENT **")

    # Ensure 'top_improvements' exists in state
    if "top_improvements" not in state:
        state["top_improvements"] = []

    # If there is an improved code available, measure its execution time
    if "improved_code" in state and state["improved_code"] is not None:
        # Measure the execution time of the improved code
        state["improved_code"].run_time = measure_execution_time(
            state["improved_code"].updated_code, state["improved_code"].run_command
        )

        # Update top improvements if it's either one of the top 5 fastest or fewer than 5 improvements exist
        if len(state["top_improvements"]) < 5:
            state["top_improvements"].append(state["improved_code"])
        elif state["improved_code"].run_time < state["top_improvements"][-1].run_time:
            state["top_improvements"][-1] = state["improved_code"]

        # Sort only when necessary to keep the top improvements ordered by run_time
        state["top_improvements"].sort(key=lambda x: x.run_time)

    else:
        # If no improvements have been made, measure the original code's execution time
        state["original_run_time"] = measure_execution_time(
            state["original_code"], state["code_execution_command"]
        )

    # Increment the iteration count
    state["iteration"] += 1

    return state


def code_improver_agent(state: AgentState, llm) -> AgentState:
    print("\n** CODE IMPROVER AGENT **")
    structured_llm = llm.with_structured_output(CodeImprovement)
    if "improved_code" in state and state["improved_code"] is not None:
        # if not first loop, improved code is the improved code from previous loop
        prompt = OPTIMIZE_OPTIMIZED_CODE_PROMPT.format(
            optimized_code=state["improved_code"].updated_code,
            optimized_code_run_time=state["improved_code"].run_time,
            summary_of_last_change=state["improved_code"].changes_summary,
            tested_improvements=state["tested_improvements"],
            code=state["original_code"],
            original_run_time=state["original_run_time"],
        )
    else:
        # if first loop, improved code is the original code
        prompt = CODE_OPTIMIZATION_SUGGESTION_PROMPT.format(
            code=state["original_code"], original_run_time=state["original_run_time"]
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
    )
    res = structured_llm.invoke(prompt)
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
        f.write(res.selected_code)

    return state
