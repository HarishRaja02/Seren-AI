# 🤖 AI Personal Assistant (Ongoing Project)

This is an intelligent **AI Personal Assistant** application developed using **Streamlit** and powered by **Groq's LLaMA 3 API**. It can **remember the user**, provide **location-based responses**, store **reminders and personal notes**, fetch **Chrome browsing history**, list **recently opened files**, and show **system information** — all in an easy-to-use chat-like interface.

---
![Screenshot 2025-06-14 120617](https://github.com/user-attachments/assets/cd43ed8d-6b75-478f-94fe-e295406dee23)

## 🧠 Features

- 📍 **Location Awareness**: Automatically detects user location via IP.
- 💬 **Chat with AI**: Ask any question and get AI-powered responses using the Groq API.
- 🧠 **Memory Storage**: Remembers user's name and location across sessions.
- 🗂️ **Chrome Browsing History**: Displays recent browsing activity.
- 📂 **Recent Files**: Lists recently accessed files from the system.
- 📝 **Personal Notes**: Save and view notes for yourself.
- 🗓️ **Task Reminders**: Add and manage daily task reminders.
- 💻 **System Info**: View your OS, RAM, processor, and Python version.
- 🕓 **Session History**: See your last 10 chat interactions with the assistant.

---

## 🏗️ Tech Stack

- **Frontend (Current)**: `Streamlit` (Python-based UI)
- **Backend (Planned)**: `FastAPI` *(To replace or integrate with Streamlit backend logic)*
- **AI Model**: `Groq LLaMA3-70B` via API
- **Languages Planned**: HTML, CSS, JavaScript (for future enhanced frontend)
- **Database**: JSON file-based storage (for memory, reminders, notes, chat history)
- **Browser History**: SQLite Chrome DB parsing
- **System Monitoring**: `psutil`, `platform`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-personal-assistant.git
cd ai-personal-assistant
