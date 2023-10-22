import streamlit as st
from pathlib import Path
from password import check_password
import json

st.header("Topics Setup")
st.markdown("This page allows you to set up the topics for the cards and the side-bar.")

if not check_password():
    st.stop()

# load the topics from the json file
with open(Path("topics.json"), "r") as f:
    topics = json.load(f)

# prompt the user to enter the topics for the cards
st.markdown("Enter the topics for the cards below")
card_topic_1 = st.text_input("Topic 1", value = topics["card_topic_1"])
card_topic_2 = st.text_input("Topic 2", value = topics["card_topic_2"])
card_topic_3 = st.text_input("Topic 3", value = topics["card_topic_3"])
card_topic_4 = st.text_input("Topic 4", value = topics["card_topic_4"])
card_topic_5 = st.text_input("Topic 5", value = topics["card_topic_5"])
card_topic_6 = st.text_input("Topic 6", value = topics["card_topic_6"])

# prompt the user to enter the questions for the side-bar
st.markdown("Enter the topics for the side-bar below")
sidebar_topic_1 = st.text_input("Sidebar Topic 1", value = topics["sidebar_topic_1"])
sidebar_topic_2 = st.text_input("Sidebar Topic 2", value = topics["sidebar_topic_2"])
sidebar_topic_3 = st.text_input("Sidebar Topic 3", value = topics["sidebar_topic_3"])
sidebar_topic_4 = st.text_input("Sidebar Topic 4", value = topics["sidebar_topic_4"])
sidebar_topic_5 = st.text_input("Sidebar Topic 5", value = topics["sidebar_topic_5"])
sidebar_topic_6 = st.text_input("Sidebar Topic 6", value = topics["sidebar_topic_6"])


# put everything into a dictionary
topics = {
    "card_topic_1": card_topic_1,
    "card_topic_2": card_topic_2,
    "card_topic_3": card_topic_3,
    "card_topic_4": card_topic_4,
    "card_topic_5": card_topic_5,
    "card_topic_6": card_topic_6,
    "sidebar_topic_1": sidebar_topic_1,
    "sidebar_topic_2": sidebar_topic_2,
    "sidebar_topic_3": sidebar_topic_3,
    "sidebar_topic_4": sidebar_topic_4,
    "sidebar_topic_5": sidebar_topic_5,
    "sidebar_topic_6": sidebar_topic_6,
}

# dump it to a local json file, when user clicks button
if st.button("Save"):
    with open(Path("topics.json"), "w") as f:
        json.dump(topics, f)
    st.success("Topics saved successfully")