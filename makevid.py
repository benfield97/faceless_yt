import requests
import os
import json
import moviepy.editor as mpy
from dotenv import load_dotenv
from pydub import AudioSegment
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
load_dotenv()
creatomate_api = os.getenv('creatomate_api')
root_dir = 'data/audio'
parent_folder_id = '1ciQRTtmiE4HaG0bJJp2HYuubtAZX1t5i'  # replace with your actual folder ID

def maketitle(username,points, time, duration, body, Mp3Path):
    points = int(points)/1000
    points = round(points, 1)
    options = {
        'template_id': 'ddf8154c-8292-4f3b-b6d1-96fa04583297',
        'modifications': {
            'Body Text': body,
            'username': username,
            'points': f'{points}k',
            'time': time,
            'duration': {duration + 0.8},
            'voiceover': Mp3Path
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

    response_data = response.json()
    print(response_data)
    return response_data

def makevid(username,points, time, duration, body, Mp3Path):
    options = {
        'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96',
        'modifications': {
            'Body Text': body,
            'username': username,
            'points': f'{points} points',
            'time': time,
            'duration': {duration + 0.8},
            'voiceover': Mp3Path
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

    response_data = response.json()
    print(response_data)
    return response_data

with open('data/posts.json', 'r') as f:
    data = json.load(f)

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

    video_files = []

    comments = post['Comments']
    title = post

    #make title vid
    audio_file = drive.CreateFile({'title': os.path.basename(title['Mp3Path']), 'parents': [{'id': parent_folder_id}]})
    audio_file.SetContentFile(title['Mp3Path'])
    audio_file.Upload()

    audio_file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    audio_link = audio_file['alternateLink']

    response = makevid(title['Post Author'], title['Score'], title['Post Date'], 
                        title['Duration'], title['Title'], audio_link)

    video_url = response[0]['url']
    video_filename = f"{root_dir}/{title['Title']}.mp4"
    download_file(video_url, video_filename)
    video_files.append(video_filename)

    for comment in comments:
        audio_file = drive.CreateFile({'title': os.path.basename(comment['Mp3Path']), 'parents': [{'id': parent_folder_id}]})
        audio_file.SetContentFile(comment['Mp3Path'])
        audio_file.Upload()

        audio_file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        audio_link = audio_file['alternateLink']

        response = makevid(comment['Comment Author'], comment['Upvotes'], comment['Comment Posted Time'], 
                           comment['Duration'], comment['Comment'], audio_link)

        video_url = response[0]['url']
        video_filename = f"{root_dir}/{comment['Comment Author']}.mp4"
        download_file(video_url, video_filename)
        video_files.append(video_filename)

    videos = [mpy.VideoFileClip(path) for path in video_files]
    final_video = mpy.concatenate_videoclips(videos)
    final_video.write_videofile(f"vidoutput/{title['Title']}.mp4")

responses = [[{'id': '93d0cf5b-9164-45f2-b2fc-477542950650', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/93d0cf5b-9164-45f2-b2fc-477542950650.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': "It's all I have", 'username': 'NaziGazpacho', 'points': 46491, 'time': '4 years ago', 'duration': 1, 'voiceover': 'https://drive.google.com/file/d/1_ZpCBoiTkCBUqPxTyKfL-iht__BXKsQ1/view?usp=drivesdk'}}],
[{'id': 'c23eb526-b12d-4ee1-9315-46dec5904442', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/c23eb526-b12d-4ee1-9315-46dec5904442.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': '[deleted]', 'username': 'deleted', 'points': 35940, 'time': '4 years ago', 'duration': 1, 'voiceover': 'https://drive.google.com/file/d/1obGLSn3gttV4vr6ZJzYNpkbEhdZdxx1Q/view?usp=drivesdk'}}],
[{'id': '80a6337e-bde6-4c1b-8fac-543ad9cae182', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/80a6337e-bde6-4c1b-8fac-543ad9cae182.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': "Bold of you to assume I'm going to take a shit this year.", 'username': 'abksploder', 'points': 34853, 'time': '4 years ago', 'duration': 2, 'voiceover': 'https://drive.google.com/file/d/1RkcJiERUuFMAepcer9SNjELFaqAzJgh_/view?usp=drivesdk'}}],
[{'id': '1f061b8e-842b-4bc6-8976-db2e4754e8f6', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/1f061b8e-842b-4bc6-8976-db2e4754e8f6.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': '"Fuck you, I won\'t poo when you tell me"', 'username': 'ThreeSheetzToTheWind', 'points': 28367, 'time': '4 years ago', 'duration': 2, 'voiceover': 'https://drive.google.com/file/d/1Aoau_FQYlsF0qnxbSBu7IbJpACa7DYrI/view?usp=drivesdk'}}],
[{'id': 'b70f8058-3589-42cb-8e44-50d397903b93', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/b70f8058-3589-42cb-8e44-50d397903b93.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': 'Everyone now thinking about the last time they pooped. Nicely played. ', 'username': 'Lady_Minuit', 'points': 26830, 'time': '4 years ago', 'duration': 3, 'voiceover': 'https://drive.google.com/file/d/1czkqws9lGQO4ePEMI39zDrOBb3h5f_WG/view?usp=drivesdk'}}],
[{'id': 'e87d37ef-4bf5-44bd-9e64-6fe4db29164f', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/e87d37ef-4bf5-44bd-9e64-6fe4db29164f.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': 'Im letting go right now as I type. ', 'username': 'PrinceofallRabbits', 'points': 26562, 'time': '4 years ago', 'duration': 1, 'voiceover': 'https://drive.google.com/file/d/1rzpOk1Mkc12-HLnszG8bhkPvk9xx590a/view?usp=drivesdk'}}],
[{'id': '4ad619b2-8745-4f0c-9414-ca1ba58560be', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/4ad619b2-8745-4f0c-9414-ca1ba58560be.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': 'Quality shitpost ', 'username': 'groggy05', 'points': 25192, 'time': '4 years ago', 'duration': 1, 'voiceover': 'https://drive.google.com/file/d/1znomweWtM6cWHVCWIR2Hr_2Ek0xoAy5P/view?usp=drivesdk'}}],
[{'id': '118179a2-83f9-4be1-8e65-315f1e175ced', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/118179a2-83f9-4be1-8e65-315f1e175ced.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': 'im constipated   Edit: Free Bobby Shmurda', 'username': 'DadAsFuck', 'points': 20416, 'time': '4 years ago', 'duration': 2, 'voiceover': 'https://drive.google.com/file/d/1JRfGjrQ2iXsRC39i3llHkD27JA0fYHg7/view?usp=drivesdk'}}],
[{'id': '7b3958e3-27f4-4e62-a085-5aad39a195b9', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/7b3958e3-27f4-4e62-a085-5aad39a195b9.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': "We have guests and I literally can't relax.", 'username': 'adsadsadsadsads', 'points': 19267, 'time': '4 years ago', 'duration': 2, 'voiceover': 'https://drive.google.com/file/d/1rOM0BTcx-ESDqOPKptSfHZV_4jaZgrJM/view?usp=drivesdk'}}],
[{'id': '509987e3-c1a1-419b-b5ef-ddfa4c7ce8c5', 'status': 'planned', 'url': 'https://cdn.creatomate.com/renders/509987e3-c1a1-419b-b5ef-ddfa4c7ce8c5.mp4', 'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96', 'template_name': 'Example template for Ben', 'template_tags': [], 'output_format': 'mp4', 'modifications': {'Body Text': 'Lets see who can go the longest in 2019 without taking a shit  Edit: This blew up..', 'username': 'Fushigibama', 'points': 15836, 'time': '4 years ago', 'duration': 4, 'voiceover': 'https://drive.google.com/file/d/1ulEQENtc7-wMzfEiKVNtLtmbJJaJkIMr/view?usp=drivesdk'}}]]
    




# to do 
# have the voice be a little more lively. Experiment with eleven settings
# get the pipeline finished. Have a final video get exported 
# needs to output each final vid into a folder
# add emojis

