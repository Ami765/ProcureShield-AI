"""
agents/data_extractor.py — Agent 1: Data Extractor
Pulls structured line-items (payment terms, liability caps, SLA clauses, etc.)
from raw contract text before the compliance pass.
"""

from langchain_core.messages import HumanMessage
from agents.state import AgentState


EXTRACTION_PROMPT = """
You are a senior contract analyst specialising in enterprise procurement documents.

Read the contract text below and extract the following structured information:

1. **Vendor Name** – if mentioned
2. **Payment Terms** – e.g. Net-30, Net-60, upfront payment required, etc.
3. **Liability Cap** – maximum dollar amount the vendor accepts liability for
4. **Indemnification Clauses** – who indemnifies whom and under what conditions
5. **Data Security / Compliance** – any GDPR, SOC2, ISO 27001, HIPAA references
6. **Auto-Renewal Terms** – notice period required to cancel
7. **Governing Law** – jurisdiction specified
8. **SLA / Service Levels** – uptime guarantees, response times
9. **Termination Clauses** – conditions under which either party can exit
10. **Any other notable clauses** – flag anything unusual

Format each item as a clear bullet point. If a field is not mentioned, write "Not specified."

CONTRACT TEXT:
{contract_text}
"""


def data_extractor(state: AgentState, llm) -> AgentState:
    """Agent 1 — extract structured items from raw contract text."""
    prompt = EXTRACTION_PROMPT.format(contract_text=state["contract_text"])
    response = llm.invoke([HumanMessage(content=prompt)])

    # Try to pull vendor name out of the extraction for later use
    vendor_name = None
    for line in response.content.splitlines():
        if "vendor name" in line.lower() and "not specified" not in line.lower():
            parts = line.split(":", 1)
            if len(parts) == 2:
                vendor_name = parts[1].strip(" *")
                break

    return {
        **state,
        "extracted_items": response.content,
        "vendor_name": vendor_name or "the vendor",
    }
