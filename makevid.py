import requests
from dotenv import load_dotenv
import os
import glob
from pydub import AudioSegment
load_dotenv()
creatomate_api = os.getenv('creatomate_api')
root_dir = 'data/audio'

def get_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0  # pydub returns length in milliseconds

def convert_wav_to_mp3(wav_file, mp3_file):
    # Check if the output file already exists
    if not os.path.isfile(mp3_file):
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")
    return mp3_file


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


def process_files(root_dir):
    result_dict = {}
    for dir_name, _, file_list in os.walk(root_dir):
        for file_name in file_list:
            if 'comment' in file_name:
                full_path = os.path.join(dir_name, file_name)
                audio = convert_wav_to_mp3(full_path, full_path.replace('.wav', '.mp3'))
                duration = get_duration(full_path)
                print(f'Duration of {file_name}: {duration} seconds')
                
                # Create a dictionary for this directory if it doesn't exist
                if dir_name not in result_dict:
                    result_dict[dir_name] = {}

                # Save the audio and duration for this file
                result_dict[dir_name][file_name] = [audio, duration]

    return result_dict


print(process_files(root_dir))

#makevid('username', 'points', 'time', duration, 'body', audio)