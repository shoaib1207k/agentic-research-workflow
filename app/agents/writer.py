import logging

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.graph.state import ResearchState

logger = logging.getLogger(__name__)

class WriterNode:
    def __init__(self):
        self.chat = ChatOllama(model="mistral", temperature=0)

    async def __call__(self, state: ResearchState):

        summary = state.summary
        research_topic = state.research_topic

        if state.is_passed_by_critic == False:
            messages = [
                SystemMessage(content="You are a helpful writing assistant."),
                HumanMessage(content=f"""
                        Based on the research topic : '{research_topic}' and 
                        provided summary: '{summary}' and critique provided: '{state.critic_results}', rewrite a comprehensive article on the topic 
                        covering all the key points.
                    """)
            ]

        else:
            messages = [
                SystemMessage(content="You are a helpful writing assistant."),
                HumanMessage(content=f"""
                        Based on the research topic : '{research_topic}' and 
                        provided summary: '{summary}', write a comprehensive article on the topic 
                        covering all the key points.
                    """)
            ]

        response = self.chat.invoke(messages)
        state.writing_results = response.content
        state.is_written = True
        
        logger.info(f"Writing completed. Article length: {len(state.writing_results)} characters")

        return {"writing_results": state.writing_results}