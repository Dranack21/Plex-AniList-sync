import requests
import os
import json
import sys
from dotenv import load_dotenv
from Get_watch_history  import  Get_key_and_user_history
from Get_watch_history  import  Search_for_title
from one_piece_kai      import  kai_to_anime
from helpers            import  check_for_status

###env handling using load_dotenv from uv
load_dotenv()
ACCESS_TOKEN = os.getenv('ANI_TOKEN')
url =  "https://graphql.anilist.co"

###headers needed by graphQL to work
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
#query for graphQL that will give us the anime by id by giving its title
query = '''
query Media($search: String, $type: MediaType)
{
  Media(search: $search, type: $type)
  {
    id
  }
}
'''
mutation = '''
mutation SaveMediaListEntry($mediaId: Int, $progress: Int)
{
  SaveMediaListEntry(mediaId: $mediaId, progress: $progress)
  {
    progress
    mediaId
  }
}
'''

# Fetches Anilist_id using a list of anime_titles and pairs them with their watched progress inside a list of list.
# Args: A list of list that contains an anime name + an anime episode watched ([One piece, 45],[K on, 17])
# Notes: Uses GraphQL to make HTTP request to ani list API
# Return: The list of list containing pairs of anime_id + progress  

def Request_id(name_progress_dict):
  progress_id = []
  allkeys = list(name_progress_dict.keys())
  for i in range(len(allkeys)):
    variables = {
        "search": allkeys[i], ##anime name
        "type": "ANIME"
    }
    response = requests.post(url, json={"query":query, "variables": variables}, headers= headers)
    if (response.status_code == 200):
      dico = response.json()
      anime_id = dico["data"]["Media"]["id"] ##we only requested anime id graphql
      progress_id.append([anime_id, name_progress_dict[allkeys[i]]]) #list of anime id + episode watched
      print(response.json())
  return (progress_id)



# Parses a list of list that contains pairs of anime_id + progress and makes a dictionnary with the highest episode watched of each anime_id 
# Args: A list of list that contains an anime_id + an anime episode watched ([4501, 45],[1701, 17], [4501, 46])
# Notes: When accessing a dictionnary key that doesnt exist python throws an KeyError exepction
# Return: A dictionnary with key being an anime id and value highest episode watched [1701, 17], [4501, 46]

def get_highest_progress(progress_id):

  id_dictionnary = {};  
  for i in range(len(progress_id)):
    try:
      if (id_dictionnary[progress_id[i][0]] and progress_id[i][1] > id_dictionnary[progress_id[i][0]]):
        id_dictionnary[progress_id[i][0]] = progress_id[i][1]
    except KeyError:
      id_dictionnary[progress_id[i][0]] = progress_id[i][1]
  return(id_dictionnary)


# This function is called in a for loop each time with an anime_id and a progress it will make an HTTP request to ANILIST to update progress
# Args: Two ints anime_id which is the id for ani list to recognize the anime and progress the number of episodes watched
# Notes: One piece kai is not present on my AniList so it's hard coded since it made things I didnt watch set as watched
# Return: Nothing

def update_anime_progress(anime_id, progress):
  ###Handle one piece kai case
  if (anime_id == 465):
    anime_id = 21
    progress = kai_to_anime(progress)
  variables = {
    "mediaId": anime_id,
    "progress": progress
  }
  check_for_status(anime_id, progress)
  response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
  if (response.status_code == 200):
    print("\033[92mAnime with ID", anime_id, "progress updated to", progress, "\033[0m")
  else:
    print("\033[91mError updating anime", anime_id, "\033[0m")


  
def main():
  print("\033[94mGetting user History using Rest and Tautulli API\033[0m")  # Blue
  try:
    dico = Get_key_and_user_history()
  except requests.exceptions.RequestException as e:
    print(f"Encountered an error when trying to access User Plex watch history: {e}")
    sys.exit(1)
  print("\033[92mFetching anime name + progress watched from precedent tautulli api request\033[0m")  # Green
  try:
    Title_list = Search_for_title(dico)
  except requests.exceptions.RequestException as e:
    print(f"Encoutered error: {e}")
    return (1) 
  Highest_progress_dic = get_highest_progress(Title_list);
  print(id)
  print("\033[93mGetting anime_id using graphQL query request on anilist api\033[0m")  # Orange/Yellow
  try:
    progress_and_id = Request_id(Highest_progress_dic)
  except requests.exceptions.RequestException as e:
      print(f"Request failed: {e}")
      return (1)
  for i in range(len(progress_and_id)):
    update_anime_progress(progress_and_id[i][0], progress_and_id[i][1])

if __name__ == "__main__":
    main()