import os
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

from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

#load environment variables
from dotenv import load_dotenv
load_dotenv()

#define llm to use
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
system_prompt = "Hi, I'm a mental health assistant. I can help you with any mental health issues you may have. What would you like to talk about?"


# function that creates the vector store
# creates a vectorstore from the selected files by loading them and splitting them into chunks
def create_vectorstore():
    # create chroma vectorstore without any documents
    vectorstore = Chroma()
    vectorstore._embedding_function = OpenAIEmbeddings()
    vectorstore._persist_directory = "db_document_embeddings"

    # text splitter
    text_splitter = CharacterTextSplitter(        
        separator = "\n\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
        is_separator_regex = False,
    )

    dir_loader_pdf = DirectoryLoader('./documents', glob="**/*.pdf").load()
    dir_loader_txt = DirectoryLoader('./documents', glob="**/*.txt").load()
    dir_loader_csv = DirectoryLoader('./documents', glob="**/*.csv").load()
    dir_loader_json = DirectoryLoader('./documents', glob="**/*.json").load()
    dir_loaer_doc = DirectoryLoader('./documents', glob="**/*.doc*").load()
    dir_loaer_xlsx = DirectoryLoader('./documents', glob="**/*.xlsx").load()

    # split the documents into chunks
    # only split if there is 1 or more documents
    if len(dir_loader_pdf) > 0: loaded_pdf = text_splitter.split_documents(dir_loader_pdf); vectorstore.add_documents(loaded_pdf)
    if len(dir_loader_txt) > 0: loaded_txt = text_splitter.split_documents(dir_loader_txt); vectorstore.add_documents(loaded_txt)
    if len(dir_loader_csv) > 0: loaded_csv = text_splitter.split_documents(dir_loader_csv); vectorstore.add_documents(loaded_csv)
    if len(dir_loader_json) > 0: loaded_json = text_splitter.split_documents(dir_loader_json); vectorstore.add_documents(loaded_json)
    if len(dir_loaer_doc) > 0: loaded_doc = text_splitter.split_documents(dir_loaer_doc); vectorstore.add_documents(loaded_doc)
    if len(dir_loaer_xlsx) > 0: loaded_xlsx = text_splitter.split_documents(dir_loaer_xlsx); vectorstore.add_documents(loaded_xlsx)

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
    vectorstore = create_vectorstore()

# button to clear vectorstore
# if st.button('Rebuild Vectorstore'):
#     st.session_state.pop('vectorstore')
#     st.experimental_rerun()

# warning to tell user to clear vector store if new documents were added
# st.warning('If you have added new documents, please rebuild the vectorstore by clicking the button above.')

#display the chat input
prompt = st.chat_input("Say something")
if prompt:
    # create the response
    create_response(vectorstore, prompt)
    # st.session_state['memory'].chat_memory.add_user_message(prompt)

for index, message in enumerate(st.session_state['memory'].load_memory_variables({})['chat_history']):
    if isinstance(message, HumanMessage):      
        # with ph:             
            bot_msg = st.chat_message("assistant")
            bot_msg.write(message.content)
    elif isinstance(message, AIMessage):
        # with ph: 
            human_msg = st.chat_message("user")
            human_msg.write(message.content)

# add a button to clear the memory
if st.button('Clear Chat'):
    st.session_state['memory'].clear()
    st.session_state['memory'].chat_memory.add_ai_message(system_prompt)
    st.experimental_rerun()