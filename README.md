# 🛡️ ProcureShield AI

**Autonomous Multi-Agent Enterprise Procurement Document Reviewer**  
*Agents League Hackathon Submission*

---

## What It Does

ProcureShield AI reviews inbound vendor contracts using a 3-agent LangGraph pipeline:

| Agent | Role |
|-------|------|
| **Agent 1 — Data Extractor** | Pulls payment terms, liability caps, SLA clauses, and 7+ other fields from raw contract text |
| **Agent 2 — Compliance Auditor** | Cross-references extracted items against company procurement standards and produces a prioritised risk report (HIGH / MEDIUM / LOW) |
| **Agent 3 — Reply Automator** | Drafts a professional negotiation email requesting amendments to all flagged clauses |

---

## Project Structure

```
procureshield_ai/
├── app.py                    ← Streamlit UI (entry point)
├── pipeline.py               ← LangGraph orchestration
├── config.py                 ← Credential loader
├── requirements.txt          ← Python dependencies
├── .env.example              ← Copy to .env and add your API key
│
├── agents/
│   ├── state.py              ← Shared AgentState TypedDict
│   ├── data_extractor.py     ← Agent 1
│   ├── compliance_auditor.py ← Agent 2
│   └── reply_automator.py    ← Agent 3
│
├── utils/
│   └── document_parser.py    ← PDF / DOCX text extraction
│
└── sample_data/
    └── sample_contract.txt   ← Demo contract with intentional violations
```

---

## Quick Start

### 1. Install dependencies

```bash
cd procureshield_ai
pip install -r requirements.txt
```

### 2. Add your API key

```bash
cp .env.example .env
# Open .env and replace "your-openai-api-key-here" with your real key
```

Or enter the key directly in the sidebar when the app is running.

### 3. Launch the app

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## Using Azure OpenAI Instead

Edit `.env` and fill in the Azure section:

```env
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01
```

Comment out `OPENAI_API_KEY` — the app auto-detects which provider to use.

---

## Supported Input Formats

| Format | Notes |
|--------|-------|
| **Paste text** | Any contract clauses pasted directly |
| **PDF** | Text-based PDFs (not scanned images) |
| **DOCX / DOC** | Microsoft Word documents |
| **TXT** | Plain text files |

---

## Company Procurement Standards (built-in)

The Compliance Auditor uses these rules (edit in `agents/compliance_auditor.py`):

| Area | Acceptable | HIGH Risk |
|------|-----------|-----------|
| Payment Terms | Net-30 or better | Net-90 or longer |
| Liability Cap | ≥ $1,000,000 | < $500,000 |
| Data Security | SOC2 / ISO27001 / GDPR DPA | None specified |
| Auto-Renewal Notice | ≥ 30 days | < 30 days |
| SLA Uptime | ≥ 99.5% | < 99% |
| Termination Lock-in | ≤ 12 months | > 12 months |

---

## Tech Stack

- **LangGraph** — Multi-agent state graph orchestration  
- **LangChain OpenAI** — LLM client (OpenAI or Azure OpenAI)  
- **Streamlit** — Interactive web UI  
- **PyPDF2** — PDF text extraction  
- **python-docx** — DOCX text extraction  
- **python-dotenv** — Environment variable management  

---

## License

MIT — free to use, modify, and extend.
