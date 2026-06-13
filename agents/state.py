"""
agents/state.py — Shared state schema for the LangGraph pipeline.
"""

from typing import TypedDict, Optional


class AgentState(TypedDict):
    """
    Shared state object that flows through every agent node.

    Fields
    ------
    contract_text   : Raw contract text extracted from the uploaded document.
    extracted_items : Structured line-items pulled out by the Data Extractor.
    risk_report     : Flagged clause analysis produced by the Compliance Auditor.
    email_draft     : Negotiation email drafted by the Reply Automator.
    vendor_name     : Optional vendor name parsed from the document.
    """
    contract_text:   str
    extracted_items: Optional[str]
    risk_report:     Optional[str]
    email_draft:     Optional[str]
    vendor_name:     Optional[str]
