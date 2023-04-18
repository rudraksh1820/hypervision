import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# Set up the YouTube API connection
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(request())
    else:
        flow = google.auth.default(scopes=SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

youtube = build('youtube', 'v3', credentials=creds)

# Set up the video metadata
body = {
    'snippet': {
        'title': 'My video title',
        'description': 'My video description',
        'tags': ['tag1', 'tag2', 'tag3'],  # add tags as needed
        'categoryId': '22',  # set the category ID for the video
        'defaultLanguage': 'en-US',  # set the default language for the video
        'defaultAudioLanguage': 'en-US',  # set the default audio language for the video
    },
    'status': {
        'privacyStatus': 'unlisted'  # set the privacy status of the video
    }
}

# Set up the video file path
video_path = '"C:\Users\ARYAN\Music\WhatsApp Video 2023-04-18 at 9.27.43 AM.mp4"'

# Upload the video to YouTube
try:
    insert_request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=video_path
    )
    
    response = insert_request.execute()
    print('Video uploaded successfully! Video ID:', response['id'])
    
except HttpError as error:
    print(f'An HTTP error {error.resp.status} occurred: {error.content}')
