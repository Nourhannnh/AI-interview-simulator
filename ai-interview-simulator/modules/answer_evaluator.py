"""
Answer Evaluator — uses OpenAI to assess the quality of a user's interview answer.
Returns structured feedback with scores, strengths, and improvement suggestions.
"""

import os
import json
import openai
from modules.config import AI_MODEL, AI_MAX_TOKENS


def _get_client() -> openai.OpenAI:
    """Build an OpenAI client using Replit's AI Integrations proxy env vars."""
    return openai.OpenAI(
        base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY", ""),
    )


def evaluate_answer(role: str, difficulty: str, question: str, answer: str) -> dict:
    """
    Evaluate a candidate's answer to an interview question.

    Scoring dimensions:
        - correctness  (0–100): Technical accuracy of the answer
        - clarity      (0–100): How clearly and concisely it is expressed
        - depth        (0–100): Breadth of knowledge and detail shown

    Args:
        role:       The job role being interviewed for
        difficulty: Interview difficulty level
        question:   The interview question asked
        answer:     The candidate's answer text

    Returns:
        A dict with keys:
            overall_score   (float): Weighted average of the three dimensions
            correctness     (int):   Score 0–100
            clarity         (int):   Score 0–100
            depth           (int):   Score 0–100
            verdict         (str):   One-line summary verdict
            strengths       (list):  What the candidate did well
            improvements    (list):  Specific suggestions to improve
            ideal_answer    (str):   A brief model answer for reference
    """
    client = _get_client()

    system_prompt = (
        "You are a senior technical interviewer evaluating a candidate's interview answer. "
        "Be rigorous but fair. Always return ONLY valid JSON — no markdown, no extra text."
    )

    user_prompt = f"""
Evaluate the following interview answer and return a JSON object with exactly these fields:
{{
  "correctness": <integer 0-100>,
  "clarity": <integer 0-100>,
  "depth": <integer 0-100>,
  "verdict": "<one concise sentence summarising the answer quality>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<specific improvement 1>", "<specific improvement 2>"],
  "ideal_answer": "<a brief 2-4 sentence model answer>"
}}

Context:
- Role: {role}
- Difficulty: {difficulty}

Question:
{question}

Candidate's Answer:
{answer if answer.strip() else "(No answer provided)"}

Scoring guide:
- correctness: Is the answer technically accurate and complete?
- clarity: Is the answer well-structured, clear, and concise?
- depth: Does the answer show deeper understanding, examples, or trade-off awareness?
"""

    # --- Call the LLM ---
    response = client.chat.completions.create(
        model=AI_MODEL,
        max_completion_tokens=AI_MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw = response.choices[0].message.content.strip()
    result = json.loads(raw)

    # --- Compute weighted overall score ---
    correctness = result.get("correctness", 0)
    clarity = result.get("clarity", 0)
    depth = result.get("depth", 0)
    overall = (correctness * 0.50) + (clarity * 0.25) + (depth * 0.25)
    result["overall_score"] = round(overall, 1)

    return result
