import os
import json
from pathlib import Path
import streamlit as st
from streamlit_card import card

st.set_page_config(
    page_title="AI Chatbot 🤖",
    page_icon="🤖",
)

st.title("AI Chatbot")

# load the topics from the json file
with open(Path("topics.json"), "r") as f:
    topics = json.load(f)

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
system_prompt = f"""I am an AI assistant, ask me anything!"""


# function that loads the vectorstore from the local directory
def load_vectorstore():
    vectorstore = Chroma(persist_directory="db_document_embeddings",embedding_function=OpenAIEmbeddings())
    return vectorstore

def create_response(vectorstore):
    # condense_question_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. 
    # Also add semantic keywords associated with the question. For example, if the question is "who is suing who?", the semantic keywords could be "plaintiff", "defendant", etc. add these keywords to the end of the question, separated by commas.
    # If you don't know the answer, answer with your own best guess.
    
    # Chat History:
    # {chat_history}
    # Follow Up Input: {question}
    # Standalone question:"""

    # CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question_template)

    # qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever = vectorstore.as_retriever(), memory=st.session_state['memory'], return_source_documents=True, condense_question_prompt=CONDENSE_QUESTION_PROMPT)
    # response = qa_chain({"question": query})
    # generate a response using the history
    chat = ChatOpenAI(model='gpt-3.5-turbo-16k')
    messages = st.session_state['memory'].chat_memory.messages
    new_msg = chat.invoke(messages).content
    st.session_state['memory'].chat_memory.add_ai_message(new_msg)

    #debug, st.write the source documents
    # st.write(response["source_documents"])

    return new_msg

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

cc = st.columns(3)

# check if already_prompted is set, if not set it to false
if 'already_prompted' not in st.session_state:
    st.session_state['already_prompted'] = ""

prompt_to_start = ""
def setPromptToStart(prompt):
    global prompt_to_start
    prompt_to_start = prompt

    # if the previous prompt is the same as the current prompt, then set it to empty
    if st.session_state['already_prompted'] == prompt:
        prompt_to_start = ""
    st.session_state['already_prompted'] = prompt

# sidebar
st.sidebar.write("Or, select a topic from the list below:")
if st.sidebar.button(topics["sidebar_topic_1"],type="primary"):
    setPromptToStart(topics["sidebar_topic_1"])
if st.sidebar.button(topics["sidebar_topic_2"],type="primary"):
    setPromptToStart(topics["sidebar_topic_2"])
if st.sidebar.button(topics["sidebar_topic_3"],type="primary"):
    setPromptToStart(topics["sidebar_topic_3"])
if st.sidebar.button(topics["sidebar_topic_4"],type="primary"):
    setPromptToStart(topics["sidebar_topic_4"])
if st.sidebar.button(topics["sidebar_topic_5"],type="primary"):
    setPromptToStart(topics["sidebar_topic_5"])
if st.sidebar.button(topics["sidebar_topic_6"],type="primary"):
    setPromptToStart(topics["sidebar_topic_6"])


theme_card = {'bgcolor': '#FFF0F0','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
card_style = {"card": {
            "width": "160px",
            "height": "100px",
            "border-radius": "5px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
            "margin": "1px",
        },"text": {
            "font-size": "1.0rem",
        }}

with cc[0]:
    # hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral', key="card1", theme_override=theme_card, content_text_size="1.0rem", title_text_size="1.0rem")
    card_topic_1_clicked = card(
        title= topics["card_topic_1"],
        text="e",
        key="card1",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_1"])
    )
    card_topic_4_clicked = card(
        title=topics["card_topic_4"],
        text="",
        key="card2",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_4"])
    )
with cc[1]:
    # hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral', key="card2", theme_override=theme_card, content_text_size="1.0rem", title_text_size="1.0rem")
    card_topic_2_clicked = card(
        title= topics["card_topic_2"],
        text="",
        key="card3",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_2"])
    )
    card_topic_5_clicked = card(
        title=topics["card_topic_5"],
        text="",
        key="card4",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_5"])
    )
with cc[2]:
    # hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral', key="card3", theme_override=theme_card, content_text_size="1.0rem", title_text_size="1.0rem")
    card_topic_3_clicked = card(
        title=topics["card_topic_3"],
        text="",
        key="card5",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_3"])
    )
    card_topic_6_clicked = card(
        title=topics["card_topic_6"],
        text="",
        key="card6",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart(topics["card_topic_6"])
    )

# display radio buttons to choose psychologist
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
psychologist_selected = st.radio("Choose your Psychologist:",("Dr. Huang","Dr. Wong","Ms. Amy"))

# add a speech to text button
prompt_audio = ""
audio_bytes = audio_recorder(text="Click to speak!", sample_rate=44100,key="voice")
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
    prompt_audio = transcript.text

    # clear audio bytes
    if 'voice' in st.session_state:
         del st.session_state['voice']

def populate_chat():
    # array to hold chat messages
    chat_messages = []

    # chat template
    for index, message in enumerate(st.session_state['memory'].load_memory_variables({})['chat_history']):

        if isinstance(message, HumanMessage):      
            # with ph:             
                human_msg = st.chat_message("human")
                human_msg.write(message.content)
                # add the message to the chat messages array
                chat_messages.append(human_msg)
        elif isinstance(message, AIMessage):
            # with ph: 
                ai_msg = st.chat_message("ai")
                ai_msg.write(message.content)
                chat_messages.append(ai_msg)

    return chat_messages

# clear chat button
if st.button('Clear Chat'):
    st.session_state['memory'].chat_memory.clear()
    st.session_state['memory'].chat_memory.add_ai_message(system_prompt)

# input
prompt = st.chat_input("Say something")
if prompt or prompt_to_start != "" or prompt_audio != "":
    # check which prompt to use
    if prompt_to_start:
        prompt = prompt_to_start
        prompt_to_start = ""

    # check if audio was used
    if prompt_audio:
        prompt = prompt_audio
        prompt_audio = ""

    # add message to history
    st.session_state['memory'].chat_memory.add_user_message(prompt)

    # populate the chat
    populate_chat()
    with st.spinner("Waiting for response..."):
        new_message = create_response(vectorstore)
        ai_msg = st.chat_message("ai")
        ai_msg.write(new_message)
else:
    populate_chat()