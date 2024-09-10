from schemas import AgentState, CodeOptimizationSuggestion
from prompts.prompts import CODE_OPTIMIZATION_SUGGESTION_PROMPT


def agent(state: AgentState, llm) -> AgentState:
    structured_llm = llm.with_structured_output(CodeOptimizationSuggestion)
    prompt = CODE_OPTIMIZATION_SUGGESTION_PROMPT.format(code=state["code"])
    res = structured_llm.invoke(prompt)
    print("\nTÄÄ STATEEN:")
    print(res.run_command)
    state["code_execution_command"] = res.run_command
    return state
