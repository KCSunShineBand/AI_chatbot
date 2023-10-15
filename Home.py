import os
import streamlit as st

st.set_page_config(
    page_title="AI Chatbot 🤖",
    page_icon="🤖",
)

st.title("AI Chatbot")

# sidebar
st.sidebar.write("Select topic")
st.sidebar.info("Topic 1")
st.sidebar.info("Topic 2")
st.sidebar.info("Topic 3")
st.sidebar.info("Topic 4")

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from audio_recorder_streamlit import audio_recorder
import openai

#load environment variables
from dotenv import load_dotenv
load_dotenv()

#define llm to use
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
system_prompt = "Hi, I'm an AI assistant. What would you like to ask me?"


# function that loads the vectorstore from the local directory
def load_vectorstore():
    vectorstore = Chroma(persist_directory="db_document_embeddings",embedding_function=OpenAIEmbeddings())
    return vectorstore

def create_response(vectorstore,query):
    condense_question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. 
    Also add semantic keywords associated with the question. For example, if the question is "who is suing who?", the semantic keywords could be "plaintiff", "defendant", etc. add these keywords to the end of the question, separated by commas.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question_template)

    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever = vectorstore.as_retriever(), memory=st.session_state['memory'], return_source_documents=True, condense_question_prompt=CONDENSE_QUESTION_PROMPT)
    response = qa_chain({"question": query})

    #debug, st.write the source documents
    # st.write(response["source_documents"])

    return response["answer"]

with st.spinner('Initializing memory...'):
    # set the streamlit memory if not already set
    if 'memory' not in st.session_state:
        st.session_state['memory'] = ConversationBufferMemory(memory_key = "chat_history", input_key='question', output_key='answer', return_messages=True)
        st.session_state['memory'].chat_memory.add_ai_message(system_prompt)

with st.spinner('Initializing vectorstore...'):
    vectorstore = load_vectorstore()

# button to clear vectorstore
# if st.button('Rebuild Vectorstore'):
#     st.session_state.pop('vectorstore')
#     st.experimental_rerun()

# warning to tell user to clear vector store if new documents were added
# st.warning('If you have added new documents, please rebuild the vectorstore by clicking the button above.')

# placeholder for the chat messages
chat_messages_ph = st.empty()

#display the chat input
with st.container():
    prompt = st.chat_input("Say something")
    if prompt:
        # create the response
        create_response(vectorstore, prompt)
        # st.session_state['memory'].chat_memory.add_user_message(prompt)

# add a speech to text button
audio_bytes = audio_recorder(sample_rate=44100,key="voice")
if audio_bytes:
    # random file name
    import uuid 
    file_name = uuid.uuid4().hex + ".wav"

    # save the audio to a file
    file = open(file_name, "wb")
    file.write(audio_bytes)
    file.close()

    # open audio in read mode
    file = open(file_name, "rb")

    transcript = openai.Audio.transcribe("whisper-1", file, api_key = os.getenv("OPENAI_API_KEY"))

    # close the file and delete it
    file.close()
    os.remove(file_name)

    # generate the response
    response = create_response(vectorstore, transcript.text)

    # clear audio bytes
    if 'voice' in st.session_state:
         del st.session_state['voice']

for index, message in enumerate(st.session_state['memory'].load_memory_variables({})['chat_history']):
    if isinstance(message, HumanMessage):      
        # with ph:             
            bot_msg = st.chat_message("assistant")
            bot_msg.write(message.content)
    elif isinstance(message, AIMessage):
        # with ph: 
            human_msg = st.chat_message("user")
            human_msg.write(message.content)

# clear chat button
if st.button('Clear Chat'):
    st.session_state['memory'].chat_memory.clear()
    st.session_state['memory'].chat_memory.add_ai_message(system_prompt)
    st.experimental_rerun()