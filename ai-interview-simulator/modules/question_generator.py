"""
Question Generator — uses OpenAI to produce role-specific interview questions.
Questions are tailored by role and difficulty level.
"""

import os
import json
import openai
from modules.config import AI_MODEL, AI_MAX_TOKENS, QUESTIONS_PER_SESSION


def _get_client() -> openai.OpenAI:
    """
    Build an OpenAI client pointed at Replit's AI Integrations proxy.
    The proxy injects a real key at runtime via the env vars set during setup.
    """
    return openai.OpenAI(
        base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY", ""),
    )


def generate_questions(role: str, difficulty: str) -> list[str]:
    """
    Generate a list of interview questions for the given role and difficulty.

    Args:
        role: Tech job role (e.g. 'Data Scientist')
        difficulty: Difficulty level ('Junior', 'Mid-level', 'Senior')

    Returns:
        A list of QUESTIONS_PER_SESSION question strings.
    """
    client = _get_client()

    system_prompt = (
        "You are an expert technical interviewer at a top tech company. "
        "Generate realistic, thoughtful interview questions. "
        "Return ONLY a valid JSON array of strings — no extra text, no markdown fences."
    )

    user_prompt = (
        f"Generate exactly {QUESTIONS_PER_SESSION} {difficulty}-level interview questions "
        f"for a {role} position. "
        "The questions should cover a mix of: "
        "technical knowledge, problem-solving, system design (if applicable), "
        "and behavioral/situational scenarios. "
        "Make them specific, realistic, and appropriately challenging for the difficulty level. "
        f"Return a JSON array of {QUESTIONS_PER_SESSION} strings."
    )

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

    # Parse the JSON array returned by the model
    questions = json.loads(raw)

    # Safety: ensure we always return the correct count
    if not isinstance(questions, list):
        raise ValueError("Model did not return a JSON array of questions.")

    return questions[:QUESTIONS_PER_SESSION]
