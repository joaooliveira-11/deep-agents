from typing import NotRequired, Annotated, Literal

from langchain.agents import AgentState
from typing_extensions import TypedDict

from src.utils import file_reducer

class Todo(TypedDict):
    """
    A structured task item for tracking progress through complex workflows.

    Attributes:
        content: Short, specific description of the task
        status: Current state - pending, in_progress, or completed
    """
    content: str
    status: Literal["pending", "in_progress", "completed"]

class DeepAgentState(AgentState):
    """
    Extended agent state that includes task tracking and virtual file system.
    Inherits from LangChain's AgentState and adds:
    - todos: List of Todo items for task planning and progress tracking
    - files: Virtual file system stored as dict mapping filenames to content
    """

    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]