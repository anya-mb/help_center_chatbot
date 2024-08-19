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

CHROMA_DB_PERSISTENT_PATH = '../data/chroma_db'
CHROMA_DB_COLLECTION_NAME = "bills_faqs"

PARSED_PATH = '../data/Bill_FAQs/parsed'

# define global LLM
Settings.llm = OpenAI(temperature=0.3, model="gpt-4o-mini")

LOG_PATH = '../logs/generative_ai_utils_log.txt'
setup_logging(LOG_PATH)


def create_vector_store(
        document_path: str = PARSED_PATH,
        chroma_path: str = CHROMA_DB_PERSISTENT_PATH,
        collection_name: str = CHROMA_DB_COLLECTION_NAME
):
    # load some documents
    documents = SimpleDirectoryReader(document_path).load_data()

    # initialize client, setting path to save data
    db = chromadb.PersistentClient(path=chroma_path)

    # create collection
    chroma_collection = db.get_or_create_collection(collection_name)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # define LLM
    llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, llm=llm
    )
    logging.info("Vector store is created")


def load_vector_store(
        chroma_path: str = CHROMA_DB_PERSISTENT_PATH,
        collection_name: str = CHROMA_DB_COLLECTION_NAME
) -> object:
    # initialize client
    db = chromadb.PersistentClient(path=chroma_path)

    # get collection
    chroma_collection = db.get_or_create_collection(collection_name)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # define LLM
    llm = OpenAI(temperature=0.1, model="gpt-4o-mini")

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context, llm=llm
    )
    logging.info("Vector store is loaded")
    return index


def create_query_engine(index: object) -> object:
    # create a query engine
    query_engine = index.as_query_engine()
    logging.info("Query engine created")

    return query_engine


if __name__ == "__main__":
    logging.info("Run create_vector_store")
    create_vector_store()
