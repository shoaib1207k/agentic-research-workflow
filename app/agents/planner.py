import json
import logging

from app.graph.state import ResearchState
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import END

logger = logging.getLogger(__name__)


class PlannerNode:
    def __init__(self):
        self.chat = ChatOllama(model="mistral", temperature=0)

    async def __call__(self, state: ResearchState):

        research_topic = state.research_topic

        messages = [
            SystemMessage(content="You are a research planner assistant."),
            HumanMessage(content=f"""
                        Based on that research topic: '{research_topic}', provide complexity level and token estimates. 
                        Simple: 300 tokens, Medium: 500 tokens, Large: 800 tokens.
                        Return the response in JSON format with keys 'complexity' and 'token_estimate'.
                    """)
        ]

        response = self.chat.invoke(messages)
        
        # Parse the response content as JSON with error handling
        try:
            response_data = json.loads(response.content)
            complexity = response_data.get("complexity", "Medium")
            token_estimate = response_data.get("token_estimate", 500)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            logger.error(f"Response content: {response.content}")
            # Fallback to default values
            complexity = "Medium"
            token_estimate = 500

        logger.info(f"Complexity: {complexity}, Token Estimate: {token_estimate}")

        return {"research_topic": research_topic, "research_complexity": complexity, "token_estimate": token_estimate}
    

    async def plan_next(self, state: ResearchState):
        """Route to the next node based on critic feedback."""
        if state.is_passed_by_critic:
            return END
        elif state.next_step == "research":
            return "researcher"
        elif state.next_step == "summarize":
            return "summarizer"
        elif state.next_step == "write":
            return "writer"
        else:
            return END