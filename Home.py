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


/* ============================================================
   GLOBAL
   ============================================================ */

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


/* ============================================================
   HEADER
   ============================================================ */

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


/* ============================================================
   AVAILABLE TOOLS LAYOUT
   ============================================================ */

[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 1.5rem !important;
    align-items: stretch !important;
}


/* ============================================================
   TOOL COLUMNS
   ============================================================ */

[data-testid="stHorizontalBlock"] > [data-testid="column"],
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
}


/* ============================================================
   TOOL CARD WRAPPER
   ============================================================ */

.tool-wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
}


/* ============================================================
   TOOL CARDS
   ============================================================ */

.tool-card {
    width: 100%;
    height: 390px;
    min-height: 390px;
    box-sizing: border-box;

    background-color: #FFFFFF;
    border: 1px solid #E3E3E0;
    border-radius: 12px;

    padding: 1.5rem 1.5rem 1.35rem 1.5rem;

    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.035);

    display: flex;
    flex-direction: column;

    overflow: hidden;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}

.tool-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.07);
    border-color: #D8D8D4;
}

.tool-card-disabled {
    background-color: #FBFBFA;
    box-shadow: none;
}

.tool-card-disabled:hover {
    transform: none;
    box-shadow: none;
}


/* ============================================================
   TOOL NAME AREA
   ============================================================ */

.tool-name-area {
    height: 92px;
    min-height: 92px;
    display: flex;
    align-items: flex-start;
    flex-shrink: 0;
}

.tool-name-box {
    width: 100%;
    min-height: 61px;
    box-sizing: border-box;

    display: flex;
    align-items: center;
    justify-content: flex-start;

    background-color: #FFF0EC;
    color: #EE3C18;

    border: 1px solid #FFD9D1;
    border-radius: 8px;

    padding: 0.65rem 0.9rem;

    font-size: 1rem;
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: -0.015em;

    overflow-wrap: break-word;
}

.tool-name-box-disabled {
    background-color: #F0F0EE;
    color: #73777B;
    border-color: #E5E5E2;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-area {
    height: 31px;
    min-height: 31px;

    display: flex;
    align-items: flex-start;
    flex-shrink: 0;

    margin-bottom: 0.25rem;
}

.status-live {
    display: inline-flex;
    align-items: center;
    gap: 5px;

    padding: 3px 8px;

    border-radius: 20px;

    background-color: #FFF0EC;
    color: #EE3C18;

    font-size: 0.66rem;
    font-weight: 600;

    letter-spacing: 0.04em;
    text-transform: uppercase;

    white-space: nowrap;
}

.status-pending {
    display: inline-flex;
    align-items: center;
    gap: 5px;

    padding: 3px 8px;

    border-radius: 20px;

    background-color: #F0F0EE;
    color: #85888C;

    font-size: 0.66rem;
    font-weight: 600;

    letter-spacing: 0.04em;
    text-transform: uppercase;

    white-space: nowrap;
}

.status-dot-live {
    width: 5px;
    height: 5px;

    min-width: 5px;
    min-height: 5px;

    border-radius: 50%;

    background-color: #EE3C18;
}

.status-dot-pending {
    width: 5px;
    height: 5px;

    min-width: 5px;
    min-height: 5px;

    border-radius: 50%;

    background-color: #9A9DA0;
}


/* ============================================================
   DESCRIPTION
   ============================================================ */

.tool-desc {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #74787D;

    flex: 1;

    padding-top: 0.1rem;

    overflow-wrap: break-word;
    word-break: normal;
}

.tool-desc-pending {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #96999D;

    flex: 1;

    padding-top: 0.1rem;

    overflow-wrap: break-word;
    word-break: normal;
}


/* ============================================================
   BUTTON AREA
   ============================================================ */

.tool-button-area {
    height: 42px;
    min-height: 42px;

    display: flex;
    align-items: flex-end;
}


/* ============================================================
   STREAMLIT BUTTON
   ============================================================ */

div[data-testid="stButton"] {
    margin-top: 0.7rem;
    margin-bottom: 0;
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


/* ============================================================
   FOOTER
   ============================================================ */

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


/* ============================================================
   RESPONSIVE
   ============================================================ */


/* MEDIUM SCREENS: 3 CARDS PER ROW */

@media (max-width: 1500px) {

    [data-testid="stHorizontalBlock"] > [data-testid="column"],
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 0 0 calc((100% - 3rem) / 3) !important;
        min-width: calc((100% - 3rem) / 3) !important;
    }
}


/* TABLET: 2 CARDS PER ROW */

@media (max-width: 900px) {

    .block-container {
        padding-top: 2.5rem;
    }

    .toolbox-wordmark {
        font-size: 2.1rem;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 1.25rem !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"],
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 0 0 calc((100% - 1.25rem) / 2) !important;
        min-width: calc((100% - 1.25rem) / 2) !important;
    }

    .tool-card {
        height: 390px;
        min-height: 390px;
    }
}


/* MOBILE: 1 CARD PER ROW */

@media (max-width: 600px) {

    [data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"],
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 0 0 100% !important;
        min-width: 100% !important;
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

col1, col2, col3, col4, col5 = st.columns(5, gap="large")


# ============================================================
# TOOL 1: ASSIGNEE NORMALIZER
# ============================================================

with col1:

    st.markdown(
        """
<div class="tool-wrapper">

<div class="tool-card">

<div class="tool-name-area">
<div class="tool-name-box">
Assignee Normalizer
</div>
</div>

<div class="status-area">
<span class="status-live">
<span class="status-dot-live"></span>
Live
</span>
</div>

<div class="tool-desc">
Resolves inconsistent parent assignee names using AI,
including corporate entity matching, subsidiary detection,
and ultimate parent identification.
</div>

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
# TOOL 2: PATENT CATEGORY MAPPER
# ============================================================

with col2:

    st.markdown(
        """
<div class="tool-wrapper">

<div class="tool-card">

<div class="tool-name-area">
<div class="tool-name-box">
Patent Category Mapper
</div>
</div>

<div class="status-area">
<span class="status-live">
<span class="status-dot-live"></span>
Live
</span>
</div>

<div class="tool-desc">
Converts patent categorization data into individual
category columns and marks applicable patents with Y.
</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "Open tool  →",
        key="open_category_mapper"
    ):
        st.switch_page(
            "pages/2_Patent_Category_Mapper.py"
        )


# ============================================================
# TOOL 3: PATENT HYPERLINKER
# ============================================================

with col3:

    st.markdown(
        """
<div class="tool-wrapper">

<div class="tool-card">

<div class="tool-name-area">
<div class="tool-name-box">
Patent Hyperlinker
</div>
</div>

<div class="status-area">
<span class="status-live">
<span class="status-dot-live"></span>
Live
</span>
</div>

<div class="tool-desc">
Creates clickable patent links using Google Patents,
New Espacenet, or the original Orbit document link,
with dynamic routing based on patent country.
</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    if st.button(
        "Open tool  →",
        key="open_patent_hyperlinker"
    ):
        st.switch_page(
            "pages/3_Patent_Hyperlinker.py"
        )


# ============================================================
# TOOL 4: FTO CLAIM SCREENING
# ============================================================

with col4:

    st.markdown(
        """
<div class="tool-wrapper">

<div class="tool-card tool-card-disabled">

<div class="tool-name-area">
<div class="tool-name-box tool-name-box-disabled">
FTO Claim Screening
</div>
</div>

<div class="status-area">
<span class="status-pending">
<span class="status-dot-pending"></span>
In progress
</span>
</div>

<div class="tool-desc-pending">
Supports freedom-to-operate research by helping researchers
identify and evaluate relevant patent claims and supporting
rationale.
</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# TOOL 5: SAMPLE
# ============================================================

with col5:

    st.markdown(
        """
<div class="tool-wrapper">

<div class="tool-card tool-card-disabled">

<div class="tool-name-area">
<div class="tool-name-box tool-name-box-disabled">
Sample
</div>
</div>

<div class="status-area">
<span class="status-pending">
<span class="status-dot-pending"></span>
Coming soon
</span>
</div>

<div class="tool-desc-pending">
New tool ideas arising from different research requirements.
</div>

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
