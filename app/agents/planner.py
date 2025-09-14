
from app.graph.state import ResearchState
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import END
import json


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
        # parse the response content as json
        response_data = json.loads(response.content)
        complexity = response_data.get("complexity", "Unknown")
        token_estimate = response_data.get("token_estimate", 0)

        print("Complexity:", complexity)
        print("Token Estimate:", token_estimate)

        return {"research_topic": research_topic, "research_complexity": complexity, "token_estimate": token_estimate}
    

    async def plan_next(self, state: ResearchState):
        if state.is_passed_by_critic:
            return END
        elif state.critic_results == "research":
            return "researcher"
        elif state.critic_results == "summarize":
            return "summarizer"
        elif state.critic_results == "write":
            return "writer"
        else:
            return "planner"