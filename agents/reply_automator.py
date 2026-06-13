"""
agents/reply_automator.py — Agent 3: Reply Automator
Drafts a professional vendor negotiation email based on the risk report.
"""

from langchain_core.messages import HumanMessage
from agents.state import AgentState


EMAIL_PROMPT = """
You are a Senior Enterprise Procurement Negotiator drafting a vendor response email.

Based on the compliance risk report below, write a professional, firm but respectful email
to {vendor_name} requesting amendments to the flagged contract clauses.

RISK REPORT:
{risk_report}

EMAIL REQUIREMENTS:
- Subject line included at the top prefixed with "Subject:"
- Open with appreciation for the partnership opportunity
- Reference each HIGH RISK item specifically — request exact amendments
- Reference MEDIUM RISK items — suggest preferred alternatives
- Do NOT mention the internal risk scoring system or company standards by name
- Close with a clear next-step (e.g. schedule a call, request revised draft within X days)
- Tone: professional, collaborative, firm but not adversarial
- Sign off as: Procurement Team, [Company Name]

Write the full email now.
"""


def reply_automator(state: AgentState, llm) -> AgentState:
    """Agent 3 — draft negotiation email from the risk report."""
    prompt = EMAIL_PROMPT.format(
        vendor_name=state.get("vendor_name", "the vendor"),
        risk_report=state.get("risk_report", "No risk report available."),
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "email_draft": response.content}
