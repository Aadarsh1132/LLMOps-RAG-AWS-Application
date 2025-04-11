import json
import os 
import sys
import boto3
from flask import Flask, render_template, request, jsonify

from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from QASystem.ingestion import data_ingestion, get_vector_store
from QASystem.retrievalandgeneration import get_llama2_llm, get_response_llm

app = Flask(__name__)

# Initialize bedrock client
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    # Get user question from form
    user_question = request.form['question']
    
    # Load the FAISS index
    faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
    
    # Get LLM and generate response
    llm = get_llama2_llm()
    response = get_response_llm(llm, faiss_index, user_question)
    
    return jsonify({'response': response})

@app.route('/update_vectordb', methods=['POST'])
def update_vectordb():
    try:
        # Update vector database
        docs = data_ingestion()
        get_vector_store(docs)
        return jsonify({'status': 'success', 'message': 'VectorDB updated successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)