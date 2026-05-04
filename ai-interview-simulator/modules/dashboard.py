"""
Dashboard — renders the performance tracking charts and analytics.
Uses Plotly for interactive visualizations.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.config import SCORE_THRESHOLDS


def _score_color(score: float) -> str:
    """Return a color string based on the score value."""
    if score >= SCORE_THRESHOLDS["excellent"]:
        return "#2ecc71"   # green
    elif score >= SCORE_THRESHOLDS["good"]:
        return "#f39c12"   # orange
    else:
        return "#e74c3c"   # red


def render_score_gauge(score: float, label: str = "Overall Score"):
    """Render a gauge chart showing a single score value."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": label, "font": {"size": 18}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": _score_color(score)},
            "steps": [
                {"range": [0, SCORE_THRESHOLDS["needs_improvement"]], "color": "#fadbd8"},
                {"range": [SCORE_THRESHOLDS["needs_improvement"], SCORE_THRESHOLDS["good"]], "color": "#fdebd0"},
                {"range": [SCORE_THRESHOLDS["good"], 100], "color": "#d5f5e3"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))
    fig.update_layout(height=260, margin=dict(t=40, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)


def render_dimension_radar(evaluations: list[dict]):
    """Render a radar chart showing average scores across evaluation dimensions."""
    if not evaluations:
        return

    avg_correctness = sum(e.get("correctness", 0) for e in evaluations) / len(evaluations)
    avg_clarity = sum(e.get("clarity", 0) for e in evaluations) / len(evaluations)
    avg_depth = sum(e.get("depth", 0) for e in evaluations) / len(evaluations)

    categories = ["Correctness", "Clarity", "Depth"]
    values = [avg_correctness, avg_clarity, avg_depth]
    # Close the radar loop
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(52, 152, 219, 0.3)",
        line=dict(color="#3498db", width=2),
        name="Your Performance",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Skill Dimension Breakdown",
        height=350,
        margin=dict(t=60, b=20, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_per_question_scores(evaluations: list[dict], questions: list[str]):
    """Render a bar chart showing the overall score for each question."""
    if not evaluations:
        return

    labels = [f"Q{i+1}" for i in range(len(evaluations))]
    scores = [e.get("overall_score", 0) for e in evaluations]
    colors = [_score_color(s) for s in scores]

    fig = go.Figure(go.Bar(
        x=labels,
        y=scores,
        marker_color=colors,
        text=[f"{s:.1f}" for s in scores],
        textposition="outside",
        hovertext=[f"Q{i+1}: {q[:80]}..." for i, q in enumerate(questions)],
        hoverinfo="text+y",
    ))
    fig.update_layout(
        title="Score per Question",
        xaxis_title="Question",
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 110]),
        height=320,
        margin=dict(t=50, b=30, l=40, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_history_chart(history: list[dict]):
    """
    Render a line chart of overall scores across past sessions.
    Each point is one completed interview session.
    """
    if not history:
        st.info("Complete your first interview session to see performance trends here.")
        return

    df = pd.DataFrame([
        {
            "Session": f"#{i+1}\n{h.get('role', '')}\n({h.get('difficulty', '')})",
            "Score": h.get("overall_score", 0),
            "Role": h.get("role", ""),
            "Difficulty": h.get("difficulty", ""),
            "Date": h.get("date", ""),
        }
        for i, h in enumerate(history)
    ])

    fig = px.line(
        df, x="Session", y="Score",
        markers=True,
        title="Performance Over Time",
        labels={"Score": "Overall Score (0–100)"},
        hover_data={"Role": True, "Difficulty": True, "Date": True},
    )
    fig.update_traces(line=dict(color="#3498db", width=2), marker=dict(size=10))
    fig.update_layout(
        yaxis=dict(range=[0, 105]),
        height=350,
        margin=dict(t=50, b=40, l=40, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_strengths_weaknesses(strengths: list[str], weaknesses: list[str]):
    """Display strengths and improvement areas in two columns."""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Strengths")
        if strengths:
            for s in strengths[:6]:
                st.success(f"✓ {s}")
        else:
            st.write("Complete a session to see your strengths.")
    with col2:
        st.markdown("#### Areas to Improve")
        if weaknesses:
            for w in weaknesses[:6]:
                st.warning(f"→ {w}")
        else:
            st.write("Complete a session to see improvement suggestions.")
