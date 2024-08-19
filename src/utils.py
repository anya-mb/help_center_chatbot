import streamlit as st
import logging


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


def setup_logging(logfile_path: str):
    """
    Setup logging configuration to log messages to both a file and the console.

    Args:
        logfile_path (str): Path to the log file where log messages will be saved.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(logfile_path), logging.StreamHandler()],
    )
