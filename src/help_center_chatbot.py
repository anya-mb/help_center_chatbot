import logging
from RAG_manager import load_vector_store, create_query_engine
import argparse
from utils import setup_logging

from nemoguardrails import RailsConfig, LLMRails
import nest_asyncio

nest_asyncio.apply()


# Path for the log file
LOG_PATH = '../logs/help_center_chatbot_log.txt'
setup_logging(LOG_PATH)

CONFIG_PATH = 'config'


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments, including the user's question.
    """
    parser = argparse.ArgumentParser(
        description="Question Answering Bot"
    )
    parser.add_argument(
        "--question",
        type=str,
        default="Why is my gas bill so high?",
        help="Question to ask the bot.",
    )
    return parser.parse_args()


def generate_response_with_llama_index(question: str) -> str:
    """
    Generate a response to a user's question using a pre-loaded vector store and query engine.

    Args:
        question (str): The user's question to be answered by the bot.

    Returns:
        str: The response generated by the query engine.
    """
    # Load the vector store from ChromaDB
    index = load_vector_store()

    # Create a query engine based on the loaded index
    query_engine = create_query_engine(index)

    logging.info(f"Question: {question}")
    response = query_engine.query(question)
    logging.info(f"Response: {response}")

    return response.response


def generate_response(question: str) -> str:
    """
    Generate a response to a user's question using a pre-loaded vector store and query engine.
    This implementation uses NEMO Guardrails.

    Args:
        question (str): The user's question to be answered by the bot.

    Returns:
        str: The response generated by the query engine.
    """

    config = RailsConfig.from_path(CONFIG_PATH)
    rails = LLMRails(config)

    logging.info(f"Question: {question}")

    response = rails.generate(messages=[{
        "role": "user",
        "content": question
    }])

    logging.info(f"Response: {response['content']}")

    return response['content']


def run():
    """
    Run the main script that handles parsing arguments, generating responses, and logging.

    This function coordinates the workflow of parsing command-line input,
    generating a response using a query engine, and logging the output.
    """
    # Parse command-line arguments
    args = parse_arguments()
    logging.info(f"Arguments: {args}")

    question = args.question
    response = generate_response(question)  # response is logged


if __name__ == "__main__":
    run()
