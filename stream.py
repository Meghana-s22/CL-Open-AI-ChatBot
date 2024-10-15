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
You are an intelligent chatbot. Respond to the user query in a helpful and polite manner.
Question: {user_question}
Answer:
"""
prompt_template = PromptTemplate(input_variables=["user_question"], template=template)

def get_gemini_response(question):
    prompt = prompt_template.format(user_question=question)
    response = chat.send_message(prompt, stream=True)
    return response


st.set_page_config(page_title="Q&A Demo")
st.header("My ChatBot")


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input: ", key="input")
submit = st.button("Enter")

if submit and input:
    response = get_gemini_response(input)
 
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))


st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
