import streamlit as st
from streamlit_chat import message

from src.help_center_chatbot import generate_response
from src.utils import set_titles_and_headers


set_titles_and_headers()

# Initialise session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# container for chat history
response_container = st.container()

# container for text box
container = st.container()


with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

        # st.session_state["messages"].append(user_input)

    if submit_button and user_input:
        output = generate_response(
            user_input#, st.session_state["messages"]
        )
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

        # st.session_state["messages"].append(output)


if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user", avatar_style="avataaars", seed=123)
            message(st.session_state["generated"][i], is_user=False, key=str(i), avatar_style="initials", seed="AI")


if st.button("Clear the chat"):
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = []

    st.experimental_rerun()
