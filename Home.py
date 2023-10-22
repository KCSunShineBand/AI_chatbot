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

# sidebar
st.sidebar.write("Or, select a topic from the list below:")
if st.sidebar.button(topics["sidebar_topic_1"],type="primary"):
    prompt_to_start = topics["sidebar_topic_1"]
if st.sidebar.button(topics["sidebar_topic_2"],type="primary"):
    prompt_to_start = topics["sidebar_topic_2"]
if st.sidebar.button(topics["sidebar_topic_3"],type="primary"):
    prompt_to_start = topics["sidebar_topic_3"]
if st.sidebar.button(topics["sidebar_topic_4"],type="primary"):
    prompt_to_start = topics["sidebar_topic_4"]
if st.sidebar.button(topics["sidebar_topic_5"],type="primary"):
    prompt_to_start = topics["sidebar_topic_5"]
if st.sidebar.button(topics["sidebar_topic_6"],type="primary"):
    prompt_to_start = topics["sidebar_topic_6"]


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

def create_response(vectorstore,query):
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

    # add the user message to the memory
    st.session_state['memory'].chat_memory.add_user_message(query)

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

prompt_to_start = None
def setPromptToStart(prompt):
    global prompt_to_start
    prompt_to_start = prompt

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
        url="",
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
        on_click=lambda: setPromptToStart()
    )
with cc[1]:
    # hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral', key="card2", theme_override=theme_card, content_text_size="1.0rem", title_text_size="1.0rem")
    card_topic_2_clicked = card(
        title= topics["card_topic_2"],
        text="",
        key="card3",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart()
    )
    card_topic_5_clicked = card(
        title=topics["card_topic_5"],
        text="",
        key="card4",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart()
    )
with cc[2]:
    # hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral', key="card3", theme_override=theme_card, content_text_size="1.0rem", title_text_size="1.0rem")
    card_topic_3_clicked = card(
        title=topics["card_topic_3"],
        text="",
        key="card5",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart()
    )
    card_topic_6_clicked = card(
        title=topics["card_topic_6"],
        text="",
        key="card6",
        image="",
        styles=card_style,
        on_click=lambda: setPromptToStart()
    )

# display radio buttons to choose psychologist
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
psychologist_selected = st.radio("Choose your Psychologist:",("Dr. Huang","Dr. Wong","Ms. Amy"))

#display the chat input
with st.container():
    prompt = st.chat_input("Say something")
    if prompt:
        # create the response
        create_response(vectorstore, prompt)
        # st.session_state['memory'].chat_memory.add_user_message(prompt)

# create response if prompt_to_start variable exists
if prompt_to_start is not "":
    create_response(vectorstore, prompt_to_start)
    del prompt_to_start

# add a speech to text button
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
    st.rerun()