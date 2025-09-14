from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from app.graph.state import ResearchState

class CriticNode:
    def __init__(self):
        self.chat = ChatOllama(model="mistral", temperature=0)

    async def __call__(self, state: ResearchState):

        writing_results = state.writing_results
        research_topic = state.research_topic

        messages = [
            SystemMessage(content="You are a helpful research article critic assistant."),
            HumanMessage(content=f"""
            You are a research article critic. 
            Critique the provided article for the following aspects:
            1. Coherence - Good/Bad/Needs Improvement
            2. Completeness - Good/Bad/Needs Improvement
            3. Accuracy - Good/Bad/Needs Improvement

            If any aspect is 'Needs Improvement' or 'Bad', set the verdict to 'Fail'. Otherwise, set it to 'Pass'.

            Respond in this exact format:
            Coherence: <Good/Bad/Needs Improvement>
            Completeness: <Good/Bad/Needs Improvement>
            Accuracy: <Good/Bad/Needs Improvement>
            Verdict: <Pass/Fail>

            Do not add any extra explanation.
            Research Topic: '{research_topic}'
            Article: '{writing_results}'
            """)
        ]

        response = self.chat.invoke(messages)
        state.critic_results = response.content
        state.is_criticized = True

        next_message = [
        SystemMessage(content="You are a workflow controller for a research article process."),
        HumanMessage(content=f"""
            Critique: '{response.content}'
            If the Verdict is 'Pass', respond ONLY with 'end'.
            If the Verdict is 'Fail', respond ONLY with one of: 'research', 'summarize', or 'write' based on critic results.
            Do not add any explanation. Respond with a single word.
        """)
    ]

        state.next_step = self.chat.invoke(next_message).content.strip().lower()
        state.is_passed_by_critic = "pass" in response.content.lower() and state.next_step == "end"

        print("*"*80)
        print("Critique Results:", state.critic_results)

        return { "critic_results": state.critic_results, "is_passed_by_critic": state.is_passed_by_critic, "next_step": state.next_step }