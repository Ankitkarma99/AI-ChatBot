# **🤖 ProBot AI Assistant**

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)]()
[![LangChain](https://img.shields.io/badge/LangChain-LLM-green)]()
[![Google API](https://img.shields.io/badge/Google-Email_Calendar-purple)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## **📘 Overview**

**ProBot** is a **multipurpose AI assistant** powered by **LangChain + Groq LLM** and **Streamlit**.
It provides **text and voice-based conversation**, can **answer queries using RAG**, **fetch real-time weather**, **send emails**, **schedule meetings**, **analyze CSV/Excel data**, and **scrape product prices**.

---

## **🚀 Features**

* **Text & Voice Chat**: Communicate with ProBot using text or audio.
* **RAG (Retrieval-Augmented Generation)**: Answers questions from stored documents.
* **Web Search**: Fetches real-time answers when RAG cannot respond.
* **Weather Information**: Retrieves current weather for any city.
* **Email Sender**: Send emails using structured input.
* **Meeting Scheduler**: Create Google Calendar events with automatic Meet links.
* **Data Visualization**: Upload CSV/Excel to generate charts automatically.
* **Web Scraping Tool**: Get product prices from Google Shopping.

---

## **🛠 Tech Stack**

| Technology                           | Use                                        |
| ------------------------------------ | ------------------------------------------ |
| **Python 3.11+**                     | Core programming language                  |
| **Streamlit**                        | Web interface                              |
| **LangChain + Groq LLM**             | Natural language understanding + reasoning |
| **Google APIs**                      | Gmail and Calendar integration             |
| **OpenAI / DuckDuckGo / SerpAPI**    | Web search & information retrieval         |
| **Matplotlib / Seaborn / Pandas**    | Data visualization                         |
| **SpeechRecognition / gTTS / pydub** | Voice input/output                         |

---

## **📁 Project Structure**

```
📦 ProBot
 ┣ 📜 app.py               # Streamlit frontend + agent initialization
 ┣ 📜 data.py              # Sample documents for RAG
 ┣ 📜 graphs.py            # Data visualization engine
 ┣ 📜 mailsender.py        # Email & Calendar integration
 ┣ 📜 voice.py             # Speech-to-text & text-to-speech
 ┣ 📜 webscrap.py          # Google Shopping scraper
 ┣ 📜 requirements.txt     # Project dependencies
 ┣ 📜 traffic-policy.yml   # OAuth configuration
 ┗ 📂 README.md
```

---

## **📥 Installation**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/probot.git
cd probot
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
WETHER_API_KEY=your_weather_api_key
SERPAPI_API_KEY=your_serpapi_api_key
GOOGLE_CREDENTIALS='your_google_credentials_json'
GOOGLE_TOKEN_JSON='your_google_token_json'
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## **📄 Usage**

1. **Select Communication Mode**: Text or Voice.
2. **Ask anything**: ProBot responds using documents, web search, or tools.
3. **Upload CSV/Excel** (optional): Generates charts for quick data visualization.
4. **Send Emails**: Input in the format:

```
to: example@gmail.com, subject: Hello, message: This is a test email.
```

5. **Schedule Meetings**: Input in the format:

```
title: Meeting, description: Discuss project, start_time: 2025-12-01T15:00:00, duration: 60
```

6. **Fetch Weather**: Ask "What's the weather in London?"
7. **Web Scraping**: Use ProBot to find products or prices online.

---

## **⚡ Notes**

* Ensure **all API keys** and credentials are correctly set in `.env`.
* Audio input works best in **wav or mp3** formats.
* Charts are generated for the first **30 rows** of uploaded datasets.
* Emails and meetings require **Google OAuth credentials**.

---

## **🤝 Contribution**

Contributions are welcome! You can help by:

* Adding more RAG documents
* Improving voice recognition
* Supporting additional file types for visualization
* Enhancing web scraping functionality

---

## **📜 License**

MIT License

---
