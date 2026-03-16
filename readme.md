


 LangGraph + Streamlit Chatbot

A professional, real-time AI chatbot built using **LangGraph** for state management and **Streamlit** for a sleek, responsive frontend. This assistant features a persistent message history during the session and a clean "Welcome" interface for new users.

---

## ✨ Features
* **Streaming Responses:** Real-time message streaming for a "typing" effect.
* **State Management:** Powered by LangGraph's `StateGraph` for robust conversation handling.
* **Clean UI:** Automatic transition from a "Welcome Screen" to the chat interface.
* **Session Persistence:** Keeps track of the conversation history during your stay.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/)
* **LLM:** OpenAI (GPT-4o / GPT-3.5)
* **Environment:** Python 3.10+

## 🚀 Quick Start (Local Development)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up your environment variables:**
Create a `.env` file in the root directory and add your OpenAI API key:
```text
OPENAI_API_KEY=sk-your-key-here

```


4. **Run the app:**
```bash
streamlit run app.py

