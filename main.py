import time
import os
import subprocess
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

# own imports
from schemas import AgentState
from agents.agents import agent

# .env file is used to store the api key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize the language model
# use dotnenv to load OPENAI_API_KEY api key
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
)


# Create a graph with the state
workflow = StateGraph(AgentState)


def create_code_f(state: AgentState):
    return agent(state, llm)


# Nodes
workflow.add_node("agent", create_code_f)

# Edges
workflow.add_edge("agent", END)

# Set entry point
workflow.set_entry_point("agent")

# Build the graph
app = workflow.compile()

res = app.invoke(
    {
        "code": """def find_top_students(students, grades):
    # Combine student names with their grades
    student_grades = []
    for i in range(len(students)):
        student_grades.append((students[i], grades[i]))

    # Sort students by their grades in descending order
    for i in range(len(student_grades)):
        for j in range(i + 1, len(student_grades)):
            if student_grades[i][1] < student_grades[j][1]:
                student_grades[i], student_grades[j] = student_grades[j], student_grades[i]

    # Return the top 3 students
    return student_grades[:3]

students = ["Alice", "Bob", "Charlie", "David", "Eve"]
grades = [85, 92, 88, 91, 76]

top_students = find_top_students(students, grades)
print(top_students)"""
    }
)

print("\nNYT LÄHTEE:")
start_time = time.time()
subprocess.run(res["code_execution_command"])  # Compile
end_time = time.time()
execution_time = end_time - start_time

print("VALMIS")
print(f"Execution time: {execution_time} seconds")
