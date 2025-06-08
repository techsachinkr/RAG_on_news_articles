import mlflow
import datetime
import sys,os
sys.path.append(os.getcwd())
from dotenv import load_dotenv

load_dotenv()

from services.evaluation_utils import (calculate_context_relevance,
                              calculate_faithfulness, 
                              calculate_answer_relevance_to_question, 
                            calculate_answer_correctness_score
                                )

retriever_model_name = "gemini_text-embedding-004"
generator_model_name = "gemini-1.5-flash"
retriever_top_k_config = "1"

def get_metrics_no_ground_truth(question,retrieved_context,generated_answer):
    context_relevance = calculate_context_relevance(question, retrieved_context)
    faithfulness = calculate_faithfulness(question, retrieved_context, generated_answer)
    answer_relevance_q = calculate_answer_relevance_to_question(question,generated_answer)

    return {"context_relevance":context_relevance,
            "faithfulness":faithfulness,
            "answer_relevance_q":answer_relevance_q
            }

@mlflow.trace(name="RAG.evaluate_question_pipeline")
def get_metrics(question,retrieved_context,generated_answer,ground_truth_answer):
    context_relevance = calculate_context_relevance(question, retrieved_context)
    faithfulness = calculate_faithfulness(question, retrieved_context, generated_answer)
    answer_relevance_q = calculate_answer_relevance_to_question(question,generated_answer)
    correctness = calculate_answer_correctness_score(question, generated_answer, ground_truth_answer)
    return {"context_relevance":context_relevance,
            "faithfulness":faithfulness,
            "answer_relevance_q":answer_relevance_q,
            "correctness":correctness}

def run_mlflow_evals(evaluation_dataset):
    mlflow.set_tracking_uri("http://localhost:5000/")
    with mlflow.start_run(run_name=f"RAG_Eval_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
            print(f"MLflow Run ID: {run.info.run_id}")
            print(f"MLflow Experiment ID: {run.info.experiment_id}")

            # Log parameters
            mlflow.log_param("retriever_model", retriever_model_name)
            mlflow.log_param("generator_model", generator_model_name)
            mlflow.log_param("retriever_top_k", retriever_top_k_config)
            mlflow.log_param("evaluation_dataset_size", len(evaluation_dataset))
            context_relevance_score=0
            faithfulness_score=0
            answer_relevance_q_score=0
            correctness_score=0
            for i, item in evaluation_dataset.iterrows():
                question_id = i+1
                question = item["question"]
                ground_truth_answer = item["answer"]
                retrieved_context = item["retrieved_context"] 
                generated_answer = item["rag_answer"]
                
                
                # Calculate metrics
                metrics_response=get_metrics(question,retrieved_context,generated_answer,ground_truth_answer)
                context_relevance = metrics_response["context_relevance"]
                faithfulness= metrics_response["faithfulness"]
                answer_relevance_q= metrics_response["answer_relevance_q"]
                correctness= metrics_response["correctness"]

                context_relevance_score+=float(context_relevance.score)
                faithfulness_score+=float(faithfulness.score)
                answer_relevance_q_score+=float(answer_relevance_q.score)
                correctness_score+=float(correctness.score)
            total_items=len(evaluation_dataset)
            mlflow.log_metric(f"avg_context_relevance",context_relevance_score/total_items)
            mlflow.log_metric(f"avg_faithfulness", faithfulness_score/total_items)
            mlflow.log_metric(f"avg_answer_relevance_q", answer_relevance_q_score/total_items)
            mlflow.log_metric(f"avg_similarity_gt", correctness_score/total_items)    