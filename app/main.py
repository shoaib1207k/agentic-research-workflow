from fastapi import FastAPI
from app.graph.state import ResearchState
from app.graph.workflow import build_workflow_graph

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/research-topic")
async def research_topic(topic: str):
    """Endpoint to research a given topic."""

    state = ResearchState(research_topic=topic)


    workflow_graph = await build_workflow_graph()

    try:
        result = [r async for r in workflow_graph.astream(state)]
    except Exception as e:
        print(f"Error during workflow execution: {e}")
        return {"error": str(e)}


    return result