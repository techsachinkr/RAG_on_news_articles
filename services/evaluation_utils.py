from assets.chroma_langchain_db.prompts.evaluation_metrics import (context_relevance_prompt,
                                                                   faithfulness_prompt,
                                                                   answer_relevance_to_question_prompt,
                                                                   answer_correctness_score_prompt)
from services.helper_utils import call_structured_llm
from pydantic import BaseModel



judge_llm = "gemini-2.0-flash"

class JudgeResponse(BaseModel):
    reasoning: str
    score: str


def calculate_context_relevance(question,context):
    promptval=context_relevance_prompt.format(question=question,doc_1_content=context)
    response=call_structured_llm(promptval,judge_llm,JudgeResponse)
    return response

def calculate_faithfulness(question,context,generated_answer):
    promptval=faithfulness_prompt.format(question=question,doc_1_content=context,generated_answer=generated_answer)
    response=call_structured_llm(promptval,judge_llm,JudgeResponse)
    return response

def calculate_answer_relevance_to_question(question,generated_answer):
    promptval=answer_relevance_to_question_prompt.format(question=question,generated_answer=generated_answer)
    response=call_structured_llm(promptval,judge_llm,JudgeResponse)
    return response

def calculate_answer_correctness_score(question,generated_answer,ground_truth_answer):
    promptval=answer_correctness_score_prompt.format(question=question,generated_answer=generated_answer,ground_truth_answer=ground_truth_answer)
    response=call_structured_llm(promptval,judge_llm,JudgeResponse)
    return response



