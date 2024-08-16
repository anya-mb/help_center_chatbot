import streamlit as st


# Setting page title and headers
def set_titles_and_headers():
    st.set_page_config(page_title="Pacific Gas and Electric Company bot", page_icon="🌐⚡💬")
    st.markdown(
        "<h1 style='text-align: center;'>FAQ assistant</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "Welcome to the Pacific Gas and Electric Company FAQ Chatbot!"
        ,
        unsafe_allow_html=True,
    )

    st.markdown(
        "Feel free to ask your questions!",
        unsafe_allow_html=True,
    )