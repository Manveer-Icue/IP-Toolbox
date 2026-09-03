import streamlit as st

def require_password():
    if st.session_state.get("authenticated", False):
        return

    app_password = st.secrets.get("APP_PASSWORD", "")

    if not app_password:
        return  # no password configured, skip gate

    st.title("IP Toolbox — Login")
    entered = st.text_input("Enter access password", type="password")

    if st.button("Enter"):
        if entered == app_password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()
