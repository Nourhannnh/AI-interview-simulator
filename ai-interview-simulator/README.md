# AI Interview Coach for Tech Roles

Preparing for technical interviews can feel random and stressful — this project aims to make it more structured and realistic.

This is a **Python + Streamlit web app** that simulates technical interviews using AI. It generates role-specific questions, evaluates your answers, and helps you understand where you stand and how to improve.

## 🚀 What this project does

Instead of just practicing questions blindly, you can:

- Get **interview questions tailored** to your role and level  
- Answer them in real-time  
- Receive **detailed AI feedback** on your performance  
- Track your progress over multiple sessions  

## 🧠 Features

- **Dynamic Question Generation**  
  Questions are generated based on your selected role and difficulty level.

- **AI Answer Evaluation**  
  Your answers are evaluated across:
  - correctness  
  - clarity  
  - depth  

- **Actionable Feedback**  
  Each response includes:
  - a score  
  - strengths  
  - areas to improve  
  - a sample "better" answer  

- **Performance Dashboard**  
  Visualize your progress over time using charts.

- **Clean, Modular Codebase**  
  Organized structure with separated logic for scalability and readability.

## 💼 Supported Roles

- Software Engineer  
- Data Scientist  
- Machine Learning Engineer  
- Frontend / Backend / Full Stack Developer  
- DevOps Engineer  
- Cloud Architect  
- Data Engineer  
- Technical Product Manager  

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| UI | Streamlit |
| AI | OpenAI API |
| Data | Pandas |
| Visualization | Plotly |
| Language | Python 3.11+ |

## 📁 Project Structure

```
ai-interview-coach/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── modules/
│   ├── config.py
│   ├── session_manager.py
│   ├── question_generator.py
│   ├── answer_evaluator.py
│   └── dashboard.py
└── .gitignore
```

## ⚙️ How to run locally

### 1. Clone the repo
```
git clone <your-repo-url>
cd ai-interview-coach
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

> The `.env` file is ignored by git and won't be uploaded.

### 4. Run the app
```
streamlit run app.py
```

## ☁️ Deployment (Streamlit Cloud)

1. Push your repo to GitHub  
2. Go to Streamlit Cloud  
3. Connect your repo  
4. Add your `OPENAI_API_KEY` in secrets  
5. Deploy 🚀  

## 📊 How scoring works

Each answer is evaluated based on:

- **Correctness (50%)** → Is the answer technically accurate?  
- **Clarity (25%)** → Is it well-structured and easy to follow?  
- **Depth (25%)** → Does it show deeper understanding?  

## 💡 Why I built this

I wanted a way to practice interviews that goes beyond static questions — something interactive that actually **helps you improve**, not just test you.

## Note

This project can be run locally using Streamlit. Deployment is not included due to platform limitations, but the full functionality is available in the codebase.

## 📄 License

MIT  
