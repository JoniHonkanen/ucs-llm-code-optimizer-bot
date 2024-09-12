from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CODE_ANALYSIS_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert in code analysis and optimization, capable of understanding any programming language. Analyze the following code to identify its language, purpose, structure, and behavior. Describe its logic, syntax, and functionality step by step.

    Provide a detailed analysis of:
    1. The programming language used.
    2. What the code accomplishes.
    3. Key patterns or operations (loops, recursion, data structures, etc.).
    4. Any inefficiencies (time complexity, memory usage, readability).

    Suggest improvements for:
    - Algorithmic efficiency.
    - Memory usage.
    - Readability and maintainability.
    - Potential refactoring or alternative approaches.

    Additionally, explain how to execute this code directly in a Python subprocess without using any files. Provide an example of how the code could be executed directly in memory, using appropriate commands for the identified programming language. Examples may include:

    - For Python: `python -c "<code_as_string>"`
    - For Java: `java -e "<code_as_string>"`
    - For C (via an interpreter): `gcc -x c - -o - -e "<code_as_string>"`
    - For JavaScript (Node.js): `node -e "<code_as_string>"`

    Focus on embedding the code in the execution command itself, ensuring compatibility with Python’s subprocess module.

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
    You are an expert code optimization advisor. Analyze the provided code and ensure that you understand what the code does and what programming language it is written in. Based on this understanding, suggest potential performance improvements, considering factors such as algorithm efficiency, memory usage, and readability. 

    Suggest different optimization techniques, such as alternative sorting algorithms, data structures, or more efficient algorithms for common operations, while preserving the functionality of the code.

    This is the optimized code from the previous iteration:
    {optimized_code}
    
    This code was executed in {optimized_code_run_time} seconds. Try to further optimize it.

    For the clarity, down below is the original code:

    Optimize this code:
    {code}
    
    Orginal code execution time was {original_run_time} seconds, so try to be better than that.
    
    Additionally, explain how to execute this code directly in a Python subprocess without using any files. Provide an example of how the code could be executed directly in memory, using appropriate commands for the identified programming language. Examples may include:

    - For Python: `python -c "<code_as_string>"`
    - For Java: `java -e "<code_as_string>"`
    - For C (via an interpreter): `gcc -x c - -o - -e "<code_as_string>"`
    - For JavaScript (Node.js): `node -e "<code_as_string>"`

    Focus on embedding the code in the execution command itself, ensuring compatibility with Python’s subprocess module.
    """
)
