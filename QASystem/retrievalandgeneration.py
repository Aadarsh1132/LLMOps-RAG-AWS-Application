import logging
import sys
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Bedrock
import boto3
from langchain.prompts import PromptTemplate
from QASystem.ingestion import get_vector_store, data_ingestion
from langchain_community.embeddings import BedrockEmbeddings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("query.log"),  # Log to a file
        logging.StreamHandler(sys.stdout)  # Also print to console
    ]
)
logger = logging.getLogger(__name__)

# Bedrock client and embeddings setup
try:
    bedrock = boto3.client(service_name="bedrock-runtime")
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {str(e)}")
    sys.exit(1)
else:
    logger.info("Successfully initialized Bedrock client.")

try:
    bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)
except Exception as e:
    logger.error(f"Failed to initialize Bedrock embeddings: {str(e)}")
    sys.exit(1)
else:
    logger.info("Successfully initialized Bedrock embeddings.")

# Prompt template
prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but use at least summarize with 
250 words with detailed explanations. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

Question: {question}

Assistant:"""

try:
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
except Exception as e:
    logger.error(f"Failed to create PromptTemplate: {str(e)}")
    sys.exit(1)
else:
    logger.info("Successfully created PromptTemplate.")

def get_llama2_llm():
    """Initialize the Llama 2 13B Chat model from Bedrock."""
    try:
        llm = Bedrock(model_id="meta.llama3-8b-instruct-v1:0", client=bedrock)
    except Exception as e:
        logger.error(f"Failed to initialize Llama 2 LLM: {str(e)}")
        raise
    else:
        logger.info("Successfully initialized Llama 2 LLM.")
        return llm

def get_response_llm(llm, vectorstore_faiss, query):
    """Retrieve and generate a response using the RetrievalQA chain."""
    try:
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore_faiss.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        logger.info(f"Created RetrievalQA chain for query: '{query}'.")
        
        answer = qa({"query": query})
    except Exception as e:
        logger.error(f"Error in RetrievalQA chain or query execution: {str(e)}")
        raise
    else:
        logger.info("Successfully retrieved and generated response.")
        return answer["result"]

if __name__ == '__main__':
    try:
        logger.info("Starting query process.")
        
        # Load FAISS index
        faiss_index = FAISS.load_local(
            "faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True
        )
    except Exception as e:
        logger.error(f"Failed to load FAISS index: {str(e)}")
        sys.exit(1)
    else:
        logger.info("Successfully loaded FAISS index from 'faiss_index' directory.")
    
    try:
        query = "What is RAG token?"
        llm = get_llama2_llm()
        response = get_response_llm(llm, faiss_index, query)
    except Exception as e:
        logger.error(f"Query process failed: {str(e)}")
        sys.exit(1)
    else:
        logger.info(f"Query: '{query}' processed successfully.")
        print(response)