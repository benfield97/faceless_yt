import requests
from dotenv import load_dotenv
import os
import glob
from pydub import AudioSegment
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




# to do 
# clean post texts to any edited or deleted
# filter for comment length as well
# in the scrape part, might want to be able to select which posts and comments to accept
# have the voice be a little more lively. Experiment with eleven settings
# get the pipeline finished. Have a final video get exported 