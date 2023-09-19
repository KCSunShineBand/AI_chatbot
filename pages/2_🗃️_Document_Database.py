import os
import io
import streamlit as st
import re
from math import floor
from pathlib import Path
import pandas as pd
from password import check_password
from streamlit_oauth import OAuth2Component
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from googleapiclient.http import MediaIoBaseDownload

#load env variables
from dotenv import load_dotenv
load_dotenv()

st.header("Document Database")
st.markdown("This is the current document database. You can upload new documents here for use in the vector store.")

if not check_password():
    st.stop()
    pass

# display the current document database


tab_local, tab_drive, tab_youtube = st.tabs(["File Upload", "Google Drive", "Youtube"])

with tab_local:
    with st.form("upload-form", clear_on_submit=True):
            uploaded_files = st.file_uploader("Choose Documents", accept_multiple_files=True, type=["json", "pdf", "csv", "xls", "xlsx", "txt"])
            submitted = st.form_submit_button("Upload")
            if submitted:
                for uploaded_file in uploaded_files:
                    st.write("Uploading " + uploaded_file.name + " ...")
                    # save to local file
                    bytes_data = uploaded_file.read()

                    #save to documents folder
                    localPath = str(Path.cwd()) + "/documents/"
                    with open(localPath + uploaded_file.name, "wb") as f:
                        f.write(bytes_data)

                    st.write("Upload Complete. Document added to database.")
   

with tab_drive:
    st.header("Google Drive")

    # Create the oauth2 component
    AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"
    CLIENT_ID = os.getenv("GOOGLE_DRIVE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("OAUTH2_REDIRECT_URI")
    SCOPE = "https://www.googleapis.com/auth/drive.readonly"
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    # Check if dropbox token exists in session state
    if 'google_token' not in st.session_state:
        # If not, show authorize button
        result = oauth2.authorize_button("Login to Drive", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            # If authorization successful, save token in session state
            st.session_state["google_token"] = result.get('token')
            st.experimental_rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state['google_token']
        # st.json(token)
        if st.button("Logout Drive"):
            # If refresh token button is clicked, refresh the token
            # token = oauth2.revoke_token(token) - this doesn't work (yet)
            del st.session_state['google_token']
            st.experimental_rerun()


    ## the page below, should only run when the user is logged in
    if 'google_token' not in st.session_state:
        st.warning("Not logged in to Google Drive yet. Please log in to Google Drive first.")
    else:
        # instantiate the google drive service
        gCreds = GoogleCredentials( 
                st.session_state["google_token"]["access_token"], 
                CLIENT_ID,
                CLIENT_SECRET, 
                refresh_token=None, 
                token_expiry=None,
                token_uri=TOKEN_URL, 
                user_agent='Python client library',
                revoke_uri=None)
        drive_service = build('drive', 'v3', credentials=gCreds)

        # get all the files in the google drive
        results = drive_service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size)").execute()
        files = results.get('files', [])
        # st.json(files)

        # create a dataframe with the files and folders
        df = pd.DataFrame()
        for entry in files:
            if entry.get("mimeType") == "application/vnd.google-apps.document": # only doduments, nothing else
                # set size to 0 if the size key doesn't exist
                if "size" not in entry:
                    entry["size"] = 0
                df = pd.concat( [df, pd.DataFrame({ "File name": [entry['name']], "Size": [entry['size']], "id": [entry['id']], "mime": [entry['mimeType']] })], ignore_index=True )


        def dataframe_with_selections(df):
            df_with_selections = df.copy()
            df_with_selections.insert(0, "Select", False)
            edited_df = st.data_editor(
                df_with_selections,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                disabled=df.columns,
                width=750,
            )

            # get the selected file names, only if checkbox is checked
            selected_file_ids = edited_df[(edited_df["Select"] == True)]["id"].tolist()
            selected_file_names = edited_df[(edited_df["Select"] == True)]["File name"].tolist()
            selected_file_mimes = edited_df[(edited_df["Select"] == True)]["mime"].tolist()

            # return a dict with the above lists
            return {"selected_file_ids": selected_file_ids, "selected_file_names": selected_file_names, "selected_file_mimeTypes": selected_file_mimes}

        selections = dataframe_with_selections(df)

    if st.button("Download selected files"):
        # download the selected files
        for fileId, fileName, mimeType in zip(selections["selected_file_ids"], selections["selected_file_names"], selections["selected_file_mimeTypes"]):
            st.write("Downloading file: " + fileName)
            st.write("File ID: " + fileId)
            st.write("Mime type: " + mimeType)
            request = drive_service.files().export_media(fileId=fileId, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document') # saves as docx
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                st.write("Download %d%%." % int(status.progress() * 100))
            st.write("Download complete.")
            
            # get the current working dir and save the file in the documents folder
            cwd = Path.cwd()
            documents_folder = cwd / "documents"
            documents_folder.mkdir(exist_ok=True)
            file_path = documents_folder / fileName
            # add docx extension if it doesn't exist, change the suffix if we want to save as a different file type
            file_path = file_path.with_suffix(".docx")
            with open(file_path, "wb") as f:
                f.write(fh.getvalue())
            st.write("File saved to: " + str(file_path))

with tab_youtube:
    from langchain.document_loaders import YoutubeLoader

    with st.form("form-youtube", clear_on_submit=False):
        text_input_url = st.text_input("Youtube URL:")
        button_submit = st.form_submit_button("Submit")
        st.warning('Not all videos have transcripts. If the video does not have a transcript, this may not work.')

        if button_submit:
            video_loader = YoutubeLoader.from_youtube_url(text_input_url, add_video_info=True)
            text_input_url = ''
            docs = video_loader.load()

            # it loads everything in a single doc so we can select the first one
            transcript = docs[0].page_content
            transcript_metadata = docs[0].metadata

            st.session_state.extracted_metadata = transcript_metadata
            st.session_state.extracted_text = transcript

    extracted_text = st.text_area("Extracted Text", 'Please enter a Youtube URL and click Submit!', disabled=True, height=200, key='extracted_text')
    
    if 'extracted_metadata' not in st.session_state:
        pass
    else:
        st.write("Video Title: " + st.session_state.extracted_metadata['title'])
        if st.button('Save into database'):
            #save to local file
            localPath = str(Path.cwd()) + "/documents/"
            filename = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", st.session_state.extracted_metadata['title'])
            with open(localPath + filename + '.txt', "w") as f:
                f.write(extracted_text)
            st.success('Document added to database as:\n "' + filename + '.txt"')        

# get all the files in the document directory and their size
files = os.listdir("documents")
files = [file for file in files]
files = [{"name": file, "size": os.path.getsize("documents/" + file)} for file in files]

# Show the document table 
colms = st.columns((.5, 2, 1, 1))
fields = ['Index', 'Document Name', 'Size', 'Delete']
for col, field_name in zip(colms, fields):
    col.write(field_name)

# iterate over files, get index, name, size, and summarize button
selected_files = []
for i, file in enumerate(files):
    col1, col2, col3, col4 = st.columns((.5, 2, 1, 1))
    col1.write(i)  # index
    col2.write(file['name'])  # name
    col3.write(str(floor(file['size'] * 0.001)) + " KB")  # email
    button_summarize = col4.empty()  # create a placeholder
    click_delete = button_summarize.button(label='Delete', key='delete_' + file['name'])
    if click_delete:
        clicked_file = file['name']
        os.remove("documents/" + clicked_file)
        st.experimental_rerun()
