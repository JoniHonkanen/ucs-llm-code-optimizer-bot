from pydantic import BaseModel, Field
from typing import Optional, TypedDict, Union, List
from enum import Enum


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
    file_extension: str = (
        Field(description="programming language extension for the code file"),
    )
    context_and_purpose: str = Field(
        description="A combined description of where the function is used and the reason for its existence or role in the system."
    )


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
        None,
        description="This will be tested later, so it is not required to be filled in.",
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


class FinalReport(BaseModel):
    """
    Represents the final report on the code optimization process.
    """

    best_improvement_description: str = Field(
        description="Description of why the chosen optimized code was selected, formatted as a comment for the specified programming language (e.g., '// for JavaScript, # for Python')."
    )
    selected_code: str = Field(
        description="The optimized code that was selected as the best improvement."
    )
    performance_gain: str = Field(
        description="The performance gain achieved with the selected code, formatted as a comment for the specified programming language (e.g., '// for JavaScript, # for Python')."
    )
    filename: str = Field(
        description="A good filename for the code, possibly reflecting the programming language."
    )
    purpose_consistency: bool = Field(
        description="Indicates whether the purpose of the original code has been preserved after optimization."
    )


class FixExecutionCommand(BaseModel):
    reason: str = Field(description="The reason why the code execution failed.")
    new_execution_command: str = Field(
        description="The new execution command to run the code successfully."
    )


# Agents state
class AgentState(TypedDict):
    orginal_analyze: OriginalCodeAnalyze
    original_code: str
    file_extension: str
    original_execution_success: bool
    original_run_time: float
    code_execution_command: str
    improved_code: CodeImprovement
    top_improvements: List[CodeImprovement]
    tested_improvements: List[str]
    messages: List[str]
    iteration: int
    final: FinalReport
