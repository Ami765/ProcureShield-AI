"""
app.py — ProcureShield AI | Streamlit Frontend
Multi-agent enterprise procurement document reviewer.
"""

import streamlit as st
import time
import os
from pathlib import Path

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="ProcureShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
[data-testid="stAppViewContainer"] {
    background: #0d1117;
    color: #e6edf3;
}
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

/* Typography */
h1 { font-size: 2rem !important; font-weight: 700 !important; }
h2 { font-size: 1.3rem !important; color: #58a6ff !important; }
h3 { font-size: 1.05rem !important; color: #79c0ff !important; }

/* Agent step cards */
.agent-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.agent-card.active { border-color: #58a6ff; }
.agent-card.done   { border-color: #3fb950; }

/* Risk badge */
.badge-high   { background:#da3633; color:#fff; padding:2px 10px; border-radius:12px; font-size:.8rem; }
.badge-medium { background:#d29922; color:#fff; padding:2px 10px; border-radius:12px; font-size:.8rem; }
.badge-low    { background:#3fb950; color:#fff; padding:2px 10px; border-radius:12px; font-size:.8rem; }

/* Buttons */
.stButton>button {
    background: #238636;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: .6rem 1.8rem;
    width: 100%;
}
.stButton>button:hover { background: #2ea043; }

/* Text areas */
.stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .85rem !important;
}

/* Tabs */
[data-testid="stTab"] { color: #8b949e; }
button[aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }

/* Info / success / error boxes */
.stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────
def load_sample_contract() -> str:
    sample_path = Path(__file__).parent / "sample_data" / "sample_contract.txt"
    if sample_path.exists():
        return sample_path.read_text()
    return ""


def parse_risk_score(risk_report: str) -> tuple[str, str]:
    """Return (score_label, css_class) from risk report text."""
    text = risk_report.upper()
    if "OVERALL RISK SCORE" in text:
        if "HIGH" in text.split("OVERALL RISK SCORE")[-1]:
            return "HIGH", "badge-high"
        elif "MEDIUM" in text.split("OVERALL RISK SCORE")[-1]:
            return "MEDIUM", "badge-medium"
    return "LOW", "badge-low"


# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ ProcureShield AI")
    st.markdown("*Enterprise Procurement Reviewer*")
    st.divider()

    st.markdown("### 🤖 Agent Pipeline")
    st.markdown("""
    1. **Data Extractor** — parses clauses  
    2. **Compliance Auditor** — flags risks  
    3. **Reply Automator** — drafts email  
    """)
    st.divider()

    st.markdown("### ⚙️ Configuration")
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza…  (or set in .env)",
        help="Get a free key at aistudio.google.com/apikey",
    )
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    model_choice = st.selectbox(
        "Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=0,
    )
    os.environ["GEMINI_MODEL"] = model_choice
    st.caption("🆓 Gemini free tier — no billing required")

    st.divider()
    st.caption("Agents League Hackathon — ProcureShield AI v1.0")


# ── Main Header ─────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown("# 🛡️ ProcureShield AI")
    st.markdown("#### Autonomous Multi-Agent Procurement Document Reviewer")
with col_badge:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<span style="background:#1f6feb;color:#fff;padding:4px 12px;border-radius:16px;font-size:.8rem;">Hackathon Build</span>',
        unsafe_allow_html=True,
    )

st.divider()

# ── Input Section ───────────────────────────────────────────────────────────
st.markdown("## 📄 Input Contract")

input_tab1, input_tab2 = st.tabs(["✏️  Paste Text", "📁  Upload File"])

contract_text = ""

with input_tab1:
    col_area, col_sample = st.columns([5, 1])
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load Sample", use_container_width=True):
            st.session_state["sample_loaded"] = True
    with col_area:
        default_val = load_sample_contract() if st.session_state.get("sample_loaded") else ""
        pasted_text = st.text_area(
            "Paste vendor contract clauses below:",
            height=240,
            value=default_val,
            placeholder="Paste contract text here, or click 'Load Sample' to use a demo contract…",
            label_visibility="collapsed",
        )
    if pasted_text.strip():
        contract_text = pasted_text.strip()

with input_tab2:
    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX contract file",
        type=["pdf", "docx", "doc", "txt"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        from utils.document_parser import parse_uploaded_file
        with st.spinner("Extracting text from document…"):
            file_bytes = uploaded_file.read()
            contract_text = parse_uploaded_file(uploaded_file.name, file_bytes)
        st.success(f"✅ Extracted {len(contract_text):,} characters from **{uploaded_file.name}**")
        with st.expander("Preview extracted text"):
            st.text(contract_text[:3000] + ("…" if len(contract_text) > 3000 else ""))

st.divider()

# ── Run Button ───────────────────────────────────────────────────────────────
run_col, _ = st.columns([2, 3])
with run_col:
    run_clicked = st.button("🚀 Run Multi-Agent Review", use_container_width=True)

# ── Pipeline Execution ───────────────────────────────────────────────────────
if run_clicked:
    if not contract_text:
        st.error("Please paste contract text or upload a file before running.")
        st.stop()

    # Validate API key
    try:
        import config
        config.get_gemini_key()
    except EnvironmentError as e:
        st.error(str(e))
        st.stop()

    # Build pipeline (imported here to avoid startup errors if key missing)
    from pipeline import build_pipeline

    st.markdown("## ⚙️ Agent Execution")

    # Agent status placeholders
    a1_status = st.empty()
    a2_status = st.empty()
    a3_status = st.empty()

    def render_card(placeholder, icon, title, status, css_class="agent-card"):
        placeholder.markdown(
            f'<div class="{css_class}">'
            f'<b>{icon} {title}</b> &nbsp; {status}'
            f'</div>',
            unsafe_allow_html=True,
        )

    render_card(a1_status, "1️⃣", "Data Extractor",    "⏳ Waiting…")
    render_card(a2_status, "2️⃣", "Compliance Auditor","⏳ Waiting…")
    render_card(a3_status, "3️⃣", "Reply Automator",   "⏳ Waiting…")

    try:
        pipeline_app = build_pipeline()

        # ── Agent 1 ───────────────────────────────────────────────────────
        render_card(a1_status, "1️⃣", "Data Extractor", "🔄 Extracting clauses…", "agent-card active")
        t0 = time.time()

        # Stream through pipeline step by step
        state_after_extract = None
        for event in pipeline_app.stream(
            {"contract_text": contract_text, "extracted_items": None,
             "risk_report": None, "email_draft": None, "vendor_name": None}
        ):
            if "extractor" in event:
                state_after_extract = event["extractor"]
                render_card(a1_status, "1️⃣", "Data Extractor",
                            f"✅ Done ({time.time()-t0:.1f}s)", "agent-card done")
            elif "auditor" in event:
                render_card(a2_status, "2️⃣", "Compliance Auditor",
                            "🔄 Auditing against company standards…", "agent-card active")
            elif "automator" in event:
                render_card(a2_status, "2️⃣", "Compliance Auditor",
                            f"✅ Done", "agent-card done")
                render_card(a3_status, "3️⃣", "Reply Automator",
                            "🔄 Drafting negotiation email…", "agent-card active")

        # Final state
        final_state = pipeline_app.invoke(
            {"contract_text": contract_text, "extracted_items": None,
             "risk_report": None, "email_draft": None, "vendor_name": None}
        )
        render_card(a3_status, "3️⃣", "Reply Automator", "✅ Done", "agent-card done")

    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.stop()

    st.divider()

    # ── Results ─────────────────────────────────────────────────────────────
    st.markdown("## 📊 Results")

    # Risk score banner
    risk_label, risk_css = parse_risk_score(final_state.get("risk_report", ""))
    vendor = final_state.get("vendor_name", "Unknown Vendor")
    st.markdown(
        f'**Vendor:** {vendor} &nbsp;&nbsp; '
        f'**Overall Risk:** <span class="{risk_css}">{risk_label}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    res_tab1, res_tab2, res_tab3 = st.tabs([
        "📋 Extracted Items", "🔍 Risk Report", "✉️ Negotiation Email"
    ])

    with res_tab1:
        st.markdown("### Agent 1 — Extracted Contract Items")
        st.markdown(final_state.get("extracted_items", "No data."))

    with res_tab2:
        st.markdown("### Agent 2 — Compliance Risk Report")
        risk_md = final_state.get("risk_report", "No report generated.")
        st.markdown(risk_md)

    with res_tab3:
        st.markdown("### Agent 3 — Automated Negotiation Email")
        email = final_state.get("email_draft", "No email generated.")
        st.markdown(email)
        st.divider()
        if st.button("📋 Copy Email to Clipboard"):
            st.code(email, language="text")
            st.info("Select all text above and copy (Ctrl+A / Cmd+A → Ctrl+C / Cmd+C)")

    # ── Download full report ─────────────────────────────────────────────────
    st.divider()
    report_md = f"""# ProcureShield AI — Procurement Review Report

**Vendor:** {vendor}  
**Overall Risk:** {risk_label}

---

## Extracted Contract Items

{final_state.get("extracted_items", "")}

---

## Compliance Risk Report

{final_state.get("risk_report", "")}

---

## Negotiation Email Draft

{final_state.get("email_draft", "")}
"""
    st.download_button(
        label="⬇️  Download Full Report (.md)",
        data=report_md,
        file_name=f"procureshield_report_{vendor.replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=False,
    )
