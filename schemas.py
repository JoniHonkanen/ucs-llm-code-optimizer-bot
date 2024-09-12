from pydantic import BaseModel, Field
from typing import Optional, TypedDict, Union, List
from enum import Enum


class CodeImprovement(BaseModel):
    """
    Represents a specific improvement applied to a piece of code.
    """

    description: str = Field(
        description="A detailed explanation of the improvement and its purpose."
    )
    changes_summary: str = Field(
        description="Summary of the changes made to the original code as part of this improvement."
    )
    success: bool = Field(
        description="Indicates whether the improvement was successfully applied without errors."
    )
    complexity_reduction: float = Field(
        description="Reduction in time complexity or runtime performance, expressed as a factor (e.g., 0.5 means 50% reduction)."
    )
    updated_code: str = Field(
        description="The code after applying the improvement. Newlines should not be added explicitly using '\\n'."
    )
    run_time: Optional[float] = Field(
        None,
        description="This will be tested later, so it is not required to be filled in.",
    )
    test_description: str = Field(
        description="A concise note on what was optimized (e.g., algorithm change) to avoid repeating similar improvements."
    )
    run_command: str = Field(
        description="The full command to execute the code/function in a python subprocess"
    )


class OriginalCodeAnalyze(BaseModel):
    description: str = Field(description="Detailed description of the code.")
    actionable_suggestion: str = Field(
        description="The specific, actionable suggestion for optimizing the code."
    )
    complexity: str = Field(
        None,
        description="The complexity analysis of the code, including time and/or space complexity.",
    )
    run_command: str = Field(
        description="The full command to execute the code/function in a python subprocess"
    )


# Agents state
class AgentState(TypedDict):
    original_code: str
    original_run_time: float
    code_execution_command: str
    improved_code: CodeImprovement
    top_improvements: List[CodeImprovement]
    tested_improvements: List[str]
    messages: List[str]
    iteration: int
