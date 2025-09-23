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
query MediaList($mediaId: Int, $userId: Int) {
  MediaList(mediaId: $mediaId, userId: $userId) {
    repeat
    status
    progress
    media {
      episodes
    }
    userId
  }
}'''

mutation ='''
mutation Mutation($mediaId: Int, $repeat: Int, $status: MediaListStatus) {
  SaveMediaListEntry(mediaId: $mediaId, repeat: $repeat, status: $status) {
    progress
  }
}
'''

# This function looks if an anime that appeared in the watch history is COMPLETED or REPEATING and updates to the other one if needed
# Args: Two ints anime_id which is the id for ani list to recognize the anime and progress the number of episodes watched
# Notes: One piece kai is not present on my AniList so it's hard coded since it made things I didnt watch set as watched
# Return: Nothing

def	check_for_status(anime_id, progress):
  print(anime_id, progress)
  variables = {
    "mediaId": anime_id,
    "userId": "7021144"
  }
  response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
  json_dico = response.json()
  print(json_dico)
  media_list = json_dico["data"]["MediaList"]
  if media_list is None:
    return
  if (json_dico["data"]["MediaList"]["status"] == "COMPLETED"):
    variables = {
      "mediaId": anime_id,
      "repeat": json_dico["data"]["MediaList"]["repeat"] + 1,
      "status": "REPEATING"
      }
    response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
    return (0);
  elif (json_dico["data"]["MediaList"]["status"] == "REPEATING"):
    if (json_dico["data"]["MediaList"]["progress"] == json_dico["data"]["MediaList"]["media"]["episodes"]):
      variables = {
        "mediaId": anime_id,
        "status": "COMPLETED"
        }
      response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
  return(0)

