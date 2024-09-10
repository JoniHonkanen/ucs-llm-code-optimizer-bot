from pydantic import BaseModel, Field
from typing import Optional, TypedDict, Union, List
from enum import Enum


# Agents state
class AgentState(TypedDict):
    messages: List[str]
    code: str
    code_execution_command: str


class ImpactLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class CodeOptimizationSuggestion(BaseModel):
    description: str = Field(
        description="Detailed description of the code optimization suggestion."
    )
    impact: Optional[ImpactLevel] = Field(
        None, description="The estimated impact of the optimization on the code."
    )
    actionable_suggestion: str = Field(
        description="The specific, actionable suggestion for optimizing the code."
    )
    category: Optional[str] = Field(
        None,
        description="The category of the suggestion (e.g., 'Performance', 'Memory', 'Readability').",
    )
    complexity: Optional[dict] = Field(
        None,
        description="The complexity analysis of the code, including time and/or space complexity.",
        example={"type": "Time Complexity", "before": "O(n^2)", "after": "O(n log n)"},
    )
    run_command: List[str] = Field(
        description="The command as a list to run the original code in a subprocess for any language. "
                    "Example for Python: ['python', '-c', '<code>'], for JavaScript: ['node', '<file.js>'], "
                    "for Java: ['java', '<file.class>'], for C: ['gcc', '<file.c>', '-o', 'output_file']"
    )
