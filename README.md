Here’s a professional `README.md` for your AI Personal Assistant project. It explains the purpose, current features, setup instructions, and future development (including HTML/CSS/JS + FastAPI integration):

---

````markdown
# 🤖 AI Personal Assistant (Ongoing Project)

This is an intelligent **AI Personal Assistant** application developed using **Streamlit** and powered by **Groq's LLaMA 3 API**. It can **remember the user**, provide **location-based responses**, store **reminders and personal notes**, fetch **Chrome browsing history**, list **recently opened files**, and show **system information** — all in an easy-to-use chat-like interface.

---
c:\Users\haris\Pictures\Screenshots\Screenshot 2025-06-14 120617.png 
c:\Users\haris\Pictures\Screenshots\Screenshot 2025-06-14 120551.png
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
````

### 2. Install Dependencies

Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

> You can generate `requirements.txt` using:
>
> ```bash
> pip freeze > requirements.txt
> ```

### 3. Run the App

```bash
streamlit run main.py
```

### 4. Optional: Set Your Groq API Key

Replace `GROQ_API_KEY` in the `main.py` file or store it in an `.env` file and load using `python-dotenv`.

---

## 📅 Future Enhancements (Planned)

✅ Replace or augment frontend with **HTML, CSS, JS** for a modern interface
✅ Build robust **FastAPI backend** for data handling and AI interaction
✅ Secure Groq API key using **environment variables**
✅ Add **user login system** with SQLite or Firebase
✅ Sync reminders/notes to the cloud
✅ Integrate **voice input/output** for hands-free assistant interaction
✅ Package as a **desktop app** using Electron or PyInstaller

---

## 📁 Project Structure (Current)

```bash
.
├── main.py                 # Main Streamlit App
├── assistant_memory.json   # Memory storage (user name/location)
├── reminders.json          # Task reminders
├── notes.json              # User notes
├── session_history.json    # Chat history
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## 🔐 Disclaimer

> This is a **personal project under active development** and not intended for production use.
> Access to Chrome history and local files is limited to the machine running the app.

---

## 👨‍💻 Author

**Harish R.**
3rd Year Student, Artificial Intelligence & Data Science
St. Joseph’s Institute of Technology

---

## 🛠️ Contribute

Pull requests are welcome! Feel free to fork and suggest improvements.

---

---

### ✅ Instructions for Use:

1. Save this as `README.md` in your project root.
2. Update your GitHub repo link if available.
3. When you integrate FastAPI and frontend files (HTML/CSS/JS), this README can evolve into a multi-module documentation.

Would you like a simple `requirements.txt` file generated from this project too?
```
