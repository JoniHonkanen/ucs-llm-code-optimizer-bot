from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CODE_ANALYSIS_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert in code analysis, optimization, and cross-language execution. Your task is to analyze the provided code, identify its programming language, and evaluate its structure, performance, and potential inefficiencies.

    The code will be executed and tested in a Python environment using the `subprocess` module. You must generate a suitable script that can be written to a file and executed from that file, matching the detected programming language.

    Provide a detailed analysis of:
    1. The programming language used.
    2. The code's purpose and behavior, explaining its logic and functionality step by step.
    3. The structure of the code, including key patterns (loops, conditionals, recursion, etc.).
    4. Any inefficiencies (time complexity, memory usage, code readability).

    After the analysis, provide suggestions for improvement in:
    - Algorithmic efficiency.
    - Memory consumption.
    - Readability and maintainability.
    - Any refactoring or alternative approaches that could optimize performance.

    Finally, based on the identified programming language, provide an exact execution command that can be used in Python's `subprocess` module. The command should reference a temporary file where the code is written before execution. 

    The execution command should take into account the programming language, examples include:
    
    - For Python: `python <filepath>`
    - For Java: `javac <filepath> && java <compiled_class>`
    - For C: `gcc <filepath> -o <output_binary> && ./<output_binary>`
    - For JavaScript (Node.js): `node <filepath>`
    
    **Important**: The placeholder `<filepath>` must be included in the execution command, as it will later be replaced with the real file path during execution.

    Focus on ensuring that the code is written to a file and executed using that file. The command must be compatible with Python's subprocess module for file-based execution.

    Analyze this code:
    {original_code}
    """
)

# Create a prompt template, topic is a variable
CODE_OPTIMIZATION_SUGGESTION_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert code optimization advisor. Analyze the provided code and ensure that you understand what the code does and what programming language it is written in. Based on this understanding, suggest potential performance improvements, considering factors such as algorithm efficiency, memory usage, and readability.

    Suggest different optimization techniques, such as alternative sorting algorithms, data structures, or more efficient algorithms for common operations, while preserving the functionality of the code.

    Optimize this code:
    {code}
    
    The original code execution time was {original_run_time} seconds, so try to be better than that.

    Here is the **original code execution command** that was successfully executed. You must derive a similar execution command for the optimized code, ensuring it runs successfully:
    {original_code_execution}
    
    After completing your analysis and optimization, provide the following information:
    
    - A **detailed description** of the improvement and its purpose.
    - A **summary of the changes** made to the original code.
    - Whether the optimization was **successful**.
    - The **reduction in time complexity** or other performance benefits.
    - The **optimized code** after applying the changes.
    - The **execution command** to run the optimized code.
    - A **test description** explaining the specific optimization (e.g., algorithm or technique) tested to avoid repeating similar improvements.
    """
)

OPTIMIZE_OPTIMIZED_CODE_PROMPT = ChatPromptTemplate.from_template(
    """
    You are a code optimization expert tasked with improving the provided code, which has already undergone several optimizations. Your goal is to produce code that is **faster, more memory-efficient, and more readable** than both the **original code** and the **latest optimized version**. All improvements must maintain the code's functionality while delivering measurable performance gains.

    **Your Key Responsibilities:**

    1. **Preserve Original Purpose and Correctness**:
       Ensure that the optimized code retains the same functionality and purpose as the original code, without altering its intended behavior. All changes must preserve the correctness of the output.

    2. **Identify Bottlenecks for Improvement**:
       Use profiling or benchmarking data to identify areas where the current optimized code is still inefficient. Prioritize optimizations that have the most impact on runtime and memory usage.

    3. **Complexity and Resource Usage Analysis**:
       Provide a detailed analysis of both the original and the currently optimized code. Assess time complexity, memory usage, and any other significant resource considerations. Describe how each new improvement affects these factors.

    4. **Propose Better, Unique Optimizations**:
       Propose optimizations that are distinct and better in performance, memory efficiency, and readability. Prioritize:
       - Improving algorithm efficiency (sorting, searching, data handling, etc.).
       - Replacing data structures to reduce memory footprint or computation time.
       - Eliminating duplicated or redundant code blocks.
       - Introducing parallelization or concurrency where it offers clear gains.

       **Note**: The proposed optimization must significantly differ from previously tested improvements, which are listed in **'Tested Improvements So Far'**.

    5. **Enhance Code Readability and Maintainability**:
       Strive to make the code not only more efficient but also easier to read and maintain. This includes clear naming conventions, modularity, and eliminating unnecessary complexity.

    6. **Refactor for Conciseness and Efficiency**:
       Refactor the code to remove any unnecessary operations or redundancy. Ensure it remains concise while balancing performance gains with readability.

    7. **Testing, Validation & Failure Handling**:
       Rigorously test the optimized code for correctness and edge cases. Confirm that the behavior of the code remains identical to the original.
       - If the execution time is `0`, the optimization is considered a failure, indicating it did not execute correctly.

    8. **Benchmark, Compare & Validate Improvements**:
       Compare multiple approaches, considering their performance, complexity, and trade-offs. Provide benchmarks and clear evidence of how each new optimization is better (faster, more memory-efficient, and/or more readable) than both the original and previously optimized versions.

    9. **Derive Execution Command**:
       Formulate a new execution command to run the optimized code based on the original command. This command must be executable from a file in a subprocess.

       **Examples of execution commands**:
       - Python: `python <filepath>`
       - Java: `javac <filepath> && java <compiled_class>`
       - C: `gcc <filepath> -o <output_binary> && ./<output_binary>`
       - JavaScript: `node <filepath>`
       
       **Important**: The placeholder `<filepath>` will later be replaced with the actual file path during execution.

    **Provided Code Details**:

    - **Optimized Code**: 
      {optimized_code}

    - **Execution Time (Optimized)**: 
      {optimized_code_run_time} seconds
      *Note: An execution time of `0` seconds indicates that the optimization failed to execute correctly.*

    - **Summary of Last Change**: 
      {summary_of_last_change}

    - **Tested Improvements So Far**: 
      {tested_improvements}

    - **Original Code**: 
      {code}

    - **Original Execution Time**: 
      {original_run_time} seconds

    - **Original Execution Command**: 
      {original_code_execution}

    **Next Steps**:

    1. Propose and explain **new optimizations** to improve the performance, memory usage, and readability of the **current optimized code** further. Ensure optimizations are distinct from those in **'Tested Improvements So Far'**.

    2. **Validate Functional Consistency**: Verify that the optimized code retains the same functionality and purpose as the original code. The behavior and output should be identical.

    3. **Ensure Transformative Optimization**: Compare the new optimization against both the **original** and **last optimized code**. If the proposed changes are too similar or marginal, refine your approach to achieve a significant performance boost, memory reduction, or readability enhancement.

    4. **Benchmark the New Optimizations**:
       Provide a comprehensive benchmark of the new optimization's performance, memory usage, and readability compared to both the original and previously optimized code.

    **Reminder**:

    - Focus on producing code that is **better than both the original and last optimized code** in terms of performance, memory usage, and readability.
    - **Do not propose or test improvements that have already been tested** as listed in **'Tested Improvements So Far'.** Always introduce unique and impactful optimizations.
    - **Ensure the optimized code is free of duplicated code and unnecessary operations.**
    - **Ensure all new optimizations are distinct and transformative compared to the last optimized code.**
    - **Indicate whether the purpose and functionality of the original code have been preserved after optimization.**
    """
)


FINAL_REPORT_AGENT_PROMPT = ChatPromptTemplate.from_template(
    """
    You are the **Final Report Agent**, tasked with analyzing and compiling a comprehensive report on the code optimization process. Your goal is to evaluate and compare the improvements made to the original code, and provide the final recommendation for the best-optimized code among the top improvements. The report should include:

    1. **Summary of Improvements:** Summarize each of the top improvements, detailing the specific optimizations applied, their purpose, and how they impacted performance (e.g., reduction in execution time, memory usage, or complexity).

    2. **Comparison with Original Code:** Compare the original code with each of the top improvements, highlighting the main differences in algorithm, structure, or logic. Explain how these changes address the inefficiencies in the original version.

    3. **Best Improvement Selection:** Based on execution time, memory usage, code readability, simplicity, and overall performance, select the best improvement. Justify your choice with specific metrics (e.g., performance gain, memory efficiency, simplicity, correctness) and explain how it strikes the best balance between these factors. 
    For example: "This improvement strikes the best balance between simplicity, performance, and correctness. It is the most appropriate choice for efficiently solving the problem while maintaining readability and robustness."
    Discuss why this improvement is preferred over others, supported by data-driven insights.

    4. **Ranking of Improvements:** Rank the top improvements by execution time, memory usage, and overall performance. Explain the relative benefits of each, considering the trade-offs between performance, memory efficiency, and maintainability. Ensure the ranking prioritizes both computational efficiency and code maintainability.

    5. **Testing and Validation:** Explain the testing and validation process. Confirm that the selected improvement maintains correctness, avoids introducing bugs, and is robust across different test cases.
    
    6. **Purpose Consistency:** Verify whether the selected best improvement still performs the same purpose as the original code. Ensure that the optimization did not alter the fundamental goal or role of the code.

    **Top Improvements:**
    {top_improvements}

    **Original Code:**
    {original_code}
    
    **Original Purpose and Context:**
    {original_purpose}

    After completing your analysis, present your final recommendation for the best improvement and justify your decision with data-driven insights.
    """
)

FIX_EXECUTION_COMMAND_PROMPT = ChatPromptTemplate.from_template(
    """
    For some reason, the execution command provided is not working as expected. Please review the command and ensure that it is correctly formatted for execution using Python's `subprocess` module. The command should be able to execute the code from a file rather than from memory.

    If the first execution attempt does not work, analyze the issue and propose a fix.

    **Important**: The placeholder `<filepath>` must be included in the execution command, as it will later be replaced with the real file path during execution.

    Here is the runnable code snippet that needs to be fixed:
    {runnable_code}

    Please ensure that after any necessary corrections, the command will work as expected.
    """
)
