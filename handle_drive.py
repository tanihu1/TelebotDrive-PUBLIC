from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
import pandas as pd
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDS = service_account.Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES)  # Credentials of the drive api service account
API_NAME = 'drive'
API_VERSION = 'v3'
try:
    service = build('drive', 'v3', credentials=CREDS)  # Create a drive service
    # This will print in server logs
    print("Drive service created successfully!")
except Exception as error:
    print("Unable to connect to the drive API:")
    print(error)


def get_main_ids():  # This function returns a dataframe of the main folders in the set drive
    try:
        main_folder = '1Aho4k9ubHkwv8WPM-x1r3FjspzaCscke'  # Folder ID of the main folder
        # Query to get the folders inside the main folder
        query = f"parents in '{main_folder}' and trashed=false"
        response = service.files().list(
            q=query,
            includeItemsFromAllDrives=True,
            supportsAllDrives=True
        ).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')
        while nextPageToken:  # Incase theres alot of files
            response = service.files().list(
                q=query,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=nextPageToken
            ).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        df = pd.DataFrame(files)
        return (df)  # Return the dataframe of the main folders
    except HttpError as error:
        error_details = error.content.decode("utf-8")
        error_status_code = error.resp.status
        error_reason = error._get_reason()

        print("An error occurred:")
        print(f"HTTP Status Code: {error_status_code}")
        print(f"Error Reason: {error_reason}")
        print(f"Error Details: {error_details}")


# This function returns a dataframe of the sub folders inside the user's selection
def get_sub_list(folder_id: str):
    try:
        sub_folder = folder_id
        query = f"parents in '{sub_folder}' and trashed=false"
        response = service.files().list(
            q=query,
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        ).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')
        while nextPageToken:
            response = service.files().list(
                q=query,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=nextPageToken,
            ).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        df = pd.DataFrame(files)
        return (df)
    except HttpError as error:
        error_details = error.content.decode("utf-8")
        error_status_code = error.resp.status
        error_reason = error._get_reason()

        print("An error occurred:")
        print(f"HTTP Status Code: {error_status_code}")
        print(f"Error Reason: {error_reason}")
        print(f"Error Details: {error_details}")


def get_file(file_id):  # This function returns the selected file and the file name
    try:
        request = service.files().get_media(fileId=file_id)
        file_name = service.files().get(fileId=file_id, fields='name').execute()
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"download progress {status.progress()*100}")
        fh.seek(0)
        return (fh, file_name)
    except HttpError as error:
        error_details = error.content.decode("utf-8")
        error_status_code = error.resp.status
        error_reason = error._get_reason()

        print("An error occurred:")
        print(f"HTTP Status Code: {error_status_code}")
        print(f"Error Reason: {error_reason}")
        print(f"Error Details: {error_details}")


if __name__ == "__main__":
    print(get_main_ids())
