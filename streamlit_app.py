import streamlit as st

st.set_page_config(
    page_title="Mental Health Chatbot 😷",
    page_icon="😷",
)

st.title("Mental Health Chatbot")

# sidebar
st.sidebar.write("Select topic")
st.sidebar.info("Topic 1")
st.sidebar.info("Topic 2")
st.sidebar.info("Topic 3")
st.sidebar.info("Topic 4")



if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

# chat template
with st.chat_message("assistant"):
    st.write("Hi, I'm a mental health assistant. I can help you with any mental health issues you may have. What would you like to talk about?")

with st.chat_message("user"):
    st.write("Hello 👋")

prompt = st.chat_input("Say something")