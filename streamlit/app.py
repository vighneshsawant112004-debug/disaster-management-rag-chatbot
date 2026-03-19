"""
app.py - DisasterAI Streamlit Frontend
"""

import streamlit as st
import traceback

st.set_page_config(
    page_title="DisasterAI · Emergency Guidance",
    page_icon="🆘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@300;400;600;700&family=Barlow+Condensed:wght@700;800&display=swap');

:root {
    --bg-void:     #080c10;
    --bg-card:     #0d1117;
    --bg-input:    #131920;
    --border:      #1e2d3d;
    --accent-red:  #ff2e2e;
    --accent-amber:#ffaa00;
    --accent-teal: #00d4aa;
    --text-primary:#e8edf2;
    --text-muted:  #6a7f94;
    --user-bubble: #0a2a4a;
    --ai-bubble:   #0d1f0f;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
    background: var(--bg-void) !important;
    color: var(--text-primary) !important;
    font-family: 'Barlow', sans-serif !important;
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

.block-container { padding: 1.5rem 2rem 6rem !important; max-width: 920px !important; }

.disaster-header {
    display: flex; align-items: center; gap: 16px;
    padding: 20px 0 8px;
    border-bottom: 2px solid var(--accent-red);
    margin-bottom: 8px;
}
.disaster-header .logo {
    font-size: 2.6rem; line-height: 1;
    animation: pulse-red 2.4s ease-in-out infinite;
}
@keyframes pulse-red {
    0%,100% { filter: drop-shadow(0 0 8px rgba(255,46,46,0.5)); }
    50%      { filter: drop-shadow(0 0 20px rgba(255,46,46,0.9)); }
}
.disaster-header h1 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2.4rem !important; font-weight: 800 !important;
    letter-spacing: 0.08em !important; color: var(--accent-red) !important;
    margin: 0 !important; padding: 0 !important;
    text-transform: uppercase; line-height: 1;
}
.disaster-header p {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem; color: var(--text-muted);
    margin: 4px 0 0; letter-spacing: 0.12em; text-transform: uppercase;
}

.status-bar {
    display: flex; align-items: center; gap: 12px;
    padding: 6px 14px; background: #0a0f14;
    border: 1px solid var(--border); border-radius: 6px; margin-bottom: 20px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.72rem; color: var(--text-muted);
}
.status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.3; } }

/* ── Chat layout ── */
.chat-block { margin-bottom: 18px; }

.user-row {
    display: flex; justify-content: flex-end;
    align-items: flex-start; gap: 10px; margin-bottom: 6px;
}
.user-avatar {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    background: #0e2040; border: 1px solid #1e4080;
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
}
.user-bubble {
    background: #0a2a4a; border: 1px solid #1e4080;
    border-radius: 14px; border-top-right-radius: 3px;
    padding: 10px 16px; max-width: 70%;
    color: #c8dff8; font-size: 0.95rem; line-height: 1.6;
}

.ai-row {
    display: flex; justify-content: flex-start;
    align-items: flex-start; gap: 10px; margin-bottom: 4px;
}
.ai-avatar {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    background: #0a2010; border: 1px solid #0e4020;
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
    box-shadow: 0 0 8px rgba(0,212,170,0.2);
}
.mode-badge {
    display: inline-block; font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.1em;
    padding: 2px 8px; border-radius: 3px; margin-bottom: 10px; text-transform: uppercase;
}
.mode-badge.rag      { background:#003322; color:#00d4aa; border:1px solid #005533; }
.mode-badge.fallback { background:#2a1a00; color:#ffaa00; border:1px solid #553300; }

/* ── Markdown rendering inside AI answers ── */
.ai-answer { padding: 2px 0 8px 44px; }
.ai-answer p  { color: #e8edf2 !important; font-size: 0.95rem !important; line-height: 1.75 !important; margin-bottom: 8px !important; }
.ai-answer ul { padding-left: 22px !important; margin: 4px 0 12px !important; }
.ai-answer ol { padding-left: 24px !important; margin: 4px 0 12px !important; }
.ai-answer li { color: #e8edf2 !important; font-size: 0.95rem !important; line-height: 1.7 !important; margin-bottom: 8px !important; }
.ai-answer strong { color: #ffaa00 !important; font-weight: 600 !important; }
.ai-answer h1, .ai-answer h2, .ai-answer h3 {
    color: #00d4aa !important; font-size: 1rem !important;
    font-weight: 700 !important; margin: 14px 0 6px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important; border: 1px solid var(--border) !important;
    color: var(--text-primary) !important; font-family: 'Barlow', sans-serif !important;
    border-radius: 6px !important; transition: all 0.2s;
}
.stButton > button:hover { border-color: var(--accent-red) !important; color: var(--accent-red) !important; }

/* ── Sidebar ── */
.sidebar-section {
    background: #0a0f14; border: 1px solid var(--border);
    border-radius: 8px; padding: 14px; margin-bottom: 14px;
}
.sidebar-section h4 {
    font-family: 'Barlow Condensed', sans-serif; font-size: 0.85rem;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--accent-amber) !important; margin: 0 0 10px !important;
}
.sidebar-section p, .sidebar-section li { font-size: 0.8rem; color: var(--text-muted) !important; line-height: 1.5; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = None
    if "pipeline_error" not in st.session_state:
        st.session_state.pipeline_error = None
    if "pipeline_loaded" not in st.session_state:
        st.session_state.pipeline_loaded = False


# ── Pipeline loader ───────────────────────────────────────────────────────────
def load_pipeline_once():
    if st.session_state.pipeline_loaded:
        return
    with st.spinner("⚙️ Loading DisasterAI... (first run may take 2-3 mins)"):
        try:
            from rag_pipeline import DisasterAIPipeline
            st.session_state.pipeline = DisasterAIPipeline()
            st.session_state.pipeline_error = None
        except Exception as e:
            st.session_state.pipeline = None
            st.session_state.pipeline_error = f"{type(e).__name__}: {e}\n\n{traceback.format_exc()}"
    st.session_state.pipeline_loaded = True


# ── Render helpers ────────────────────────────────────────────────────────────
QUICK_QUESTIONS = [
    "🌊 What to do during a flood?",
    "🏚️ Steps during an earthquake?",
    "🌀 How to prepare for a cyclone?",
    "🔥 Fire emergency actions?",
    "🎒 Emergency kit essentials?",
]


def render_header():
    st.markdown("""
    <div class="disaster-header">
        <span class="logo">🆘</span>
        <div>
            <h1>DisasterAI</h1>
            <p>Emergency Guidance · RAG-Powered · Always Calm</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_status(ok: bool):
    color  = "#00d4aa" if ok else "#ff2e2e"
    status = "SYSTEM ONLINE · DOCUMENTS INDEXED" if ok else "SYSTEM OFFLINE · CHECK CONFIGURATION"
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot" style="background:{color};box-shadow:0 0 6px {color};"></div>
        <span>{status}</span>
    </div>
    """, unsafe_allow_html=True)


def render_user_message(content: str):
    """Render a plain-text user bubble — no HTML parsing of content."""
    st.markdown(f"""
    <div class="user-row">
        <div class="user-bubble">{st.html if False else ""}{content}</div>
        <div class="user-avatar">👤</div>
    </div>
    """, unsafe_allow_html=True)


def render_ai_message(content: str, mode: str = ""):
    """Render AI response: badge via HTML, content via st.markdown for proper formatting."""
    badge = ""
    if mode == "rag":
        badge = '<span class="mode-badge rag">📚 Document-Grounded</span>'
    elif mode == "fallback":
        badge = '<span class="mode-badge fallback">⚡ AI General Knowledge</span>'

    # Avatar + badge row
    st.markdown(f"""
    <div class="ai-row">
        <div class="ai-avatar">🤖</div>
        <div>{badge}</div>
    </div>
    """, unsafe_allow_html=True)

    # Content rendered as markdown (bullets, bold, headers all work)
    with st.container():
        st.markdown(
            f'<div class="ai-answer">',
            unsafe_allow_html=True
        )
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar(pipeline):
    with st.sidebar:
        st.markdown("""
        <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.4rem;
                    font-weight:800;letter-spacing:0.1em;color:#ff2e2e;
                    text-transform:uppercase;padding:8px 0 16px;">
            🆘 DisasterAI
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-section">
            <h4>About</h4>
            <p>Instant, actionable safety guidance using official disaster management
            documents + free AI (LLaMA-3 via Groq).</p>
        </div>
        <div class="sidebar-section">
            <h4>Disasters Covered</h4>
            <ul>
                <li>🌊 Floods &amp; Tsunamis</li>
                <li>🏚️ Earthquakes</li>
                <li>🌀 Cyclones &amp; Hurricanes</li>
                <li>🔥 Fires &amp; Wildfires</li>
                <li>⛰️ Landslides</li>
                <li>🐍 Snake Bites &amp; First Aid</li>
                <li>🏥 Survival &amp; Emergency Kits</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if pipeline:
            try:
                n_docs = pipeline.vectorstore.index.ntotal if pipeline.vectorstore else 0
                mode_label = "RAG + AI Fallback" if pipeline.vectorstore else "AI-Only Mode"
                st.markdown(f"""
                <div class="sidebar-section">
                    <h4>System Info</h4>
                    <p>📄 Chunks indexed: <strong style="color:#00d4aa">{n_docs}</strong></p>
                    <p>🔍 Embeddings: all-MiniLM-L6-v2</p>
                    <p>🧠 LLM: LLaMA-3.3-70b (Groq)</p>
                    <p>⚡ Mode: <strong style="color:#ffaa00">{mode_label}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            except Exception:
                pass

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        if pipeline and st.button("🔄 Rebuild Index", use_container_width=True):
            st.session_state.pipeline_loaded = False
            st.session_state.pipeline = None
            st.rerun()

        st.markdown("""
        <div class="sidebar-section" style="margin-top:14px">
            <h4>⚠️ Disclaimer</h4>
            <p>Always follow instructions from local emergency authorities during an actual disaster.</p>
        </div>
        """, unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    init_session()
    render_header()
    load_pipeline_once()

    pipeline = st.session_state.pipeline
    error    = st.session_state.pipeline_error

    render_status(ok=pipeline is not None)
    render_sidebar(pipeline)

    if error:
        st.error("🚨 DisasterAI failed to start.", icon="🚨")
        with st.expander("🔍 Error Details", expanded=True):
            st.code(error, language="python")
        st.info(
            "**Common fixes:**\n"
            "- Set `GROQ_API_KEY` in `.env`\n"
            "- Delete `streamlit/faiss_index/` folder and restart\n"
            "- Check terminal for full traceback",
            icon="📋",
        )
        return

    if pipeline and pipeline.mode == "fallback-only":
        st.warning(
            "⚡ **No PDFs found** — Running in AI-only mode. "
            "DisasterAI will answer all questions using built-in AI knowledge. "
            "Add PDFs to `data/` folder and restart for document-grounded answers.",
            icon="⚡",
        )

    # Welcome screen
    if not st.session_state.messages:
        st.markdown("""
        <div style="background:#0d1117;border:1px solid #1e2d3d;border-radius:10px;
                    padding:20px 24px;margin-bottom:20px;">
            <p style="font-family:'Barlow Condensed',sans-serif;font-size:1.15rem;
                      font-weight:700;color:#ffaa00;margin:0 0 8px;">
                👋 Welcome to DisasterAI
            </p>
            <p style="font-size:0.9rem;color:#6a7f94;margin:0;line-height:1.6;">
                Ask me anything about <strong style="color:#e8edf2">floods, earthquakes,
                cyclones, fires, first aid, survival</strong> or any emergency.
                I'll give detailed, structured, point-by-point guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p style="font-size:0.78rem;color:#6a7f94;margin-bottom:6px;'
                    'font-family:\'Share Tech Mono\',monospace;letter-spacing:0.1em;">'
                    'QUICK QUESTIONS</p>', unsafe_allow_html=True)

        cols = st.columns(len(QUICK_QUESTIONS))
        for col, q in zip(cols, QUICK_QUESTIONS):
            with col:
                if st.button(q, key=f"chip_{q}", use_container_width=True):
                    clean_q = q.split(" ", 1)[1]
                    st.session_state.messages.append({"role": "user", "content": clean_q})
                    st.rerun()

    # Render full chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_message(msg["content"])
        else:
            render_ai_message(msg["content"], msg.get("mode", ""))

    # Input box
    user_input = st.chat_input("Ask anything about disasters, safety, first aid, survival...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_user_message(user_input)

        with st.spinner("🔍 Searching documents and generating guidance…"):
            try:
                result = pipeline.ask(
                    question=user_input,
                    chat_history=st.session_state.messages[:-1],
                )
                answer = result["answer"]
                mode   = result["mode"]
            except Exception as exc:
                answer = f"**⚠️ Error:** {exc}\n\nPlease check the terminal for details."
                mode   = ""

        st.session_state.messages.append({"role": "ai", "content": answer, "mode": mode})
        render_ai_message(answer, mode)
        st.rerun()


if __name__ == "__main__":
    main()