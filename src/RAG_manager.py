from dotenv import load_dotenv, find_dotenv
import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import openai
import logging
from utils import setup_logging

import warnings

warnings.filterwarnings("ignore")

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define file paths and collection name for ChromaDB
CHROMA_DB_PERSISTENT_PATH = '../data/chroma_db'
CHROMA_DB_COLLECTION_NAME = "bills_faqs"
PARSED_PATH = '../data/Bill_FAQs/parsed'

# Configure global LLM settings
Settings.llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

# Set up logging configuration
LOG_PATH = '../logs/generative_ai_utils_log.txt'
setup_logging(LOG_PATH)


def create_vector_store(
        document_path: str = PARSED_PATH,
        chroma_path: str = CHROMA_DB_PERSISTENT_PATH,
        collection_name: str = CHROMA_DB_COLLECTION_NAME
):
    """
    Create a vector store from documents and save it in ChromaDB.

    Args:
        document_path (str): The path to the directory containing the documents to be indexed.
        chroma_path (str): The path where ChromaDB will persist data.
        collection_name (str): The name of the ChromaDB collection to use or create.

    Returns:
        None
    """
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(document_path).load_data()

    # Initialize ChromaDB client with a persistent path for saving data
    db = chromadb.PersistentClient(path=chroma_path)

    # Create or retrieve the specified collection in ChromaDB
    chroma_collection = db.get_or_create_collection(collection_name)

    # Assign ChromaDB collection as the vector store for the storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create an index from the documents using the storage context and LLM
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, llm=Settings.llm
    )

    logging.info("Vector store has been created successfully.")


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


def create_query_engine(index: object) -> object:
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


if __name__ == "__main__":
    logging.info("Running create_vector_store function.")
    create_vector_store(CHROMA_DB_PERSISTENT_PATH, CHROMA_DB_COLLECTION_NAME)
