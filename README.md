# 🎓 AI-Powered Study Buddy

An intelligent, all-in-one learning assistant powered by **Google Gemini AI** and built with **Streamlit**. Transform the way you study — explain concepts, summarize notes, generate flashcards, take quizzes, and chat with your AI tutor.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 💡 **Explain Concept** | Enter any topic and get a tailored AI explanation by level (beginner to expert) and style (simple, analogy, step-by-step, narrative) |
| 📝 **Summarize Notes** | Upload PDF/TXT files or paste text to get structured summaries, key takeaways, and a glossary |
| 🎴 **Flashcards** | Auto-generate interactive flip-card decks from any topic or your uploaded notes. Track mastery per card |
| ⚔️ **Quiz Arena** | Generate multiple-choice quizzes with instant grading, correct answers, and detailed explanations |
| 💬 **Study Chat** | Conversational AI tutor with full chat history — ask follow-ups, get code examples, clarify doubts |
| 📂 **Dashboard** | Central hub with a quick overview and navigation to all study tools |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ installed
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/kalyandev-19/ai-study-buddy.git
cd ai-study-buddy
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not present, install manually:
> ```bash
> pip install streamlit PyPDF2 google-genai
> ```

### 5. Run the App

```bash
python -m streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 🗂️ Project Structure

```
ai_study_buddy/
│
├── app.py              # Main Streamlit application & UI
├── utils.py            # Gemini API logic (explain, summarize, flashcards, quiz, chat)
├── styles.css          # Custom dark-theme CSS styling
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| **UI Framework** | [Streamlit](https://streamlit.io/) |
| **AI Model** | [Google Gemini](https://ai.google.dev/) via `google-genai` SDK |
| **PDF Parsing** | [PyPDF2](https://pypdf2.readthedocs.io/) |
| **Styling** | Custom CSS (dark glassmorphism theme) |
| **Language** | Python 3.13 |

---

## 📖 How to Use

### 💡 Explain a Concept
1. Go to the **Explain Concept** tab
2. Type any topic (e.g., *"Quantum Computing"*, *"Photosynthesis"*)
3. Choose your **Audience Level** and **Explanation Style**
4. Click **Explain to Me!**

### 📝 Summarize Notes
1. Go to the **Summarize Notes** tab
2. Upload a `.pdf` or `.txt` file, or paste your notes directly
3. Click **Summarize & Analyze Notes**
4. Get a structured overview, key takeaways, and glossary

### 🎴 Flashcards
1. Go to the **Flashcards** tab
2. Enter a topic or use your uploaded notes
3. Set the number of cards and click **Generate**
4. Flip cards, mark them as learned, and track your mastery score

### ⚔️ Quiz Arena
1. Go to the **Quiz Arena** tab
2. Enter a topic or use uploaded notes
3. Set the number of questions and click **Generate Quiz**
4. Answer all questions and click **Submit My Answers** for instant grading

### 💬 Study Chat
1. Go to the **Study Chat** tab
2. Type your question in the chat box
3. Get AI-powered responses with full conversation history
4. Click **Clear Chat Conversation** to start fresh

---

## 🔐 API Key Configuration

The app uses a **pre-configured Gemini API Key** stored in the session state inside `app.py`.

To use your own API key, open `app.py` and update line 21:

```python
"api_key": "YOUR_GEMINI_API_KEY_HERE",
```

Get a free API key at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## 📦 Requirements

```
streamlit
PyPDF2
google-genai
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs via [Issues](https://github.com/kalyandev-19/ai-study-buddy/issues)
- 💡 Suggest features or improvements
- 🔀 Submit Pull Requests

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

## 👨‍💻 Author

**Kalyan** — [@kalyandev-19](https://github.com/kalyandev-19)

---

> 🌟 *Star this repo if you found it helpful!*
