import requests

source = {
 'output_format': 'mp4',
 'width': 1920,
 'height': 1080,
 'elements': [
  {
   'type': 'video',
   'track': 1,
   'source': 'https://cdn.creatomate.com/demo/drone.mp4'
  },
  {
   'type': 'video',
   'track': 1,
   'source': 'https://cdn.creatomate.com/demo/river.mp4',
   'animations': [
    {
     'time': 'start',
     'duration': 1,
     'transition': True,
     'type': 'fade'
    }
   ]
  }
 ]
}

response = requests.post(
 'https://api.creatomate.com/v1/renders',
 headers={
  # Find your API key under 'Project Settings' in your account:
  # https://creatomate.com/docs/api/rest-api/authentication
  'Authorization': 'Bearer Your-API-Key',
  'Content-Type': 'application/json',
 },
 json={'source': source}
)

print(response.json())