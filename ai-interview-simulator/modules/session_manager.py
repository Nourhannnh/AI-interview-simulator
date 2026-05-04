"""
Session Manager — handles all Streamlit session state.
Provides a clean interface for reading and updating interview session data.
"""

import streamlit as st
from datetime import datetime


def init_session():
    """Initialize all session state keys if they don't already exist."""
    defaults = {
        # Interview setup
        "role": None,
        "difficulty": None,
        "session_started": False,

        # Questions and answers for the current session
        "questions": [],          # List[str] — generated questions
        "current_q_index": 0,     # Which question we're on
        "answers": [],            # List[str] — user's raw answers
        "evaluations": [],        # List[dict] — AI evaluation results

        # Session metadata
        "session_id": None,
        "session_date": None,

        # Historical performance across sessions
        "history": [],            # List[dict] — past session summaries
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_session(role: str, difficulty: str, questions: list[str]):
    """Begin a new interview session with the given role, difficulty, and generated questions."""
    st.session_state.role = role
    st.session_state.difficulty = difficulty
    st.session_state.questions = questions
    st.session_state.current_q_index = 0
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.session_started = True
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.session_date = datetime.now().strftime("%B %d, %Y at %H:%M")


def record_answer(answer: str):
    """Store the user's answer for the current question."""
    st.session_state.answers.append(answer)


def record_evaluation(evaluation: dict):
    """Store the AI evaluation result for the current answer."""
    st.session_state.evaluations.append(evaluation)


def advance_question():
    """Move to the next question."""
    st.session_state.current_q_index += 1


def is_session_complete() -> bool:
    """Return True if all questions have been answered and evaluated."""
    return (
        st.session_state.session_started
        and len(st.session_state.evaluations) == len(st.session_state.questions)
        and len(st.session_state.questions) > 0
    )


def get_current_question() -> str | None:
    """Return the current question text, or None if session not started."""
    idx = st.session_state.current_q_index
    questions = st.session_state.questions
    if questions and idx < len(questions):
        return questions[idx]
    return None


def get_session_summary() -> dict:
    """
    Compute a summary of the current session's scores and feedback.
    Returns a dict with overall score, per-question breakdown, strengths, and weaknesses.
    """
    evals = st.session_state.evaluations
    if not evals:
        return {}

    total_score = sum(e.get("overall_score", 0) for e in evals) / len(evals)

    strengths, weaknesses = [], []
    for e in evals:
        strengths.extend(e.get("strengths", []))
        weaknesses.extend(e.get("improvements", []))

    return {
        "role": st.session_state.role,
        "difficulty": st.session_state.difficulty,
        "date": st.session_state.session_date,
        "session_id": st.session_state.session_id,
        "overall_score": round(total_score, 1),
        "evaluations": evals,
        "questions": st.session_state.questions,
        "answers": st.session_state.answers,
        "strengths": list(dict.fromkeys(strengths)),    # deduplicated
        "weaknesses": list(dict.fromkeys(weaknesses)),  # deduplicated
    }


def save_session_to_history():
    """Persist the current session summary into the history list."""
    summary = get_session_summary()
    if summary:
        st.session_state.history.append(summary)


def reset_session():
    """Clear current interview state so the user can start a new one."""
    for key in ["role", "difficulty", "session_started", "questions",
                "current_q_index", "answers", "evaluations",
                "session_id", "session_date"]:
        st.session_state[key] = None if key in ["role", "difficulty",
                                                  "session_id", "session_date"] else (
            [] if key in ["questions", "answers", "evaluations"] else
            (False if key == "session_started" else 0)
        )
