import logging
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock
import json
import os
import sys
import boto3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ingestion.log"),  # Log to a file
        logging.StreamHandler(sys.stdout)      # Also print to console
    ]
)
logger = logging.getLogger(__name__)

# Bedrock client setup
try:
    bedrock = boto3.client(service_name="bedrock-runtime")
    logger.info("Successfully initialized Bedrock client.")
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {str(e)}")
    sys.exit(1)  # Exit if Bedrock client fails, as it's critical

try:
    bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)
    logger.info("Successfully initialized Bedrock embeddings.")
except Exception as e:
    logger.error(f"Failed to initialize Bedrock embeddings: {str(e)}")
    sys.exit(1)  # Exit if embeddings fail

def data_ingestion():
    """Load and split PDF documents from a directory."""
    try:
        # Load PDFs
        loader = PyPDFDirectoryLoader("./data")
        logger.info("Starting PDF loading from './data' directory.")
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from './data'.")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        logger.info(f"Split documents into {len(docs)} chunks.")
        
        return docs
    
    except FileNotFoundError as e:
        logger.error(f"Directory './data' not found or inaccessible: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error during data ingestion: {str(e)}")
        raise

def get_vector_store(docs):
    """Create and save a FAISS vector store from document chunks."""
    try:
        logger.info("Creating FAISS vector store from documents.")
        vector_store_faiss = FAISS.from_documents(docs, bedrock_embeddings)
        logger.info("Successfully created FAISS vector store.")
        
        # Save the vector store locally
        vector_store_faiss.save_local("faiss_index")
        logger.info("Saved FAISS vector store to 'faiss_index' directory.")
        
        return vector_store_faiss
    
    except Exception as e:
        logger.error(f"Error creating or saving FAISS vector store: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        logger.info("Starting ingestion process.")
        docs = data_ingestion()
        vector_store = get_vector_store(docs)
        logger.info("Ingestion process completed successfully.")
    except Exception as e:
        logger.error(f"Ingestion process failed: {str(e)}")
        sys.exit(1)