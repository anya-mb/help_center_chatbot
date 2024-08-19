import logging
from src.generative_ai_utils import load_vector_store, create_query_engine


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

index = load_vector_store()
query_engine = create_query_engine(index)


def generate_response(question: str) -> str:
    response = query_engine.query(question)

    return response.response
