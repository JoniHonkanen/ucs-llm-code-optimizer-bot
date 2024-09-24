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
    You are a code optimization expert tasked with further optimizing the provided code. Your goal is to maximize performance without compromising correctness or functionality. Review the optimizations made so far and propose more improvements.

    **Your Key Responsibilities:**
    
    1. **Identify Bottlenecks**:
       Use profiling or benchmarking data to identify areas of the current optimized code that are still inefficient.
    
    2. **Complexity Analysis**:
       Provide a detailed complexity analysis (time and space) of both the original and optimized code. For each new optimization you propose, include the impact on complexity.
    
    3. **Advanced Optimization Techniques**:
       Focus on improvements in:
       - Algorithm efficiency (sorting, searching, data handling, etc.).
       - Data structures that reduce memory usage and computation overhead.
       - Refactoring to remove redundancies or unnecessary operations.

    4. **Compare Multiple Approaches**:
       Where applicable, propose alternative solutions, comparing their performance, complexity, and trade-offs. Always aim to choose the most effective approach.

    5. **Testing & Validation**:
       Ensure all optimizations are rigorously tested for correctness, edge case handling, and the absence of new bugs.
    
    6. **Trade-offs**:
       Consider the trade-offs between performance, code readability, and maintainability. Prioritize significant performance gains over minor readability issues, but avoid making the code unmanageable.

    **Provided Code Details:**
    
    - **Optimized Code**: 
      {optimized_code}

    - **Execution Time (Optimized)**: 
      {optimized_code_run_time} seconds

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
    
    1. Propose and explain optimizations to improve the current performance.
    
    2. Derive a new execution command for running the optimized code. You must:
       - Base it on the original execution command but adapt it for the optimized code.
       - Ensure the command is valid and executable from a file.

       **Examples of execution commands**:
       - Python: `python <filepath>`
       - Java: `javac <filepath> && java <compiled_class>`
       - C: `gcc <filepath> -o <output_binary> && ./<output_binary>`
       - JavaScript: `node <filepath>`
       
    **Important**: The placeholder `<filepath>` must be included in the execution command, as it will later be replaced with the real file path during execution.

    3. Ensure the command is suitable for running in a subprocess, and the code is executed from a file.

    **Benchmark the New Optimizations**:
    
    Provide an estimate of the expected execution time for your new optimizations compared to both the original and the currently optimized versions.
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
