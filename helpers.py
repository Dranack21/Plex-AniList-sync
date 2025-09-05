import requests
import os
import json
from dotenv import  load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('ANI_TOKEN')

url =  "https://graphql.anilist.co"

###headers needed by graphQL to work
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
query = '''
query MediaList($mediaId: Int) {
  MediaList(mediaId: $mediaId) {
    progress
    repeat
    status
    media {
      episodes
    }
  }
}'''

mutation ='''
mutation Mutation($mediaId: Int, $repeat: Int, $status: MediaListStatus) {
  SaveMediaListEntry(mediaId: $mediaId, repeat: $repeat, status: $status) {
    progress
  }
}
'''

def	check_for_status(anime_id, progress):
  print(anime_id, progress)
  variables = {
  "mediaId": anime_id
  }
  response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
  json_dico = response.json()
  print(json_dico)
  if (json_dico["data"]["MediaList"]["status"] == "COMPLETED" or json_dico["data"]["MediaList"]["status"] == "REPEATING"):
    if (json_dico["data"]["MediaList"]["progress"] == json_dico["data"]["MediaList"]["media"]["episodes"]):
      variables = {
        "mediaId": anime_id,
        "repeat": json_dico["data"]["MediaList"]["repeat"] + 1,
        "status": "REPEATING"
      }
      response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
    return(1);
  return(0);

