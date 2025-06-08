import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI

api_key = os.getenv("GOOGLE_API_KEY")

def get_gemini_embeddings_model():
    try:
        doc_embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", task_type="RETRIEVAL_DOCUMENT"
        )
        query_embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", task_type="RETRIEVAL_QUERY"
        )
        print("Gemini Embeddings model initialized successfully.")
        return doc_embeddings_model, query_embeddings_model
    except Exception as e:
        print(f"Error initializing Gemini Embeddings model: {e}")


def call_llm(prompt_txt,model_name):
    llm = GoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)
    response = llm.invoke(prompt_txt)
    return response

def call_structured_llm(prompt_txt,model_name, ResponseClass):
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)
    structured_llm = llm.with_structured_output(ResponseClass)
    response = structured_llm.invoke(prompt_txt)
    return response
