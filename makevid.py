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

def makevid(username,points, time, duration, body):

    options = {
    # The ID of the template that you created in the template editor
    'template_id': '823ad2be-9b2e-46af-bdf5-f39abf90ed96',
    

    # Modifications that you want to apply to the template
    'modifications': {
        'Body Text': "Hi! 👋 Thanks for trying out Creatomate!",
        'username': "✨🦖",
        'points': '👍 100',
        'time': '4 years ago',
        'duration': '20 s'
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

for dir_name, _, file_list in os.walk(root_dir):
    print(dir_name)
    for file_name in file_list:
        if 'comment' in file_name:
            full_path = os.path.join(dir_name, file_name)
            duration = get_duration(full_path)
            print(f'Duration of {file_name}: {duration} seconds')
            # Perform further processing here