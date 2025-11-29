import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains import LLMChain
import requests
from langchain.tools import Tool
import data
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from duckduckgo_search import DDGS
from voice import transcribe, text_to_speech
from webscrap import ws
import pandas as pd
from graphs import graph_generator
import re
from mailsender import send_email, create_event

# venv\Scripts\activate
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
WETHER_API_KEY = os.getenv("WETHER_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
)

# ---------------------- UPDATED PROMPT ----------------------------

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful multipurpose AI assistant.
Use ONLY the information provided in the context to answer the user's question.
If the information is not present in the context, simply respond with: "I don't know".

Context:
{context}

Question: {question}
Answer:
"""
)

if "rag_chain" not in st.session_state:
    st.session_state["rag_chain"] = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=data.vector_store.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )

# -----------------------------------------------------------------------------------------------

def get_weather(city: str):
    url = f"https://api.weatherapi.com/v1/current.json?key={WETHER_API_KEY}&q={city}"
    response = requests.get(url)
    data = response.json()
    temp = data['current']['temp_c']
    condition = data['current']['condition']['text']
    return f"Temperature in {city}: {temp}°C, {condition}"

def rag_tool_func(query: str):
    output = st.session_state["rag_chain"]({"query": query})
    result = output['result'][:200]
    return result

def answer_question(question):
    try:
        ddgs = DDGS()
        results = ddgs.text(question, max_results=2)
        if not results:
            return "No results found."

        out_lines = []
        for r in results:
            title = (r.get('title') or r.get('body') or '')[:100]
            url = (r.get('href') or '')[:80]
            snippet = (r.get('body') or '')[:100]
            out_lines.append(f"{title}\n{snippet}\n{url}")

        return "\n\n".join(out_lines)[:300]
    except Exception as e:
        return f"Search error: {e}"

def summarize_text(text):
    return llm.predict(f"Summarize this text: {text}")

def send_email_input_string(input_string: str):
    try:
        to_match = re.search(r"to:\s*(.*?)(?=, subject:|$)", input_string, re.IGNORECASE)
        subject_match = re.search(r"subject:\s*(.*?)(?=, message:|$)", input_string, re.IGNORECASE)
        message_match = re.search(r"message:\s*(.*)", input_string, re.IGNORECASE | re.DOTALL)

        to = to_match.group(1).strip() if to_match else None
        subject = subject_match.group(1).strip() if subject_match else None
        message = message_match.group(1).strip() if message_match else None

        if to and subject and message:
            return send_email(to, subject, message)
        else:
            return "Error: Missing to, subject, or message."

    except Exception as e:
        return f"Error parsing input: {str(e)}"

def schedule_meeting_input_string(input_string: str):
    try:
        parts = input_string.split(",")
        title = parts[0].split("title:")[1].strip()
        description = parts[1].split("description:")[1].strip()
        start_time = parts[2].split("start_time:")[1].strip()
        duration = int(parts[3].split("duration:")[1].strip().replace("'", ""))
        return create_event(title, description, start_time, duration)
    except Exception as e:
        return f"Error parsing meeting input: {str(e)}"

# -----------------------------------------------------------------------------------------------

weather_tool = Tool(
    name="WeatherFetcher",
    func=get_weather,
    description="Fetches current weather information for any city."
)

rag_tool = Tool(
    name="RAG_Tool",
    func=rag_tool_func,
    description="""Use this tool to answer questions using stored documents. 
If it responds with 'I don't know', return the same to the user."""
)

question_tool = Tool(
    name="QA_Tool",
    func=answer_question,
    description="Uses web search to answer questions when RAG_Tool cannot answer."
)

summarization_tool = Tool(
    name="SummarizationTool",
    func=summarize_text,
    description="Summarizes large text into simple and clear points."
)

WebScraper_tool = Tool(
    name="WebScraperTool",
    func=ws,
    description="Use this tool to find product prices or purchase links from Google Shopping."
)

email_tool = Tool(
    name="EmailSender",
    func=send_email_input_string,
    description="Send an email using this format: 'to: <email>, subject: <subject>, message: <message>'."
)

meeting_tool = Tool(
    name="MeetingScheduler",
    func=schedule_meeting_input_string,
    description="Schedules a meeting. Format: 'title: x, description: y, start_time: yyyy-mm-ddTHH:MM:SS, duration: 45'."
)

# -----------------------------------------------------------------------------------------------

tools = [
    weather_tool, rag_tool, question_tool,
    summarization_tool, WebScraper_tool,
    email_tool, meeting_tool
]

# ---------------------- MAIN AGENT PROMPT UPDATED ----------------------------

if "agent" not in st.session_state:
    custom_prompt = """
You are a smart and helpful AI assistant.
Your goal is to assist the user with accurate, clear, and friendly responses.

If RAG_Tool returns "I don't know", then call QA_Tool for additional information.

If the user asks to send an email:
- Never include the assistant’s or developer’s name in the email.
- Use EmailSender with this JSON-like format:
{
    "to": "example@gmail.com",
    "subject": "Subject here",
    "message": "Message body here"
}

Example:
User says: "Send an email to test@gmail.com about the report."
You call:
{
    "to": "test@gmail.com",
    "subject": "Regarding the Report",
    "message": "This is a quick reminder about the report."
}
"""

    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=1)

    st.session_state["agent"] = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )

# ------------------------------ STREAMLIT UI ------------------------------

st.set_page_config(page_title="ProBot", layout="wide")
st.title("ProBot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], caption=msg["content"])
        else:
            st.markdown(msg["content"])

user_select = st.sidebar.selectbox(
    "Choose communication mode:",
    ("Text", "Voice")
)

st.sidebar.subheader("Upload for Visualization")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file and st.sidebar.button("Generate Charts"):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if not df.empty:
        chart_path = graph_generator(df.head(30))
        if not chart_path:
            st.write("No charts were generated")
        else:
            for path in chart_path:
                st.image(path, caption=path)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": path})

if user_select == "Text":
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state["agent"].run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

else:
    uploaded_file = st.audio_input("Record a Voice Message")
    if uploaded_file and st.button("🎤 Confirm Audio"):
        user_input = transcribe(uploaded_file)

        if user_input:
            st.chat_message("user").markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state["agent"].run(user_input)

                    if response.strip():
                        audio_file = text_to_speech(response)
                        st.sidebar.audio(audio_file, format="audio/mp3", auto_play=True)

                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
