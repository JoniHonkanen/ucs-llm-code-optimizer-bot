from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Create a prompt template, topic is a variable
CODE_OPTIMIZATION_SUGGESTION_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an expert code optimization advisor. Analyze the provided code and ensure that you understand what the code does and what programming language it is written in. Based on this understanding, suggest potential performance improvements, considering factors such as algorithm efficiency, memory usage, and readability. 

    Suggest different optimization techniques, such as alternative sorting algorithms, data structures, or more efficient algorithms for common operations, while preserving the functionality of the code.

    Optimize this code:
    {code}
    """
)
