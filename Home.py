import streamlit as st
from auth import require_password

st.set_page_config(
    page_title="IP Toolbox",
    page_icon="📇",
    layout="wide"
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

require_password()


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap');

    .stApp {
        background-color: #14181F;
    }

    .block-container {
        max-width: 760px;
        padding-top: 4.5rem;
        padding-bottom: 4rem;
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .toolbox-wordmark {
        font-family: 'Fraunces', serif;
        font-size: 2.4rem;
        font-weight: 600;
        color: #F2EFE6;
        letter-spacing: -0.01em;
        margin-bottom: 0.4rem;
    }

    .toolbox-intro {
        font-size: 1.02rem;
        line-height: 1.6;
        color: #8B93A3;
        max-width: 52ch;
        margin-bottom: 2.6rem;
    }

    .registry-rule {
        border: none;
        border-top: 1px solid #2A313D;
        margin: 1.7rem 0;
    }

    .tool-name {
        font-family: 'Fraunces', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #F2EFE6;
        margin-bottom: 0.35rem;
    }

    .tool-status-live {
        font-size: 0.82rem;
        color: #B08D57;
        margin-left: 0.6rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .tool-status-pending {
        font-size: 0.82rem;
        color: #5C6472;
        margin-left: 0.6rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .tool-desc {
        font-size: 0.95rem;
        line-height: 1.55;
        color: #A7ADB8;
        max-width: 58ch;
    }

    .tool-desc-pending {
        font-size: 0.95rem;
        line-height: 1.55;
        color: #5C6472;
        max-width: 58ch;
        font-style: italic;
    }

    div[data-testid="stButton"] button {
        background: none;
        border: none;
        color: #B08D57;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        padding: 0;
        margin-top: 0.5rem;
        text-decoration: underline;
        text-underline-offset: 3px;
    }

    div[data-testid="stButton"] button:hover {
        color: #C9A876;
        background: none;
    }

    div[data-testid="stButton"] button:focus {
        box-shadow: none;
        outline: 2px solid #B08D57;
        outline-offset: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONTENT
# ============================================================

st.markdown('<div class="toolbox-wordmark">IP Toolbox</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="toolbox-intro">
    A working set of tools built for the patent research team.
    Pick one below to get started.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<hr class="registry-rule">', unsafe_allow_html=True)

# ------------------------------------------------------------
# Tool: Assignee Normalizer (live)
# ------------------------------------------------------------

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown(
        """
        <div class="tool-name">Assignee Normalizer<span class="tool-status-live">Live</span></div>
        <div class="tool-desc">
        Resolves inconsistent parent assignee names using AI — corporate
        entity matching, subsidiary detection, and ultimate parent
        identification for patent datasets.
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open tool", key="open_assignee_normalizer"):
        st.switch_page("pages/1_Assignee_Normalizer.py")

st.markdown('<hr class="registry-rule">', unsafe_allow_html=True)

# ------------------------------------------------------------
# Tool: FTO Tool (placeholder - not yet available)
# ------------------------------------------------------------

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown(
        """
        <div class="tool-name">FTO Tool<span class="tool-status-pending">In progress</span></div>
        <div class="tool-desc-pending">
        Freedom-to-operate analysis support. Not yet available.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<hr class="registry-rule">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="font-size: 0.85rem; color: #5C6472; margin-top: 1rem;">
    Internal tool · IP Toolbox · Questions or issues? Reach out anytime.
    </div>
    """,
    unsafe_allow_html=True
)
