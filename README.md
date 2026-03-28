# 🔥 Resume Roaster

> **"Your resume wouldn't survive 6 seconds."** — Let AI tell you why.

Resume Roaster is a brutal, AI-powered application that gives you honestly harsh feedback on your resume. Built with **Streamlit**, **Groq**, and **Llama 3**, it analyzes your content to find weaknesses and provides actionable fixes so recruiters actually notice you.

---

## 📸 Demo Screenshots

| Input Interface | Brutal Roast Output |
|---|---|
| ![Input](screenshots/paste_resume.png) | ![Output](screenshots/roast_output.png) |

---

## ✨ Features

- 📄 **Two Input Modes** — Paste plain text or upload a PDF resume directly.
- 🔥 **Brutally Honest Feedback** — Get an overall score, a harsh roast, identified weaknesses, and step-by-step fixes.
- 🤖 **Powered by Groq + Llama 3 70B** — Lightning-fast processing with one of the world's most powerful open LLMs.
- ⬇️ **Export Your Roast** — Download the feedback as a `.txt` file for offline reading.
- 🖥️ **Modern Web UI** — A clean, dark-themed Streamlit interface.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Groq** | High-performance LLM API (Llama 3 70B) |
| **Streamlit** | Interactive web application framework |
| **pdfplumber** | Robust PDF text extraction |
| **Python** | Core application logic |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- A free **Groq API Key** (Get one at [console.groq.com](https://console.groq.com))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/kokilamariyayi/resume-roaster.git

# Navigate to the project directory
cd resume-roaster

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
resume-roaster/
├── app.py                  # Main Streamlit web application
├── roaster.py              # LLM logic and prompt engineering
├── requirements.txt        # Python dependencies
├── screenshots/            # Demo screenshots for documentation
├── .gitignore              # Files to ignore in Git
└── README.md               # Project documentation
```

---

## 💡 What the Roast Looks Like

> **"Your resume reads like a grocery list, not a career."**

- **🎯 Overall Score:** 4/10
- **🔥 The Roast:** "You've listed 'Proficient in Word' in 2024? That's not a skill, that's a baseline for existence. Your summary is so generic it could be used for a blender manual."
- **❌ What's Weak:** Lack of metrics, missing impact statements, outdated skills.
- **✅ How To Fix It:** Use the STAR method, quantify your achievements with percentages, and remove the 'References available upon request' line (we know).

---

## 👩‍💻 Author



---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
