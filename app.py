import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🫡",
    layout="centered",
)

st.title("AI Interview Assistant")
st.caption("A platform for interview preparation and feedback.")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add GROQ_API_KEY to your Streamlit secrets.")
    st.stop()

role_choice = st.selectbox(
    "Job title",
    [
        "Software engineer",
        "Senior software engineer",
        "Data analyst",
        "Prompt engineer",
        "DevOps engineer",
        "Other",
    ],
)

if role_choice == "Other":
    role = st.text_input("Enter your job title", "")
else:
    role = role_choice

model = st.selectbox("Model", ["openai/gpt-oss-20b", "openai/gpt-oss-120b"])
difficulty = st.selectbox("Difficulty level", ["Beginner", "Intermediate", "Advanced"])
mode = st.radio(
    "Activity",
    ["Generate questions", "Generate coding questions", "Evaluate answer", "Improve answer"],
)

if mode == "Generate questions":
    count = st.slider("Number of questions", min_value=1, max_value=10, value=5)
elif mode == "Generate coding questions":
    topic = st.selectbox(
        "Topic",
        ["SQL", "AI/ML", "Python", "DSA", "C/C++", "Java", "Cybersecurity", "Machine learning"],
    )
    count = st.slider("Number of questions", min_value=1, max_value=10, value=5)
else:
    question = st.text_area("Enter the interview question")
    answer = st.text_area("Enter your answer", height=160)

if st.button("Generate AI response", type="primary"):
    if not role.strip():
        st.warning("Please enter a job title.")
        st.stop()

    if mode in ["Evaluate answer", "Improve answer"] and (not question.strip() or not answer.strip()):
        st.warning("Please enter both the question and your answer.")
        st.stop()

    background = f"Job role: {role}. Difficulty level: {difficulty}. "

    if mode == "Generate questions":
        task = (
            f"Generate {count} frequently asked interview questions for this role. "
            "Include a mix of theory and conceptual questions. Do not provide answers; give a hint for each."
        )
    elif mode == "Generate coding questions":
        task = (
            f"Generate {count} frequently asked coding interview questions about {topic} "
            f"at a {difficulty.lower()} level."
        )
    elif mode == "Evaluate answer":
        task = (
            f"Question: {question}\nCandidate's answer: {answer}\n"
            "Evaluate the answer for conceptual accuracy, relevance, communication, and concision. "
            "Give each category a score out of 5 and explain the scores."
        )
    else:
        task = (
            f"Question: {question}\nCandidate's answer: {answer}\n"
            "Improve the answer's wording and identify useful keywords to include. "
            "Do not invent experience or facts about the candidate."
        )

    with st.spinner("Generating your response..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Act as a senior interviewer with both HR and technical expertise.",
                    },
                    {"role": "user", "content": background + task},
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            output = response.choices[0].message.content or "No response was returned."
            st.subheader("AI response")
            st.markdown(output)
            st.download_button(
                "Download response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain",
            )
        except Exception as exc:
            st.error(f"API connection was unsuccessful: {exc}")
            st.info("Please check your API key and rate limits.")

st.caption("Powered by Streamlit and the Groq API.")
