from fastapi import FastAPI
import logging

from app.graph.state import ResearchState
from app.graph.workflow import build_workflow_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/research-topic")
async def research_topic(topic: str):
    """Endpoint to research a given topic."""
    
    if not topic or not topic.strip():
        return {"error": "Topic cannot be empty"}
    
    logger.info(f"Starting research workflow for topic: {topic}")
    
    state = ResearchState(research_topic=topic)
    workflow_graph = await build_workflow_graph()

    try:
        result = [r async for r in workflow_graph.astream(state)]
        logger.info(f"Workflow completed successfully for topic: {topic}")
        return result
    except Exception as e:
        logger.error(f"Error during workflow execution: {e}")
        return {"error": str(e)}