import logging
from generative_ai_utils import load_vector_store, create_query_engine
import argparse
from utils import setup_logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOG_PATH = '../logs/help_center_chatbot_log.txt'
setup_logging(LOG_PATH)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Question Answering Bot"
    )
    parser.add_argument(
        "--question",
        type=str,
        default="Why is my gas bill so high?",
        help="Question to ask a bot",
    )
    return parser.parse_args()


def generate_response(query_engine: object, question: str) -> str:
    index = load_vector_store()
    query_engine = create_query_engine(index)

    logging.info(f"Question: {question}")

    response = query_engine.query(question)
    logging.info(f"Response: {response}")

    return response.response


def run():
    args = parse_arguments()
    logging.info(f"Arguments: {args}")

    question = args.question
    response = generate_response(question)
    print(response)


if __name__ == "__main__":
    run()
