<div align="center">

# 🆘 DisasterAI

### AI-Powered Disaster Management Chatbot

*Instant, structured, and reliable emergency guidance — powered by RAG + LLaMA-3*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://console.groq.com)
[![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<img src="https://img.shields.io/badge/Status-Active-00d4aa?style=flat-square"/>
<img src="https://img.shields.io/badge/LLM-LLaMA--3.3--70b-ff6b35?style=flat-square"/>
<img src="https://img.shields.io/badge/Free%20API-Groq-orange?style=flat-square"/>

</div>

---

## 📖 About

**DisasterAI** is an intelligent emergency guidance assistant built with **Retrieval-Augmented Generation (RAG)**. It combines official disaster management documents with the power of **LLaMA-3.3-70b** (via Groq's free API) to deliver instant, structured, and actionable safety guidance during natural and man-made disasters.

Whether you're preparing for a **cyclone**, responding to an **earthquake**, treating a **snake bite**, or building an **emergency kit** — DisasterAI provides clear, point-by-point answers grounded in official guidelines.

> 💡 Even without PDF documents, DisasterAI answers every safety question using its built-in AI knowledge — it **never says "I don't know"** for emergency topics.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📚 **RAG Pipeline** | Answers grounded in your official PDF documents |
| 🤖 **Free AI Fallback** | LLaMA-3 via Groq answers anything not in documents |
| 🔍 **FAISS Vector Search** | Lightning-fast semantic similarity search |
| 💬 **Multi-turn Chat** | Remembers conversation context across messages |
| 🌙 **Dark Emergency UI** | High-contrast dark theme optimised for stress situations |
| 📄 **Auto PDF Discovery** | Drop PDFs in `data/` — auto-indexed, no code changes |
| ⚡ **One-click Rebuild** | Rebuild FAISS index instantly from the sidebar |
| 🇮🇳 **India-Specific** | References NDMA, NDRF, SDMA, IMD, helpline 1078 |
| 🏥 **Broad Coverage** | Floods, earthquakes, first aid, survival, and more |

---

## 🧠 How It Works

```
User Query
    │
    ▼
[Condense question with chat history]
    │
    ▼
[FAISS Similarity Search on PDF chunks]
    │
    ├── Score ≥ 0.20 ──► [RAG Mode]      → Answer from your documents
    │                     📚 Document-Grounded badge
    │
    └── Score < 0.20 ──► [Fallback Mode] → LLaMA-3 answers from own knowledge
                          ⚡ AI General Knowledge badge
```

---

## 🗂️ Project Structure

```
DisasterAI/
├── run.bat                     ← Double-click to start everything
├── .env                        ← Your GROQ_API_KEY (never commit)
├── .env.example                ← Template
├── README.md
│
├── data/                       ← Drop your PDF files here
│   └── *.pdf
│
└── streamlit/
    ├── app.py                  ← Streamlit UI & chat interface
    ├── rag_pipeline.py         ← Core RAG engine
    ├── config.py               ← All parameters in one place
    ├── prompts.py              ← LLM prompt templates
    ├── utils.py                ← Helper utilities
    └── faiss_index/            ← Auto-created FAISS index (gitignore this)
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/disaster-management-rag-chatbot.git
cd disaster-management-rag-chatbot
```

### 2. Get a FREE Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free (no credit card needed)
3. Navigate to **API Keys** → Create new key
4. Copy the key

### 3. Configure environment

```bash
copy .env.example .env
```

Open `.env` and add your key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add your PDF documents

Drop any disaster management PDF files into the `data/` folder:
```
data/
├── Disaster management plan.pdf
├── disaster_management_in_india.pdf
└── any_other_guide.pdf
```

> 💡 The app also works **without any PDFs** — it will use AI knowledge only.

### 5. Run the app

```bash
run.bat
```

The script will automatically:
- ✅ Check Python installation
- ✅ Create a virtual environment (`venv/`)
- ✅ Install all dependencies (one-time only)
- ✅ Launch the app at `http://localhost:8501`

---

## 🖥️ Screenshots

> *Dark emergency-focused UI with structured point-by-point answers*

---

## 🔧 Configuration

All settings are in `streamlit/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | `800` | Characters per text chunk |
| `CHUNK_OVERLAP` | `150` | Overlap between chunks |
| `TOP_K` | `5` | Chunks retrieved per query |
| `SIMILARITY_THRESHOLD` | `0.20` | Min score to use RAG mode |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq LLM model |
| `LLM_TEMPERATURE` | `0.2` | Lower = more factual |

---

## 📝 Example Queries

```
"What should I do during a flood?"
"Steps to take during an earthquake?"
"How to prepare an emergency kit?"
"Snake bite first aid treatment"
"What is NDMA's role in disaster management?"
"How to purify water after a disaster?"
"Cyclone preparedness checklist"
"What to do after a tsunami?"
"How to treat burns at home?"
"Disaster Management Act 2005 India"
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM** | LLaMA-3.3-70b via Groq (Free) |
| **RAG Framework** | LangChain |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |
| **Vector Database** | FAISS (local) |
| **PDF Loader** | PyPDF |
| **Language** | Python 3.9+ |

---

## 💻 Terminal Commands

```bash
# Run the app
run.bat

# Rebuild FAISS index (after adding new PDFs)
rmdir /s /q streamlit\faiss_index
run.bat

# Install a missing package
venv\Scripts\pip.exe install <package-name>

# Full reset
rmdir /s /q venv
rmdir /s /q streamlit\faiss_index
run.bat

# Check loaded PDFs
dir data\*.pdf

# Verify API key
type .env
```

---

## ➕ Adding New Documents

1. Copy new `.pdf` files into the `data/` folder
2. Open the running app
3. Click **🔄 Rebuild Index** in the sidebar
4. Wait ~1-2 minutes for re-indexing
5. Ask questions from the new document ✅

No code changes needed — ever.

---

## 🚀 Deployment

To deploy on **Streamlit Cloud**:

1. Push to GitHub (make sure `data/*.pdf` is included)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set main file as `streamlit/app.py`
4. Add `GROQ_API_KEY` in **Secrets** settings
5. Deploy 🎉

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## ⚠️ Disclaimer

DisasterAI provides guidance based on official documents and AI knowledge.
**Always follow instructions from local emergency authorities during an actual disaster.**
For life-threatening emergencies, call your local emergency number immediately.

**India Emergency Helplines:**
- 🚨 National Disaster Helpline: **1078**
- 🚑 Ambulance: **108**
- 🚒 Fire: **101**
- 👮 Police: **100**

---

<div align="center">

Made with ❤️ for disaster preparedness

⭐ Star this repo if it helped you!

</div>
