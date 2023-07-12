import os
import json
from elevenlabs import voices, generate
import wave
import re
from pydub import AudioSegment
from mutagen.mp3 import MP3

# Get the Eleven Labs API key
eleven_api = os.getenv('ELEVEN_API_KEY')

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

def convert_wav_to_mp3(wav_file, mp3_file):
    # Check if the output file already exists
    if not os.path.isfile(mp3_file):
        audio = AudioSegment.from_wav(wav_file)
        audio.export(mp3_file, format="mp3")
        os.remove(wav_file)  # This line deletes the original WAV file
    # Calculate the duration of the mp3 file
    mp3_audio = MP3(mp3_file)
    duration = int(mp3_audio.info.length)
    return duration

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
    mp3_duration = convert_wav_to_mp3(audio_file_path, audio_file_path.replace('.wav', '.mp3'))
    
    # Store the path and duration of the mp3 file
    post['TitleMp3Path'] = audio_file_path.replace('.wav', '.mp3')
    post['TitleDuration'] = mp3_duration

    # Generate and write audio for each comment
    for i, comment in enumerate(post['Comments']):
        audio = generate(text=comment['Comment'], voice=voices[0])
        audio_file_path = os.path.join(post_folder_path, f"comment_{i+1}.wav")
        write_audio_file(audio_file_path, audio)
        mp3_duration = convert_wav_to_mp3(audio_file_path, audio_file_path.replace('.wav', '.mp3'))

        # Store the path and duration of the mp3 file
        comment['Mp3Path'] = audio_file_path.replace('.wav', '.mp3')
        comment['Duration'] = mp3_duration

# Save the updated posts back to the JSON file
with open('data/posts.json', 'w') as f:
    json.dump(posts, f, indent=4)
