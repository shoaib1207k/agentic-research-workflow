from pydantic import BaseModel

class ResearchState(BaseModel):
    """
    Represents the state of a graph node or edge.
    """
    research_topic: str
    token_estimate: int = 0
    research_complexity: str = ""
    is_researched: bool = False
    research_results: str = ""
    is_summarized: bool = False
    summary: str = ""
    is_written: bool = False
    writing_results: str = ""
    is_criticized: bool = False
    is_passed_by_critic: bool = None
    critic_results: str = ""
    next_step: str = ""
    