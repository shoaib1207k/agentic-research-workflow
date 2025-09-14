from langgraph.graph import StateGraph, START, END
from .state import ResearchState
from app.agents.planner import PlannerNode
from app.agents.researcher import ResearchNode
from app.agents.summarizer import SummarizerNode
from app.agents.writer import WriterNode
from app.agents.critic import CriticNode

async def build_workflow_graph():
    workflow_graph = StateGraph(ResearchState)

    planner = PlannerNode()
    researcher = ResearchNode()
    summarizer = SummarizerNode()
    writer = WriterNode()
    critic = CriticNode()

    workflow_graph.add_node("planner", planner)
    workflow_graph.add_node("researcher", researcher)
    workflow_graph.add_node("summarizer", summarizer)
    workflow_graph.add_node("writer", writer)
    workflow_graph.add_node("critic", critic)


    workflow_graph.add_edge(START, "planner")
    workflow_graph.add_edge("planner", "researcher")
    workflow_graph.add_edge("researcher", "summarizer")
    workflow_graph.add_edge("summarizer", "writer")
    workflow_graph.add_edge("writer", "critic")
    workflow_graph.add_conditional_edges("critic", planner.plan_next)

    try:
        compiled_graph = workflow_graph.compile()
    except Exception as e:
        print("Error compiling workflow graph:", e)
        return None

    return compiled_graph

