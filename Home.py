import streamlit as st
from auth import require_password

st.set_page_config(page_title="IP Toolbox", page_icon="🧰", layout="wide")

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

st.title("🧰 IP Toolbox")
st.write("Internal tools for patent and IP research. Select a tool below to get started.")

st.markdown("---")

tools = [
    {
        "name": "Assignee Normalizer",
        "desc": "AI-powered normalization of Parent Assignee names in patent datasets — resolves spelling variants, subsidiaries, and ultimate parent companies.",
        "page": "pages/1_Assignee_Normalizer.py",
        "icon": "🏢"
    },
    # Add new tools here as they're built, e.g.:
    # {
    #     "name": "FTO Tool",
    #     "desc": "Freedom-to-operate analysis helper.",
    #     "page": "pages/2_FTO_Tool.py",
    #     "icon": "⚖️"
    # },
]

cols = st.columns(2)

for i, tool in enumerate(tools):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(f"{tool['icon']} {tool['name']}")
            st.write(tool["desc"])
            st.page_link(tool["page"], label=f"Open {tool['name']} →", use_container_width=True)

st.markdown("---")
st.caption("Internal Tool · IP Toolbox · Questions or issues? Reach out anytime.")
