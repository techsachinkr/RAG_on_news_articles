RAG_GENERATION_PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know. Answer should be based on concise piece of factual information from the context.
Question: {question}
Context: {context}
Answer:
"""