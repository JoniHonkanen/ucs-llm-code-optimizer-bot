import time
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

# own imports
from schemas import AgentState
from agents.agents import (
    code_analyzer_agent,
    code_measurer_agent,
    code_improver_agent,
    final_report_agent,
)

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


def analyze_code_f(state: AgentState):
    return code_analyzer_agent(state, llm)


def measure_code_f(state: AgentState):
    return code_measurer_agent(state)


def improve_code_f(state: AgentState):
    return code_improver_agent(state, llm)


def final_report_f(state: AgentState):
    return final_report_agent(state, llm)


# Nodes
workflow.add_node("analyzer", analyze_code_f)
workflow.add_node("measurer", measure_code_f)
workflow.add_node("improver", improve_code_f)
workflow.add_node("report", final_report_f)

# Edges
workflow.add_edge("analyzer", "measurer")


def improve(state: AgentState):
    if state["iteration"] < 3:
        return "improver"
    else:
        return "report"


workflow.add_conditional_edges("measurer", improve)
workflow.add_edge("improver", "measurer")
workflow.add_edge("report", END)

# Set entry point
workflow.set_entry_point("analyzer")

# Build the graph
app = workflow.compile()

optimize_me = """def find_top_students(students, grades):
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

optimize_me2 = """
function findTopStudents(students, grades) {
    // Combine student names with their grades
    let studentGrades = [];
    for (let i = 0; i < students.length; i++) {
        studentGrades.push([students[i], grades[i]]);
    }

    // Sort students by their grades in descending order
    for (let i = 0; i < studentGrades.length; i++) {
        for (let j = i + 1; j < studentGrades.length; j++) {
            if (studentGrades[i][1] < studentGrades[j][1]) {
                [studentGrades[i], studentGrades[j]] = [studentGrades[j], studentGrades[i]];
            }
        }
    }

    // Return the top 3 students
    return studentGrades.slice(0, 3);
}

let students = ["Alice", "Bob", "Charlie", "David", "Eve"];
let grades = [85, 92, 88, 91, 76];

let topStudents = findTopStudents(students, grades);
console.log(topStudents);
"""

res = app.invoke(
    {
        "messages": [
            HumanMessage(content=optimize_me2),
        ],
        "original_code": optimize_me2,
        "iteration": 0,
    }
)

print("VALMIS :)")
