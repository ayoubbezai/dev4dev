"""
Base tool with helper methods for CrewAI compatibility.
"""
from langchain.tools import BaseTool

# Add to_dict method to BaseTool for CrewAI compatibility
def _to_dict(self):
    """Convert a LangChain BaseTool to a dictionary for CrewAI compatibility."""
    return {
        "name": self.name,
        "description": self.description,
        "func": self._run
    }

BaseTool._to_dict = _to_dict