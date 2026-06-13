"""
agents/compliance_auditor.py — Agent 2: Compliance Auditor
Cross-references extracted items against company procurement standards
and produces a prioritised risk report.
"""

from langchain_core.messages import HumanMessage
from agents.state import AgentState


# ── Internal company procurement standards (acts as the RAG "knowledge base") ──
COMPANY_STANDARDS = """
COMPANY PROCUREMENT STANDARDS (internal policy — treat as ground truth):

PAYMENT TERMS
  • Acceptable: Net-30 or better (Net-15, Net-7, immediate).
  • Risky: Net-60. Flag as MEDIUM risk.
  • Unacceptable: Net-90 or longer, or upfront full payment. Flag as HIGH risk.

LIABILITY
  • Minimum acceptable liability cap: $1,000,000.
  • Caps below $500,000 are HIGH risk.
  • Caps between $500,000–$999,999 are MEDIUM risk.
  • Unlimited liability exposure for the company is HIGH risk.

INDEMNIFICATION
  • Mutual indemnification is acceptable.
  • One-sided indemnification (vendor only indemnified by us) is HIGH risk.

DATA SECURITY & COMPLIANCE
  • Vendor must hold at least one: SOC 2 Type II, ISO 27001, or GDPR DPA.
  • Missing all certifications/agreements = HIGH risk.

AUTO-RENEWAL
  • Notice period of less than 30 days to cancel = MEDIUM risk.
  • No auto-renewal clause = acceptable.

GOVERNING LAW
  • Preferred: jurisdiction where our HQ operates.
  • Foreign jurisdiction (especially non-EU/US) = MEDIUM risk.

SLA / SERVICE LEVELS
  • Minimum acceptable uptime: 99.5%.
  • Below 99% = HIGH risk.
  • No SLA specified for critical services = MEDIUM risk.

TERMINATION
  • Vendor must allow termination for convenience with ≤ 30 days notice.
  • Lock-in periods > 12 months = MEDIUM risk.
"""

AUDIT_PROMPT = """
You are an Enterprise Compliance Officer conducting a procurement risk audit.

Use ONLY the company standards below to judge risk — do not apply personal legal opinions.

{standards}

EXTRACTED CONTRACT ITEMS:
{extracted_items}

ORIGINAL CONTRACT TEXT (for additional context):
{contract_text}

Produce a structured risk report with these exact sections:

## 🔴 HIGH RISK ITEMS
List each HIGH risk clause. For each: state the clause, why it violates policy, and the exact policy rule.

## 🟡 MEDIUM RISK ITEMS
List each MEDIUM risk clause with the same detail.

## 🟢 ACCEPTABLE / COMPLIANT ITEMS
List items that meet company standards.

## ⚠️ MISSING INFORMATION
List any required fields that were not found in the contract.

## 📊 OVERALL RISK SCORE
Rate overall risk: LOW / MEDIUM / HIGH and provide a one-sentence justification.
"""


def compliance_auditor(state: AgentState, llm) -> AgentState:
    """Agent 2 — audit extracted items against company procurement standards."""
    prompt = AUDIT_PROMPT.format(
        standards=COMPANY_STANDARDS,
        extracted_items=state.get("extracted_items", "No items extracted."),
        contract_text=state["contract_text"],
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "risk_report": response.content}
