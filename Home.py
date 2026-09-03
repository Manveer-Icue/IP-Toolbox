import streamlit as st
from auth import require_password

st.set_page_config(
    page_title="IP Toolbox",
    page_icon="📇",
    layout="wide"
)

# ============================================================
# HIDE SIDEBAR
# ============================================================

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background-color: #F7F7F5;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }

    * {
        font-family: 'Inter', sans-serif;
    }


    /* --------------------------------------------------------
       HEADER
    -------------------------------------------------------- */

    .toolbox-wordmark {
        font-size: 2.5rem;
        font-weight: 700;
        color: #EE3C18;
        letter-spacing: -0.045em;
        line-height: 1.1;
        margin-bottom: 0.65rem;
    }

    .toolbox-intro {
        font-size: 1rem;
        line-height: 1.65;
        color: #6B6F76;
        max-width: 650px;
        margin-bottom: 2.8rem;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #8A8E94;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1rem;
    }


    /* --------------------------------------------------------
       TOOL CARDS
    -------------------------------------------------------- */

    .tool-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-radius: 12px;
        padding: 1.65rem;
        height: 260px;
        box-sizing: border-box;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.035);
        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            border-color 0.18s ease;
    }

    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.07);
        border-color: #D9D9D5;
    }

    .tool-card-disabled {
        background-color: #FBFBFA;
        box-shadow: none;
    }

    .tool-card-disabled:hover {
        transform: none;
        box-shadow: none;
    }


    /* --------------------------------------------------------
       TOOL NAME BOX
    -------------------------------------------------------- */

    .tool-name-box {
        display: inline-flex;
        align-items: center;
        background-color: #FFF0EC;
        color: #EE3C18;
        border: 1px solid #FFD9D1;
        border-radius: 8px;
        padding: 0.65rem 0.9rem;
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.2;
        letter-spacing: -0.015em;
        margin-bottom: 1rem;
    }

    .tool-name-box-disabled {
        background-color: #F0F0EE;
        color: #73777B;
        border-color: #E5E5E2;
    }


    /* --------------------------------------------------------
       STATUS
    -------------------------------------------------------- */

    .status-live {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        margin-left: 8px;
        padding: 3px 8px;
        border-radius: 20px;
        background-color: #FFF0EC;
        color: #EE3C18;
        font-size: 0.66rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        vertical-align: middle;
        text-transform: uppercase;
    }

    .status-pending {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        margin-left: 8px;
        padding: 3px 8px;
        border-radius: 20px;
        background-color: #F0F0EE;
        color: #85888C;
        font-size: 0.66rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        vertical-align: middle;
        text-transform: uppercase;
    }

    .status-dot-live {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background-color: #EE3C18;
    }

    .status-dot-pending {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background-color: #9A9DA0;
    }


    /* --------------------------------------------------------
       DESCRIPTION
    -------------------------------------------------------- */

    .tool-desc {
        font-size: 0.88rem;
        line-height: 1.6;
        color: #74787D;
    }

    .tool-desc-pending {
        font-size: 0.88rem;
        line-height: 1.6;
        color: #96999D;
    }


    /* --------------------------------------------------------
       BUTTON
    -------------------------------------------------------- */

    div[data-testid="stButton"] {
        margin-top: 0.8rem;
    }

    div[data-testid="stButton"] button {
        background-color: #EE3C18;
        color: #FFFFFF;
        border: 1px solid #EE3C18;
        border-radius: 7px;
        font-size: 0.84rem;
        font-weight: 600;
        padding: 0.42rem 0.85rem;
        min-height: 36px;
        transition: all 0.15s ease;
    }

    div[data-testid="stButton"] button:hover {
        background-color: #D93414;
        border-color: #D93414;
        color: #FFFFFF;
    }

    div[data-testid="stButton"] button:focus {
        box-shadow: 0 0 0 3px rgba(238, 60, 24, 0.15);
        outline: none;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer-rule {
        border: none;
        border-top: 1px solid #E2E2DF;
        margin-top: 2.7rem;
        margin-bottom: 1.1rem;
    }

    .footer {
        font-size: 0.76rem;
        color: #999C9F;
    }


    /* --------------------------------------------------------
       RESPONSIVE
    -------------------------------------------------------- */

    @media (max-width: 800px) {

        .block-container {
            padding-top: 2.5rem;
        }

        .toolbox-wordmark {
            font-size: 2.1rem;
        }

        .tool-card {
            height: auto;
            min-height: 260px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="toolbox-wordmark">IP Toolbox</div>
    <div class="toolbox-intro">
        A focused set of tools built to support patent research,
        analysis, and portfolio workflows.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AVAILABLE TOOLS
# ============================================================

st.markdown(
    '<div class="section-label">Available tools</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")


# ============================================================
# TOOL 1: ASSIGNEE NORMALIZER
# ============================================================

with col1:

    st.markdown(
        """
        <div class="tool-card">

            <div class="tool-name-box">
                Assignee Normalizer
            </div>

            <div>
                <span class="status-live">
                    <span class="status-dot-live"></span>
                    Live
                </span>
            </div>

            <div class="tool-desc" style="margin-top: 0.9rem;">
                Resolves inconsistent parent assignee names using AI,
                including corporate entity matching, subsidiary detection,
                and ultimate parent identification.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Open tool  →",
        key="open_assignee_normalizer"
    ):
        st.switch_page("pages/1_Assignee_Normalizer.py")


# ============================================================
# TOOL 2: FTO ANALYSIS
# ============================================================

with col2:

    st.markdown(
        """
        <div class="tool-card tool-card-disabled">

            <div class="tool-name-box tool-name-box-disabled">
                FTO Analysis
            </div>

            <div>
                <span class="status-pending">
                    <span class="status-dot-pending"></span>
                    In progress
                </span>
            </div>

            <div class="tool-desc-pending" style="margin-top: 0.9rem;">
                Supports freedom-to-operate analysis by helping
                researchers identify and evaluate potentially relevant
                patent rights.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TOOL 3: PATENT SCREENING
# ============================================================

with col3:

    st.markdown(
        """
        <div class="tool-card tool-card-disabled">

            <div class="tool-name-box tool-name-box-disabled">
                Patent Screening
            </div>

            <div>
                <span class="status-pending">
                    <span class="status-dot-pending"></span>
                    Coming soon
                </span>
            </div>

            <div class="tool-desc-pending" style="margin-top: 0.9rem;">
                Streamlines initial patent review and helps identify
                potentially relevant documents for deeper analysis.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr class="footer-rule">
    <div class="footer">
        Internal IP Research Platform
    </div>
    """,
    unsafe_allow_html=True
)
