"""
AI Interview Simulator for Tech Roles
======================================
Main Streamlit application entry point.

Structure:
  - Sidebar:   Role and difficulty selection, session controls
  - Tab 1:     Live interview (question display + answer input)
  - Tab 2:     Results (per-question feedback after session ends)
  - Tab 3:     Dashboard (historical performance analytics)
"""

import streamlit as st

# --- Page config must be the very first Streamlit call ---
st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Module imports (after set_page_config) ---
from modules.config import ROLES, DIFFICULTY_LEVELS, QUESTIONS_PER_SESSION
from modules.session_manager import (
    init_session,
    start_session,
    record_answer,
    record_evaluation,
    advance_question,
    is_session_complete,
    get_current_question,
    get_session_summary,
    save_session_to_history,
    reset_session,
)
from modules.question_generator import generate_questions
from modules.answer_evaluator import evaluate_answer
from modules.dashboard import (
    render_score_gauge,
    render_dimension_radar,
    render_per_question_scores,
    render_history_chart,
    render_strengths_weaknesses,
)

# ── Initialize session state ──────────────────────────────────────────────────
init_session()


# ── Sidebar — setup controls ───────────────────────────────────────────────────
with st.sidebar:
    st.title("🎯 AI Interview Simulator")
    st.caption("Practice tech interviews with real-time AI feedback")
    st.divider()

    st.subheader("Session Setup")

    selected_role = st.selectbox(
        "Select Role",
        options=ROLES,
        index=0,
        help="Choose the tech role you want to be interviewed for.",
    )

    selected_difficulty = st.selectbox(
        "Difficulty Level",
        options=list(DIFFICULTY_LEVELS.keys()),
        index=1,
        help="Choose how challenging the questions should be.",
    )

    st.caption(DIFFICULTY_LEVELS[selected_difficulty])
    st.divider()

    # --- Start / Reset buttons ---
    if not st.session_state.session_started:
        if st.button("Start Interview", type="primary", use_container_width=True):
            with st.spinner(f"Generating {QUESTIONS_PER_SESSION} questions for {selected_role}..."):
                try:
                    questions = generate_questions(selected_role, selected_difficulty)
                    start_session(selected_role, selected_difficulty, questions)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate questions: {e}")
    else:
        st.info(
            f"**Role:** {st.session_state.role}\n\n"
            f"**Level:** {st.session_state.difficulty}\n\n"
            f"**Progress:** {len(st.session_state.evaluations)}/{len(st.session_state.questions)} answered"
        )
        if st.button("New Interview", use_container_width=True):
            reset_session()
            st.rerun()

    st.divider()
    st.caption("Powered by OpenAI · Built with Streamlit")


# ── Main content ───────────────────────────────────────────────────────────────
tab_interview, tab_results, tab_dashboard = st.tabs(
    ["📋 Interview", "📊 Results", "📈 Dashboard"]
)


# ═══════════════════════════════════════════════════════════════
# TAB 1 — INTERVIEW
# ═══════════════════════════════════════════════════════════════
with tab_interview:
    if not st.session_state.session_started:
        # Welcome screen
        st.markdown("## Welcome to AI Interview Simulator")
        st.markdown(
            "Practice real tech interviews with instant AI-powered feedback. "
            "Select your target role and difficulty level on the left, then press **Start Interview**."
        )
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🎙️ Answer Questions")
            st.write("Respond to dynamically generated interview questions tailored to your chosen role.")
        with col2:
            st.markdown("### 🤖 Get AI Feedback")
            st.write("Receive detailed feedback on correctness, clarity, and depth — plus a model answer.")
        with col3:
            st.markdown("### 📈 Track Progress")
            st.write("Monitor your performance across sessions with charts showing strengths and weaknesses.")

    elif is_session_complete():
        # Session done — prompt user to view results
        st.success("Interview complete! Head to the **Results** tab to review your feedback.")
        summary = get_session_summary()
        st.metric("Overall Score", f"{summary['overall_score']:.1f} / 100")

    else:
        # Active interview — show current question
        q_index = st.session_state.current_q_index
        total_q = len(st.session_state.questions)
        question_text = get_current_question()

        st.markdown(f"### Question {q_index + 1} of {total_q}")
        st.progress((q_index) / total_q)
        st.divider()

        # Question card
        st.markdown(f"**{question_text}**")
        st.divider()

        # Answer text area
        answer_key = f"answer_input_{q_index}"
        user_answer = st.text_area(
            "Your Answer",
            key=answer_key,
            height=200,
            placeholder="Type your answer here. Take your time — be as detailed as you like.",
        )

        col_submit, col_skip = st.columns([3, 1])
        with col_submit:
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if not user_answer.strip():
                    st.warning("Please enter an answer before submitting.")
                else:
                    with st.spinner("Evaluating your answer..."):
                        try:
                            evaluation = evaluate_answer(
                                role=st.session_state.role,
                                difficulty=st.session_state.difficulty,
                                question=question_text,
                                answer=user_answer,
                            )
                            record_answer(user_answer)
                            record_evaluation(evaluation)

                            # If this was the last question, save to history
                            if len(st.session_state.evaluations) == total_q:
                                save_session_to_history()
                            else:
                                advance_question()

                            st.rerun()
                        except Exception as e:
                            st.error(f"Evaluation failed: {e}")

        with col_skip:
            if st.button("Skip", use_container_width=True):
                record_answer("(skipped)")
                evaluation = {
                    "correctness": 0, "clarity": 0, "depth": 0,
                    "overall_score": 0.0,
                    "verdict": "Question was skipped.",
                    "strengths": [],
                    "improvements": ["Always attempt to answer — even a partial answer is better than none."],
                    "ideal_answer": "N/A",
                }
                record_evaluation(evaluation)
                if len(st.session_state.evaluations) == total_q:
                    save_session_to_history()
                else:
                    advance_question()
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# TAB 2 — RESULTS
# ═══════════════════════════════════════════════════════════════
with tab_results:
    if not is_session_complete():
        st.info("Complete your interview session to see results here.")
    else:
        summary = get_session_summary()
        evals = summary["evaluations"]
        questions = summary["questions"]
        answers = summary["answers"]

        st.markdown(f"## Results — {summary['role']} ({summary['difficulty']})")
        st.caption(f"Session completed on {summary['date']}")
        st.divider()

        # --- Overall score gauge + radar ---
        col_gauge, col_radar = st.columns(2)
        with col_gauge:
            render_score_gauge(summary["overall_score"], "Overall Score", key="results_gauge")
        with col_radar:
            render_dimension_radar(evals, key="results_radar")

        st.divider()

        # --- Per-question breakdown ---
        render_per_question_scores(evals, questions, key="results_per_question")
        st.divider()

        # --- Detailed per-question accordion ---
        st.subheader("Question-by-Question Feedback")
        for i, (q, a, e) in enumerate(zip(questions, answers, evals)):
            score = e.get("overall_score", 0)
            verdict = e.get("verdict", "")
            with st.expander(f"Q{i+1}: {q[:80]}{'...' if len(q) > 80 else ''} — Score: {score:.1f}/100"):
                st.markdown("**Question:**")
                st.write(q)

                st.markdown("**Your Answer:**")
                st.write(a if a != "(skipped)" else "_Question skipped_")

                st.markdown("**AI Verdict:**")
                st.write(verdict)

                c1, c2, c3 = st.columns(3)
                c1.metric("Correctness", f"{e.get('correctness', 0)}/100")
                c2.metric("Clarity", f"{e.get('clarity', 0)}/100")
                c3.metric("Depth", f"{e.get('depth', 0)}/100")

                if e.get("strengths"):
                    st.markdown("**Strengths:**")
                    for s in e["strengths"]:
                        st.success(f"✓ {s}")

                if e.get("improvements"):
                    st.markdown("**Suggestions for improvement:**")
                    for imp in e["improvements"]:
                        st.warning(f"→ {imp}")

                st.markdown("**Model Answer:**")
                st.info(e.get("ideal_answer", "N/A"))

        st.divider()
        render_strengths_weaknesses(summary["strengths"], summary["weaknesses"])


# ═══════════════════════════════════════════════════════════════
# TAB 3 — DASHBOARD
# ═══════════════════════════════════════════════════════════════
with tab_dashboard:
    st.markdown("## Performance Dashboard")
    st.caption("Track your progress across interview sessions.")
    st.divider()

    history = st.session_state.history

    if not history:
        st.info("No sessions recorded yet. Complete an interview to populate this dashboard.")
    else:
        # Summary metrics
        total_sessions = len(history)
        avg_score = sum(h["overall_score"] for h in history) / total_sessions
        best_score = max(h["overall_score"] for h in history)
        latest_score = history[-1]["overall_score"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Sessions Completed", total_sessions)
        m2.metric("Average Score", f"{avg_score:.1f}")
        m3.metric("Best Score", f"{best_score:.1f}")
        m4.metric("Latest Score", f"{latest_score:.1f}",
                  delta=f"{latest_score - history[-2]['overall_score']:+.1f}" if total_sessions > 1 else None)

        st.divider()

        # Progress over time
        render_history_chart(history, key="dashboard_history")
        st.divider()

        # Latest session breakdown
        latest = history[-1]
        st.subheader(f"Latest Session — {latest['role']} ({latest['difficulty']})")
        col_g, col_r = st.columns(2)
        with col_g:
            render_score_gauge(latest["overall_score"], "Latest Overall Score", key="dashboard_gauge")
        with col_r:
            render_dimension_radar(latest["evaluations"], key="dashboard_radar")

        st.divider()
        render_strengths_weaknesses(latest["strengths"], latest["weaknesses"])

        st.divider()
        # Session history table
        st.subheader("Session History")
        import pandas as pd
        history_df = pd.DataFrame([
            {
                "Date": h.get("date", ""),
                "Role": h.get("role", ""),
                "Difficulty": h.get("difficulty", ""),
                "Score": f"{h['overall_score']:.1f} / 100",
            }
            for h in history
        ])
        st.dataframe(history_df, use_container_width=True, hide_index=True)
