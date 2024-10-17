from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

template = """
You are an intelligent chatbot. Use the following document content to respond to the user query in a helpful and polite manner.
Document content: {document_content}
Question: {user_question}
Answer:
"""
prompt_template = PromptTemplate(input_variables=["user_question", "document_content"], template=template)


def get_gemini_response(question, document_content):
    prompt = prompt_template.format(user_question=question, document_content=document_content)
    response = chat.send_message(prompt, stream=True)
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("My ChatBot")


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        document_content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        document_content = ""
        for page_num in range(len(pdf_reader.pages)):
            document_content += pdf_reader.pages[page_num].extract_text()


input = st.text_input("Input: ", key="input")
submit = st.button("Enter")

if submit and input and uploaded_file:
    response = get_gemini_response(input, document_content)
    
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
