import requests
import os
import glob
import json
import moviepy.editor as mpy
from dotenv import load_dotenv
from pydub import AudioSegment
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
load_dotenv()
creatomate_api = os.getenv('creatomate_api')
root_dir = 'data/audio'


def makevid(username,points, time, duration, body, voiceover):

    options = {
    # The ID of the template that you created in the template editor
    'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96',
    

    # Modifications that you want to apply to the template
    'modifications': {
        'Body Text': "Hi! 👋 Thanks for trying out Creatomate!",
        'username': "✨🦖",
        'points': '👍 100',
        'time': '4 years ago',
        'duration': duration,
        'voiceover': voiceover
    },
    }


    response = requests.post(
    'https://api.creatomate.com/v1/renders',
            headers={
                'Authorization': f'Bearer {creatomate_api}',
                'Content-Type': 'application/json',
            },
            json=options
            )

    print(response.content)


# Load your JSON data
with open('data/posts.json', 'r') as f:
    data = json.load(f)

# List to store paths of generated video files
video_files = []

# GoogleDrive login
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def download_file(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: 
                    f.write(chunk)

for post in data:
    comments = post['Comments']
    for comment in comments:
        # Upload the audio file to Google Drive
        audio_file = drive.CreateFile({'title': os.path.basename(comment['Mp3Path'])})
        audio_file.SetContentFile(comment['Mp3Path'])
        audio_file.Upload()

        # Get the shareable link
        audio_file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        audio_link = audio_file['alternateLink']

        response = makevid(comment['Comment Author'], comment['Upvotes'], comment['Comment Posted Time'], 
                           comment['Duration'], comment['Comment'], audio_link)

        # Assume the response is a list of dictionaries
        video_url = response[0]['url']
        video_filename = f"{root_dir}/{comment['Comment Author']}.mp4"
        download_file(video_url, video_filename)
        video_files.append(video_filename)

# Concatenate all the videos
videos = [mpy.VideoFileClip(path) for path in video_files]
final_video = mpy.concatenate_videoclips(videos)
final_video.write_videofile("final_output.mp4")



# to do 
# make title template page
# have makevid for title
# clean post texts to any edited or deleted
# filter for comment length as well
# in the scrape part, might want to be able to select which posts and comments to accept
# have the voice be a little more lively. Experiment with eleven settings
# get the pipeline finished. Have a final video get exported 