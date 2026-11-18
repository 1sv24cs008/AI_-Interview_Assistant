import streamlit as st
from groq import Groq
import streamlit as st
st.set_page_config(page_title = "AI Interview", page_icon = '🫡', layout= 'centered')
st.title("AI Interview Assistant")
st.caption("practice and prepare for your Placements")
try:
  client = Groq(api_key= st.secrets["GROQ_API_KEY"])
except (KeyError,FileNotFoundError):
    st.error("API Key is missing.Add it in Advanced setting")
    st.stop()
role = st.selectbox("JOB Title",["Software Engineer","Prompt Engineer","DevOps Engineer","other"])
if role == "other":
  st.text_input("Enter your Job Title","XXXXXXX")
role = st.selectbox("Model",["openai/gpt-oss-20b","openai/gpt-oss-120b"])
role = st.selectbox("difficult level", ['bigginer','intermidiate','advance'])




  
