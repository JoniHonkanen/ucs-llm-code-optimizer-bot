import time
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

# own imports
from schemas import AgentState
from agents.agents import (
    code_analyzer_agent,
    code_measurer_agent,
    code_improver_agent,
    final_report_agent,
    fix_execution_agent,
)
from optimize_functions import (
    optimize_me,
    optimize_me2,
    optimize_me3,
    optimize_me4,
    optimize_me5,
    optimize_me6,
    optimize_me7,
    optimize_me8,
    optimize_me9,
    optimize_me10,
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


def fix_execution_agent_f(state: AgentState):
    return fix_execution_agent(state, llm)


# Nodes
workflow.add_node("analyzer", analyze_code_f)
workflow.add_node("measurer", measure_code_f)
workflow.add_node("fix_execution", fix_execution_agent_f)
workflow.add_node("improver", improve_code_f)
workflow.add_node("report", final_report_f)

# Edges
workflow.add_edge("analyzer", "measurer")


def combined_condition(state: AgentState):
    if state["original_execution_success"] and state["iteration"] < 3:
        return "improver"
    elif state["original_execution_success"]:
        return "report"
    else:
        return "fix_execution"


workflow.add_conditional_edges("measurer", combined_condition)
workflow.add_edge("fix_execution", "measurer")
workflow.add_edge("improver", "measurer")
workflow.add_edge("report", END)

# Set entry point
workflow.set_entry_point("analyzer")

# Build the graph
app = workflow.compile()

config = RunnableConfig(recursion_limit=50)
res = app.invoke(
    {
        "messages": [
            HumanMessage(content=optimize_me7),
        ],
        "original_code": optimize_me7,
        "iteration": 0,
    },
    config=config,
)

print("VALMIS :)")
