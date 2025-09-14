from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.graph.state import ResearchState


class ResearchNode:
    def __init__(self):
        self.chat = ChatOllama(model="mistral", temperature=0, max_tokens=1000)


    async def __call__(self, state: ResearchState):
        research_topic = state.research_topic

        if state.is_passed_by_critic == False:
            messages = [
                SystemMessage(content="You are a research assistant."),
                HumanMessage(content=f"""
                    Based on the research topic: '{research_topic}' and critique provided: '{state.critic_results}', 
                    provide a research on this topic in bullet points.
                    Limit the response based on the complexity level provided.
                    Compexity level: '{state.research_complexity}'.
                    Token limit: '{state.token_estimate}'
                    """)
            ]
        
        else:
            messages = [
                SystemMessage(content="You are a research assistant."),
                HumanMessage(content=f"""
                    Based on the research topic: '{research_topic}', 
                    provide a research on this topic in bullet points.
                    Limit the response based on the complexity level provided.
                    Compexity level: '{state.research_complexity}'.
                    Token limit: '{state.token_estimate}'
                    """)
            ]

        response = self.chat.invoke(messages)

        state.research_results = response.content

        print("Research Results:", state.research_results)

        state.is_researched = True 

        return {"research_results": state.research_results, "is_researched": state.is_researched}
