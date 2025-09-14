from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.graph.state import ResearchState

class SummarizerNode:
    def __init__(self):
        self.chat = ChatOllama(model="mistral", temperature=0)

    async def __call__(self, state: ResearchState):

        research_results = state.research_results

        if state.is_passed_by_critic == False:
            messages = [
                SystemMessage(content="You are a helpful summarization assistant."),
                HumanMessage(content=f"""
                    Based on the research results: '{research_results}' and critique provided: '{state.critic_results}', 
                    resummarize the key points in concise manner. So it can be used for writing task.
                    """
                    )
            ]
        else:
             messages = [
            SystemMessage(content="You are a helpful summarization assistant."),
            HumanMessage(content=f"""
                Based on the research results: '{research_results}', 
                summarize the key points in concise manner. So it can be used for writing task.
                """
                )
        ]

       

        response = self.chat.invoke(messages)

        state.summary = response.content
        state.is_summarized = True
        print("Summary:", state.summary)


        return {"summary": state.summary, "is_summarized": state.is_summarized}

