import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_response(question: str) -> str:
    return "Here is the answer!"
