import os
import json
from elevenlabs import voices, generate
import wave
import re


# this works! need a better selection method for the content though
os.environ['ELEVEN_API_KEY'] = 'ab6f1c5edd135c28345d10c208e1b5d5'

# Constants
AUDIO_FORMAT = "audio/wav"
BASE_FOLDER_PATH = "data/audio"
SAMPLE_RATE = 44100
NUM_CHANNELS = 2
SAMPLE_WIDTH = 2

# Ensure base folder exists
os.makedirs(BASE_FOLDER_PATH, exist_ok=True)

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]', '', filename)

def write_audio_file(file_path, audio_data):
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(NUM_CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)

# Load posts
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

# Fetch available voices
voices = voices()

# Iterate over posts
for post in posts[:1]:
    # Create a folder for the post
    post_folder_path = os.path.join(BASE_FOLDER_PATH, sanitize_filename(post['Title']))
    os.makedirs(post_folder_path, exist_ok=True)
    
    # Generate and write audio for the post title
    audio = generate(text=post['Title'], voice=voices[0])
    audio_file_path = os.path.join(post_folder_path, "title.wav")
    write_audio_file(audio_file_path, audio)

    # Generate and write audio for each comment
    for i, comment in enumerate(post['Comments']):
        audio = generate(text=comment['Comment'], voice=voices[0])
        audio_file_path = os.path.join(post_folder_path, f"comment_{i+1}.wav")
        write_audio_file(audio_file_path, audio)