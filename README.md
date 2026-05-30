# AI Interview Simulator

Practice technical interviews with an AI that actually gives you feedback.

Pick a role and difficulty. Get 5 questions. Answer them. See where you were right, where you were vague, and what a better answer looks like. Track your scores across sessions.

Built with Python and Streamlit, powered by OpenAI.

---

## What it does

Select from 10 tech roles — Software Engineer, Data Scientist, ML Engineer, Frontend Developer, Backend Developer, and more — across three difficulty levels: Junior, Mid-level, and Senior.

Each session runs 5 questions. After each answer, the AI scores it on three dimensions:

- **Correctness** — was it technically accurate?
- **Clarity** — was it well-structured and easy to follow?
- **Depth** — did you show real understanding or just surface knowledge?

Overall score is a weighted average: 50% correctness, 25% clarity, 25% depth. At the end you get a full breakdown — what you did well, what to improve, and a model answer for each question.

The Dashboard tab tracks your scores across sessions so you can see whether you're actually improving.

---

## Stack

- Python + Streamlit for the UI
- OpenAI API for question generation and answer evaluation
- Streamlit session state for in-session history tracking

---

## Project structure

```
ai-interview-simulator/
├── app.py                      # Main Streamlit app — all UI and tab logic
├── modules/
│   ├── config.py               # Roles, difficulty levels, scoring weights, model config
│   ├── question_generator.py   # Calls OpenAI to generate role-specific questions
│   ├── answer_evaluator.py     # Calls OpenAI to score answers and return structured feedback
│   ├── session_manager.py      # Manages Streamlit session state
│   └── dashboard.py            # Score gauge, radar chart, history visualizations
└── requirements.txt
```

---

## Setup

Clone the repo:

```
git clone https://github.com/Nourhannnh/AI-interview-simulator.git
cd AI-interview-simulator/ai-interview-simulator
```

Install dependencies:

```
pip install -r requirements.txt
```

Add your OpenAI key to a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

Run:

```
streamlit run app.py
```

---

## How the AI works

**Question generation:** sends the role, difficulty, and number of questions to OpenAI and asks for a JSON array of strings back. Nothing hardcoded — questions are generated fresh every session.

**Answer evaluation:** sends the role, difficulty, question, and answer to OpenAI and asks for a structured JSON response with correctness, clarity, and depth scores, a verdict, strengths, improvement suggestions, and a model answer. The overall score is computed in Python using fixed weights — not by the model — so the math is always consistent regardless of what the model returns.
