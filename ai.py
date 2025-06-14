import streamlit as st
import os
import requests
import json
import sqlite3
import shutil
import platform
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import tempfile

# ----------- CONFIG -----------
GROQ_API_KEY = "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"  # Replace with your actual Groq API key
MEMORY_FILE = "assistant_memory.json"
REMINDERS_FILE = "reminders.json"
NOTES_FILE = "notes.json"
HISTORY_FILE = "session_history.json"
CHROME_HISTORY_PATH = r"C:\Users\haris\AppData\Local\Google\Chrome\User Data"
RECENT_DIR = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
# ------------------------------

# ===== Type Definitions =====
MemoryData = Dict[str, str]
Reminder = Dict[str, str]
Note = Dict[str, str]
HistoryEntry = Dict[str, Union[str, int]]
SystemInfo = Dict[str, str]

# ===== File Handling =====
def load_json(file: str) -> Union[Dict, List]:
    """Load JSON data from file with error handling."""
    try:
        if os.path.exists(file):
            with open(file, "r") as f:
                return json.load(f)
        return [] if file in [REMINDERS_FILE, NOTES_FILE, HISTORY_FILE] else {}
    except (json.JSONDecodeError, IOError) as e:
        st.error(f"Error loading {file}: {str(e)}")
        return [] if file in [REMINDERS_FILE, NOTES_FILE, HISTORY_FILE] else {}

def save_json(file: str, data: Union[Dict, List]) -> None:
    """Save data to JSON file with error handling."""
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
    except (TypeError, IOError) as e:
        st.error(f"Error saving to {file}: {str(e)}")

# ===== Memory Functions =====
def load_memory() -> MemoryData:
    """Load user memory data."""
    return load_json(MEMORY_FILE)

def save_memory(data: MemoryData) -> None:
    """Save user memory data."""
    save_json(MEMORY_FILE, data)

def remember_user(name: str, location: str) -> None:
    """Store user information in memory."""
    memory = load_memory()
    memory['name'] = name
    memory['last_location'] = memory.get('current_location', "")
    memory['current_location'] = location
    save_memory(memory)

# ===== Location Services =====
def get_location() -> str:
    """Get current location using IP API."""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return f"{data['city']}, {data['regionName']}, {data['country']}"
        return "Unknown"
    except (requests.RequestException, KeyError):
        return "Unknown"

# ===== Chrome History =====
def convert_chrome_time(chrome_time: int) -> str:
    """Convert Chrome timestamp to readable format."""
    epoch_start = datetime(1601, 1, 1)
    microseconds = chrome_time
    try:
        timestamp = epoch_start + timedelta(microseconds=microseconds)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    except (OverflowError, TypeError):
        return "Unknown time"

def get_recent_history() -> List[HistoryEntry]:
    """Get recent Chrome browsing history."""
    try:
        if not os.path.exists(CHROME_HISTORY_PATH):
            return [{"title": "Chrome data not found", "url": "", "visits": 0, "time": ""}]

        profiles = [
            f for f in os.listdir(CHROME_HISTORY_PATH) 
            if os.path.isdir(os.path.join(CHROME_HISTORY_PATH, f)) 
            and (f.startswith("Default") or f.startswith("Profile"))
        ]

        if not profiles:
            return [{"title": "No Chrome profiles found", "url": "", "visits": 0, "time": ""}]

        history_entries = []
        
        for profile in profiles:
            history_path = os.path.join(CHROME_HISTORY_PATH, profile, "History")
            if not os.path.exists(history_path):
                continue

            # Use tempfile for safer temporary file handling
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                shutil.copy2(history_path, temp_path)
                
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                # Try the new Chrome history format first, fallback to old format
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
                    if not cursor.fetchone():
                        continue

                    cursor.execute("""
                        SELECT url, title, visit_count, last_visit_time
                        FROM urls
                        ORDER BY last_visit_time DESC
                        LIMIT 10
                    """)

                    for row in cursor.fetchall():
                        url, title, visit_count, last_visit_time = row
                        history_entries.append({
                            "title": title or "No Title",
                            "url": url,
                            "visits": visit_count,
                            "time": convert_chrome_time(last_visit_time)
                        })

                except sqlite3.Error as e:
                    st.error(f"SQLite error: {str(e)}")
                
                conn.close()
                
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

        return history_entries[:10] if history_entries else [
            {"title": "No history entries found", "url": "", "visits": 0, "time": ""}
        ]

    except Exception as e:
        st.error(f"Error accessing Chrome history: {str(e)}")
        return [{"title": "Error accessing history", "url": str(e), "visits": 0, "time": ""}]

# ===== Recent Files =====
def get_recent_files() -> List[str]:
    """Get list of recently opened files."""
    try:
        if os.path.exists(RECENT_DIR):
            return [
                f for f in os.listdir(RECENT_DIR) 
                if not f.startswith('.') and os.path.isfile(os.path.join(RECENT_DIR, f))
            ][:5]
        return ["Recent files folder not found"]
    except Exception as e:
        return [f"Error reading recent files: {str(e)}"]

# ===== Groq API Chat =====
def ask_groq(prompt: str) -> str:
    """Query Groq API with error handling."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        return f"Error connecting to Groq API: {str(e)}"
    except (KeyError, ValueError) as e:
        return f"Error processing API response: {str(e)}"

# ===== System Info =====
def get_system_info() -> SystemInfo:
    """Get basic system information."""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor() or "Unknown",
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Python Version": platform.python_version()
    }

# ===== Streamlit UI Components =====
def setup_user() -> None:
    """Handle user setup flow."""
    memory = load_memory()
    if "name" not in memory:
        name = st.text_input("What's your name?")
        if name:
            location = get_location()
            remember_user(name, location)
            st.success(f"Hi {name} from {location}! Let's get started.")
            st.experimental_rerun()
    else:
        st.info(f"Hello {memory['name']} 👋 (Location: {memory.get('current_location', 'Unknown')})")

def chat_interface() -> None:
    """Handle the main chat interface."""
    user_prompt = st.text_input("💬 Ask me anything...", key="user_input")
    
    if user_prompt:
        with st.spinner("Thinking..."):
            response = ask_groq(user_prompt)
        
        st.write("### 💬 Assistant says:")
        st.write(response)

        # Save to session history
        history = load_json(HISTORY_FILE)
        history.append({
            "q": user_prompt, 
            "a": response, 
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json(HISTORY_FILE, history[-10:])  # Keep only last 10 chats

def create_sidebar() -> None:
    """Create sidebar with quick access panels."""
    with st.sidebar:
        st.header("Quick Access")
        
        if st.button("🔄 Refresh Data"):
            st.experimental_rerun()
            
        if st.button("🧹 Clear Memory"):
            save_memory({})
            st.success("Memory cleared!")
            st.experimental_rerun()

def create_expanders() -> None:
    """Create all expandable panels."""
    memory = load_memory()
    
    with st.expander("📍 Location Info"):
        st.write(f"Last Location: {memory.get('last_location', 'N/A')}")
        st.write(f"Current Location: {memory.get('current_location', get_location())}")

    with st.expander("🌐 Recent Chrome History"):
        history = get_recent_history()
        for item in history:
            st.markdown(f"""
            - **{item['title']}**  
              🔗 [Open URL]({item['url']})  
              🕒 Visited: {item['time']}  
              🔁 Count: {item['visits']}
            """)

    with st.expander("📂 Recent Files Opened"):
        for file in get_recent_files():
            st.write(f"- {file}")

    with st.expander("🧠 Session History"):
        history = load_json(HISTORY_FILE)
        for entry in reversed(history):
            st.markdown(f"**You**: {entry['q']}\n\n**Assistant**: {entry['a']}\n\n---")

    with st.expander("🗓️ Task Reminders"):
        st.subheader("Add Reminder")
        task = st.text_input("Reminder Text", key="reminder_text")
        time = st.date_input("Due Date", key="reminder_date")
        if st.button("Add Reminder", key="add_reminder"):
            reminders = load_json(REMINDERS_FILE)
            reminders.append({"task": task, "due": str(time)})
            save_json(REMINDERS_FILE, reminders)
            st.success("Reminder Added!")
            st.experimental_rerun()

        st.subheader("Your Reminders")
        reminders = load_json(REMINDERS_FILE)
        if reminders:
            for r in reminders:
                st.markdown(f"📌 **{r['task']}** - Due: {r['due']}")
        else:
            st.write("No reminders yet.")

    with st.expander("📝 Personal Notes"):
        note = st.text_area("Add a Note", key="note_text")
        if st.button("Save Note", key="save_note"):
            notes = load_json(NOTES_FILE)
            notes.append({
                "note": note, 
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            save_json(NOTES_FILE, notes)
            st.success("Note Saved!")
            st.experimental_rerun()

        st.subheader("Your Notes")
        notes = load_json(NOTES_FILE)
        if notes:
            for n in notes:
                st.markdown(f"- 📝 {n['note']} *(Saved on {n['time']})*")
        else:
            st.write("No notes yet.")

    with st.expander("💻 System Info"):
        sysinfo = get_system_info()
        for k, v in sysinfo.items():
            st.write(f"**{k}**: {v}")

# ===== Main App =====
def main():
    """Main application function."""
    st.set_page_config(
        page_title="AI Personal Assistant", 
        page_icon="🤖",
        layout="wide"
    )
    st.title("🤖 AI Personal Assistant")
    st.markdown("Ask me anything and I'll remember you, remind you, and assist you!")
    
    create_sidebar()
    setup_user()
    chat_interface()
    create_expanders()
    
    # Footer
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit, Groq AI & Python – by Harish")

if __name__ == "__main__":
    main()