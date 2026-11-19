import streamlit as st
from groq import Groq
import streamlit as st
st.set_page_config(page_title = "AI Interview", page_icon = '🫡', layout= 'centered')
st.title("AI Interview Assistant")
st.caption("practice and prepare for your Placements")
st.caption("launched by Ameer khan")
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
mode = st.radio('Activity', ['generate questions', 'generate code questions', 'evaluate answer','improve answers'])
if mode == 'generate questions':
  count = st.slider(1,10,5)
elif mode == 'generate code questions':
  topic = st.selectbox('Topics', ['SQL','AIML','Python','DSA','c++/c','Java','cyber security','ML'])
  count = st.slider("Number od question",1,10,5)
else:
  question = st.text_area('Enter interview question here ')
  answer = st.text_area('enter your answer ', height = 160)

if st.button("Generate AI Response",type ="primary"):
  if mode in ["Evaluate Answer", "Improve Answer"] and (
    not question.strip() or not answer.strip()
):
     st.warning("Please enter a vaild Question and Answer")
     st.stop()
  if mod == "generate Questions":
     task  = "generate" + str(count) + "Frequently asked Interview Questions 3 theory and 2 conceptual.do not give answer.give hints"
  elif mode == "'generate code questions":
     task = "generate"+ str(count) + "Frequently asked coding Questions on topic" + topic +"anything related to the topic python coding"
  elif mode == "evaluate answer":
     task = "question :" + question + "MY Answer : " + answer + "Evalute this answer based on concept, relevence , communication, length of answe. give each rating out of 5 in a list. "
  elif mode == "improve answers":
     task = "question :" + question + "MY Answer : " + answer + "imporve the answern based oon choice on words key words to include. do not invent anything about candidate "
  background = ="Job role:" +role+ "Difficulti level "+level 
  with st.spinner(" generating your answer .... "):
     try:
       response = client.chat.completions.create(
         model = gen_model,
         messages = [{"role":"system","content":"Act as a senoir interviewer , both HR and technicall expert"},
                     {"role" : "user",
                     "content" : backgroound + task }],
         temprature = 0.7,
         max_tokens = 2000)
         output = response.choives[0].message.content
         st.subheader("AI Response")
         st.markdown(output)
         st.downloads_button("Download Response", output, file_name = "interview_Response.txt",mime = "text/plain" )
     except Exception as e:
        st.error ("API connection was unsuccessful : ",e)
        st.info ("Please check your API Key   and rate limits")
st.caption("Powered by Streamlit.io and GitHub.using LLM API")
         
  


  
