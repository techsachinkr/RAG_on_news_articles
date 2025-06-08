context_relevance_prompt="""
You are an expert evaluator for a Retrieval Augmented Generation system. Your task is to assess the relevance of the provided context for answering a given question.

**Question**:
{question}

Retrieved Context:
---
{doc_1_content}
---

Instructions:
Consider document in the retrieved context. Evaluate how relevant each document is to the user's **Question**.
Then, provide an overall score for the entire set of retrieved context. The score should be a single floating-point number between 0.0 and 1.0, where 0.0 means the context is completely irrelevant or unhelpful, and 1.0 means the context is perfectly relevant and provides all necessary information to answer the question.

Briefly explain your reasoning for the score, noting why document is most/least relevant.

Please provide a response in a structured JSON format that matches the following format:
{{
  "reasoning": <Your brief explanation>,
  "score": <Your Score as a float, e.g., 0.85>
}}
"""

faithfulness_prompt="""
You are an expert evaluator for a Retrieval Augmented Generation system. Your task is to assess the faithfulness of a generated answer to its provided context. An answer is faithful if all claims made in the answer are supported by the information present in the retrieved context. The answer should not make up information or contradict the context.

Retrieved Context:
---
{doc_1_content}
---

Question (for reference):
{question}

Generated Answer:
{generated_answer}

Carefully compare the **Generated Answer** with the **Retrieved Context**. Determine if all factual statements in the answer can be verified from the context.
Provide a score between 0.0 and 1.0, where:
* 0.0 means the answer is completely unfaithful (e.g., contradicts the context or is entirely based on information outside the context).
* 1.0 means the answer is perfectly faithful and all its claims are fully supported by the context.

Identify any specific claims in the answer that are not supported by the context or contradict it. If the answer is fully faithful, state that.

Please provide a response in a structured JSON format that matches the following format:
{{
  "reasoning": <Your brief explanation>,
  "score": <Your Score as a float, e.g., 0.85>
}}
"""

answer_relevance_to_question_prompt="""
You are an expert evaluator for a Retrieval Augmented Generation system. Your task is to assess how relevant and complete a generated answer is with respect to the user's question.

**Question:**
{question}

**Generated Answer:**
{generated_answer}

Evaluate the **Generated Answer** based on how well it addresses the **Question**. Consider the following:
* **Directness:** Does the answer directly address the main intent of the question?
* **Completeness:** Does the answer provide a reasonably complete response to the question, or does it miss key aspects?
* **Focus:** Is the answer focused on the question, or does it include irrelevant information?

Provide a score between 0.0 and 1.0, where:
* 0.0 means the answer is completely irrelevant to the question or fails to address it at all.
* 1.0 means the answer is perfectly relevant, directly addresses the question, and is comprehensive.

Explain why the answer is or isn't relevant, noting any aspects of the question that were well-addressed or missed.

Please provide a response in a structured JSON format that matches the following format:

{{
  "reasoning": <Your brief explanation>,
  "score": <Your Score as a float, e.g., 0.85>
}}

"""

answer_correctness_score_prompt="""
You are an expert evaluator for a Retrieval Augmented Generation system. Your task is to assess the factual correctness and completeness of a **Generated Answer** by comparing it against a **Ground Truth Answer**.

**Question:**
{question}

**Generated Answer:**
{generated_answer}

**Ground Truth Answer**
{ground_truth_answer}

**Instructions:**
Carefully compare the **Generated Answer** with the **Ground Truth Answer**.
Evaluate the **Generated Answer** based on the following criteria:
* **Factual Accuracy:** Are all facts presented in the **Generated Answer** accurate when compared to the **Ground Truth Answer**? Does it introduce any inaccuracies or contradictions?
* **Completeness:** Does the **Generated Answer** cover all the key information present in the **Ground Truth Answer** relevant to the question? Does it omit any critical details?
* **Conciseness (Optional, if important):** Does the **Generated Answer** provide the information without unnecessary verbosity compared to the ground truth? (Consider if this is a primary evaluation goal).

Provide an overall score for correctness between 0.0 and 1.0, where:
* 0.0 means the **Generated Answer** is completely incorrect, factually inaccurate, or entirely misses the information present in the **Ground Truth Answer**.
* 0.5 means the **Generated Answer** has some correct elements but also contains significant inaccuracies or omissions when compared to the **Ground Truth Answer**.
* 1.0 means the **Generated Answer** is perfectly correct, factually accurate, and complete with respect to the **Ground Truth Answer**.

**Reasoning (Optional but Recommended):**
Explain your score by highlighting any factual inaccuracies, omissions, or (if evaluating conciseness) unnecessary information in the **Generated Answer** when compared to the **Ground Truth Answer**.

Please provide a response in a structured JSON format that matches the following format:
{{
  "reasoning": <Your brief explanation>,
  "score": <Your Score as a float, e.g., 0.5>
}}

"""