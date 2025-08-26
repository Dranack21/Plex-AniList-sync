import requests
import json

url =  "https://graphql.anilist.co"

f = open(".env")
f.readline()
ACCESS_TOKEN = f.readline()

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
# query = '''	
# {
# 	Viewer
# 	{
# 		name
# 	}
# }
# '''


mutation SaveMediaListEntry($mediaId: Int, $progress: Int) {
  SaveMediaListEntry(mediaId: $mediaId, progress: $progress) {
    
  }
}

variables ={
	'mediaId': 7791
	'progress': 24
}

response = requests.post(url, json={"mutation": mutation}, headers=headers, 'variables': variables)
print(response)
print(response.json())	