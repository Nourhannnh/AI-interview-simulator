"""
Configuration constants for the AI Interview Simulator.
Defines supported roles, difficulty levels, and evaluation criteria.
"""

# Tech roles available for interview simulation
ROLES = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Cloud Architect",
    "Data Engineer",
    "Product Manager (Technical)",
]

# Difficulty levels and their descriptions
DIFFICULTY_LEVELS = {
    "Junior": "Entry-level questions covering fundamentals and basic concepts.",
    "Mid-level": "Intermediate questions covering practical experience and problem-solving.",
    "Senior": "Advanced questions covering system design, architecture, and leadership.",
}

# Number of questions per session
QUESTIONS_PER_SESSION = 5

# Scoring rubric weights
SCORE_WEIGHTS = {
    "correctness": 0.50,
    "clarity": 0.25,
    "depth": 0.25,
}

# Minimum score thresholds
SCORE_THRESHOLDS = {
    "excellent": 85,
    "good": 70,
    "needs_improvement": 50,
}

# AI model to use (via Replit AI Integrations proxy)
AI_MODEL = "gpt-5.1"
AI_MAX_TOKENS = 1024
