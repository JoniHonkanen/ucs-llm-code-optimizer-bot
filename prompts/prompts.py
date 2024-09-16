from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CODE_ANALYSIS_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert in code analysis, optimization, and cross-language execution. Your task is to analyze the provided code, identify its programming language, and evaluate its structure, performance, and potential inefficiencies.

    The code will be executed and tested in a Python environment using the `subprocess` module, without writing the code to any files. You must understand how `subprocess` works and generate a suitable script that can be executed directly from memory.

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

    Finally, explain how to execute the code directly in Python's `subprocess` using an in-memory approach, without writing to external files. Generate a working execution command for the identified programming language. Example commands include:

    - For Python: `python -c "<code_as_string>"`
    - For Java: `java -e "<code_as_string>"`
    - For C: `gcc -x c - -o - -e "<code_as_string>"`
    - For JavaScript (Node.js): `node -e "<code_as_string>"`

    Focus on embedding the code inside the execution command itself and ensure the command is compatible with Python's subprocess module for execution.

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
    
    Orginal code execution time was {original_run_time} seconds, so try to be better than that.
    """
)

# Create a prompt template, topic is a variable
OPTIMIZE_OPTIMIZED_CODE_PROMPT = ChatPromptTemplate.from_template(
    """
    You are a highly skilled code optimization expert. Your task is to analyze the provided code, identify its inefficiencies, and propose further optimizations based on an understanding of the differences between the original code and the optimized version. Your goal is to achieve the best possible performance while maintaining correctness and functionality.

    **Key Points to Address:**
    1. **Identify Bottlenecks:** Use profiling and performance benchmarking techniques to identify where the current optimized code is still slow or inefficient.
    2. **Complexity Analysis:** Provide an analysis of the time and space complexity of both the original and the optimized code. Include the new optimizations you propose and their respective complexities.
    3. **Advanced Optimization Techniques:** Focus on techniques such as:
       - More efficient algorithms for common operations (sorting, searching, etc.).
       - Improved data structures to minimize memory and processing overhead.
       - Refactorings or algorithmic changes that minimize redundant operations.
    4. **Consider Multiple Approaches:** Where appropriate, suggest alternative strategies and compare their performance, complexity, and trade-offs. Choose the most effective optimization approach.
    5. **Testing and Validation:** Ensure that all optimizations maintain the correctness of the code, handle edge cases properly, and do not introduce bugs.
    6. **Trade-offs:** Identify potential trade-offs between performance improvements, readability, and maintainability. Ensure that the proposed optimizations strike a balance where necessary.
    
    Here is the **optimized code** from the previous iteration:
    {optimized_code}
    
    The execution time of the optimized code was **{optimized_code_run_time} seconds**. Your task is to optimize it further and aim for an even faster execution time while considering all the above factors.
    
    This is the **summary of the last change**: {summary_of_last_change}
    
    Here is list of tested improvements so far: {tested_improvements}

    For context, this was the **original code**:
    {code}
    
    The original code executed in **{original_run_time} seconds**. Make sure that your new optimizations go beyond both the original and previously optimized versions.

    Additionally, explain how the optimized code can be executed directly in a Python subprocess without writing any files. Provide a working example of how the code can be executed directly in memory, based on the programming language. Examples include:

    - For Python: `python -c "<code_as_string>"`
    - For Java: `java -e "<code_as_string>"`
    - For C: `gcc -x c - -o - -e "<code_as_string>"`
    - For JavaScript (Node.js): `node -e "<code_as_string>"`

    Focus on embedding the code in the execution command itself and ensure compatibility with Python's subprocess module.

    **Finally, benchmark the new optimizations and provide an estimate of the expected execution time.**
    """
)

FINAL_REPORT_AGENT_PROMPT = ChatPromptTemplate.from_template(
    """
    You are the **Final Report Agent**, tasked with analyzing and compiling a comprehensive report on the code optimization process. Your goal is to evaluate and compare the improvements made to the original code, and provide the final recommendations. The report should include:

    1. **Summary of Improvements:** Summarize each improvement, detailing the specific optimizations applied, their purpose, and how they impacted performance (e.g., reduction in execution time, memory usage, or complexity).
    2. **Comparison with Original Code:** Compare the original code with the top improvements, highlighting the main differences in algorithm, structure, or logic. Explain how these changes address the inefficiencies in the original version.
    3. **Best Improvement Selection:** Based on execution time, code readability, and overall performance, select the best improvement. Justify your choice with specific metrics (e.g., performance gain, complexity reduction) and discuss why this optimization is preferred over others.
    4. **Top 5 Improvements:** Rank the top 5 improvements by execution time and explain the relative benefits of each. Ensure the ranking prioritizes both performance and maintainability.
    5. **Testing and Validation:** Explain the testing and validation process. Confirm that the selected improvements maintain correctness, avoid introducing bugs, and are robust across different test cases.
    6. **Iteration Count:** Provide the total number of iterations performed during the optimization process and comment on how iterative changes influenced the final result.
    7. **Final Notes and Insights:** Include any additional insights, challenges encountered during the optimization process, or potential areas for further improvement.

    **Top Improvements:**
    {top_improvements}

    **Original Code:**
    {original_code}

    After completing your analysis, present the final recommendation for the best improvement and justify your decision with data-driven insights.
    """
)
