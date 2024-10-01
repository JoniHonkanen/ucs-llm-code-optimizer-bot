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
    You are a code optimization expert tasked with improving provided code that has already undergone several optimizations. Your goal is to produce code that is **faster, more memory-efficient, and more readable** than both the **original code** and the **latest optimized version**. All improvements must preserve functionality while delivering measurable performance gains.

    **Your Key Responsibilities:**

    1. **Preserve Original Purpose and Correctness**:
       Ensure that the optimized code retains the functionality and purpose of the original code without altering its intended behavior. All changes must maintain the correctness of the output.

    2. **Identify and Address Performance Bottlenecks**:
       Use profiling or benchmarking data to identify areas where the current optimized code is still inefficient. Prioritize impactful optimizations that target runtime and memory usage.

    3. **Analyze Complexity and Resource Usage**:
       Provide a detailed analysis of both the original and current optimized code. Assess time complexity, memory usage, and other resource considerations. Describe how each new improvement affects these metrics.

    4. **Propose Unique, Impactful Optimizations**:
       Propose optimizations that are clearly better in terms of performance, memory efficiency, and readability, while being significantly distinct from previously tested improvements listed in **'Tested Improvements So Far'**. Consider:
       - Enhancing algorithm efficiency (sorting, searching, data handling, etc.).
       - Replacing data structures to reduce memory usage or computation time.
       - Eliminating redundant code or unnecessary operations.
       - Leveraging parallelization or concurrency for clear gains in performance.

    5. **Improve Code Readability and Maintainability**:
       Make the code not only efficient but also easy to read and maintain. This includes clear naming conventions, modularity, and reducing unnecessary complexity.

    6. **Refactor for Conciseness and Efficiency**:
       Refactor the code to remove any unnecessary operations or redundancies. Keep it concise, balancing performance gains with readability.

    7. **Testing, Validation & Correctness Assurance**:
       Thoroughly test the optimized code for correctness, covering various input sizes and edge cases. Confirm that the behavior remains identical to the original.
       - **Failure Condition**: If the execution time is `0`, consider the optimization to have failed (indicating incorrect execution or an error).

    8. **Benchmark and Validate Improvements**:
       Provide comprehensive benchmarks of the new optimizations against both the original and previously optimized versions, considering performance, complexity, and trade-offs. Clearly indicate how the new changes improve execution time, memory usage, and code readability.

    9. **Derive New Execution Command for Optimized Code**:
       Formulate a new execution command for running the optimized code based on the original command provided. This command must be executable as a file in a subprocess.

       **Examples of execution commands**:
       - Python: `python <filepath>`
       - Java: `javac <filepath> && java <compiled_class>`
       - C: `gcc <filepath> -o <output_binary> && ./<output_binary>`
       - JavaScript: `node <filepath>`
       
       **Note**: The placeholder `<filepath>` will be replaced with the actual file path during execution. Ensure that this command accurately reflects the necessary steps to compile or run the optimized code.

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

    2. **Validate Functional Consistency**: Verify that the optimized code retains the same functionality and purpose as the original code, ensuring the output remains identical.

    3. **Ensure Transformative Optimization**: Compare the new optimization against both the **original** and **last optimized code**. If the proposed changes are too similar or marginal, refine the approach to achieve a significant performance boost, memory reduction, or readability enhancement.

    4. **Benchmark the New Optimizations**:
       Provide comprehensive benchmarks detailing the new optimization's performance, memory usage, and readability relative to both the original and previously optimized code.

    **Final Task**:
    
    Return a response that includes all fields necessary for the `CodeImprovement` schema:

    - **description**: A detailed explanation of the improvement and its purpose.
    - **changes_summary**: Summary of the changes made to the original code as part of this improvement.
    - **complexity_reduction**: Estimated reduction in time complexity or runtime performance as a factor (e.g., `0.5` for a 50% reduction).
    - **updated_code**: The code after applying the improvement, ensuring it's more efficient while preserving functionality.
    - **test_description**: A concise note describing what was optimized (e.g., algorithm change) to avoid repeating similar improvements.
    - **run_command**: The full command to execute the optimized code in a Python subprocess.

    **Reminder**:
    - Produce code that is **better than both the original and last optimized code** in terms of performance, memory usage, and readability.
    - **Do not propose or test already tested improvements** as listed in **'Tested Improvements So Far'.** All new optimizations must be distinct and impactful.
    - **Ensure the optimized code is free from duplicated code or unnecessary operations.**
    - **Ensure the purpose and functionality of the original code are preserved.**
    """
)


FINAL_REPORT_AGENT_PROMPT = ChatPromptTemplate.from_template(
    """
    You are the **Final Report Agent**, responsible for analyzing and compiling a thorough evaluation of multiple optimized versions of code that achieve the same objective but differ in their algorithms and performance. Your task is to compare these versions and provide a data-driven recommendation for the best one. Your evaluation should focus on key performance criteria, including execution speed, algorithmic efficiency, memory usage, and code maintainability.

    The report should include the following sections:

    1. **Summary of Each Optimized Version:** Provide a concise summary of each version, detailing the specific algorithm or approach used. Explain the intended purpose of any unique optimization or strategy within the version and its impact on performance metrics (e.g., execution time, memory usage, or complexity). Highlight any significant trade-offs or side effects of each approach.

    2. **Comparison Across All Versions:** Compare all versions against each other, focusing on major differences in algorithms, structure, and logic. Clearly articulate how each version's approach addresses specific inefficiencies and how these differences affect performance.

    3. **Metrics-Based Evaluation:** Evaluate each version based on the following criteria:
       - **Execution Time:** Measure and compare the average time taken to run each version across different input sizes.
       - **Memory Usage:** Track and compare peak memory consumption for each version.
       - **Algorithmic Complexity:** Analyze and compare the computational complexity of each version.
       - **Readability & Maintainability:** Assess the clarity and modifiability of the code.
       - Provide a ranking or scoring system to objectively compare how well each version performs in these areas.

    4. **Selection of Best Version:** Select the version that offers the best balance across execution time, memory usage, complexity, readability, and maintainability. Justify your choice with quantitative data and qualitative analysis, discussing how the selected version outperforms the others while maintaining correctness and efficiency.

    5. **Edge Case Testing and Validation:** Describe the testing process used to validate all versions, including tests on various input scenarios (small, large, edge cases, and stress tests). Confirm that the chosen version maintains correctness, robustness, and does not introduce any bugs across these test cases.

    6. **Purpose Consistency Check:** Verify that the selected version retains the original purpose and behavior of the code. Ensure that optimizations did not alter the fundamental goal or functionality.

    **Top Improvements:**
    {top_improvements}

    **Original Code:**
    {original_code}
    
    **Original Purpose and Context:**
    {original_purpose}

    Conclude your report with a final recommendation for the best optimized version, providing a data-driven justification for your decision. Clearly explain how it strikes an optimal balance between computational efficiency, memory usage, maintainability, and consistency of purpose.
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
