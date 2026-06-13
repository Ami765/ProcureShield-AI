"""
pipeline.py — LangGraph Multi-Agent Orchestration Pipeline
Powered by Google Gemini (free tier).
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

import config
from agents.state import AgentState
from agents.data_extractor import data_extractor
from agents.compliance_auditor import compliance_auditor
from agents.reply_automator import reply_automator


def _build_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=config.get_gemini_key(),
        temperature=0,
    )


def build_pipeline():
    llm = _build_llm()

    def node_extractor(state: AgentState):
        return data_extractor(state, llm)

    def node_auditor(state: AgentState):
        return compliance_auditor(state, llm)

    def node_automator(state: AgentState):
        return reply_automator(state, llm)

    graph = StateGraph(AgentState)
    graph.add_node("extractor",  node_extractor)
    graph.add_node("auditor",    node_auditor)
    graph.add_node("automator",  node_automator)

    graph.set_entry_point("extractor")
    graph.add_edge("extractor",  "auditor")
    graph.add_edge("auditor",    "automator")
    graph.add_edge("automator",  END)

    return graph.compile()
