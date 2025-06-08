from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
import os,sys
sys.path.append(os.getcwd())


from services.helper_utils import get_gemini_embeddings_model, call_llm
from assets.chroma_langchain_db.prompts.rag_generation import RAG_GENERATION_PROMPT_TEMPLATE



current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

vectordb_filename=os.path.join(os.path.dirname(current_directory),"assets")
PERSIST_DIRECTORY = vectordb_filename+"/chroma_langchain_db"

doc_embeddings_model, query_embeddings_model = get_gemini_embeddings_model()


def load_vector_db():
    vector_db_load = Chroma(persist_directory=PERSIST_DIRECTORY ,
                            embedding_function=doc_embeddings_model,
                            collection_name="rag_collection")
    return vector_db_load



def get_RAG_response(question):
    model_name="gemini-1.5-flash"
    vector_db_load = load_vector_db()
    retrieval_result = vector_db_load.similarity_search_by_vector(
        embedding=query_embeddings_model.embed_query(question), k=1
    )
    context_text=retrieval_result[0].page_content
    prompt_txt=RAG_GENERATION_PROMPT_TEMPLATE.format(question=question, context=context_text)
    response=call_llm(prompt_txt,model_name)
    return context_text, response

# get_RAG_response("whats the ISEQ index of leading shares")

