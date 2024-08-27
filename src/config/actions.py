from typing import Optional
from nemoguardrails.actions import action
# from llama_index.core import SimpleDirectoryReader
# from llama_index.core.llama_pack import download_llama_pack
# from llama_index.packs.recursive_retriever import RecursiveRetrieverSmallToBigPack
# from llama_index.core.base.base_query_engine import BaseQueryEngine
# from llama_index.core.base.response.schema import StreamingResponse

from dotenv import load_dotenv, find_dotenv
import os
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import openai
import logging

import warnings

warnings.filterwarnings("ignore")

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define file paths and collection name for ChromaDB
# CHROMA_DB_PERSISTENT_PATH = '../data/chroma_db_1_source'
CHROMA_DB_PERSISTENT_PATH = '../data/chroma_db'
CHROMA_DB_COLLECTION_NAME = "bills_faqs"
PARSED_PATH = '../data/Bill_FAQs/all'

# Configure global LLM settings
Settings.llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

# # Set up logging configuration
# LOG_PATH = '../logs/generative_ai_utils_log.txt'
# logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
#     )


def load_vector_store(
        chroma_path: str = CHROMA_DB_PERSISTENT_PATH,
        collection_name: str = CHROMA_DB_COLLECTION_NAME
) -> object:
    """
    Load an existing vector store from ChromaDB.

    Args:
        chroma_path (str): The path where ChromaDB has persisted data.
        collection_name (str): The name of the ChromaDB collection to load.

    Returns:
        object: The loaded VectorStoreIndex object.
    """
    logging.info("Loading the vector store")
    logging.info(f"Chroma path: {chroma_path}")
    logging.info(f"Collection name: {collection_name}")

    # Initialize ChromaDB client with a persistent path
    db = chromadb.PersistentClient(path=chroma_path)

    # Retrieve the specified collection from ChromaDB
    chroma_collection = db.get_or_create_collection(collection_name)

    # Assign ChromaDB collection as the vector store for the storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load the index from the stored vector data
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context, llm=Settings.llm
    )

    logging.info("Vector store has been loaded successfully.")
    return index


def create_query_engine(index: object) -> BaseQueryEngine:
    """
    Create a query engine from the given index.

    Args:
        index (object): The VectorStoreIndex object from which to create the query engine.

    Returns:
        object: The created query engine.
    """
    # Create a query engine from the provided index
    query_engine = index.as_query_engine()

    logging.info("Query engine has been created successfully.")
    return query_engine


# Global variable to cache the query_engine
query_engine_cache = None

def init():
    global query_engine_cache  # Declare to use the global variable
    # Check if the query_engine is already initialized
    if query_engine_cache is not None:
        print('Using cached query engine')
        return query_engine_cache

    # load data
    index = load_vector_store()

    # create query engine
    query_engine_cache = create_query_engine(index)

    return query_engine_cache

def get_query_response(query_engine: BaseQueryEngine, query: str) -> str:
    """
    Function to query based on the query_engine and query string passed in.
    """
    response = query_engine.query(query)

    response_str = response.response
    if response_str is None:
        return ""
    return response_str

@action(is_system_action=True)
async def user_query(context: Optional[dict] = None):
    """
    Function to invoke the query_engine to query user message.
    """
    user_message = context.get("user_message")
    print('user_message is ', user_message)
    query_engine = init()
    return get_query_response(query_engine, user_message) 