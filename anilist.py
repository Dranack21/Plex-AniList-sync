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
query Media($type: MediaType, $startDate: FuzzyDateInt, $episodes: Int) {
  Media(type: $type, startDate: $startDate, episodes: $episodes) {
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
            "type": "ANIME",       # type of media
            "startDate": name_progress_dict[allkeys[i]]['air_date'],
            "episodes": name_progress_dict[allkeys[i]]['episode_count']
        }
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        if response.status_code == 200:
            dico = response.json()
            anime_id = dico["data"]["Media"]["id"]  # requested anime id via GraphQL
            progress_id.append([anime_id, name_progress_dict[allkeys[i]]])  # list of anime id + progress dict
            print(response.json())
        else:
           print(response);
           print(name_progress_dict[allkeys[i]]['air_date'])

    return (progress_id)



# Parses a list of list that contains pairs of anime_name + progress and makes a dictionnary with the highest episode watched of each anime_name 
# Args: A list of list that contains an anime_name + an anime episode watched ([one piece, 45],[K ON, 17], [one piece, 46])
# Notes: When accessing a dictionnary key that doesnt exist python throws an KeyError exepction
# Return: A dictionnary with key being an anime id and value highest episode watched [K ON, 17], [one piece, 46]
def get_highest_progress(progress_list):
    anime_dict = {}
    for anime_name, episode, _, air_date , episode_count in progress_list:
        if anime_name in anime_dict:
            anime_dict[anime_name]['max'] = max(anime_dict[anime_name]['max'], episode)
            anime_dict[anime_name]['min'] = min(anime_dict[anime_name]['min'], episode)
            anime_dict[anime_name]['air_date'] = air_date
            anime_dict[anime_name]['episode_count'] = episode_count
        else:
            anime_dict[anime_name] = {
                'max': episode,
                'min': episode,
                'air_date': air_date,
                'episode_count': episode_count
            }
    return (anime_dict);


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
  Dic_max_min_airdate = get_highest_progress(Title_list);
  print(id)
  print("\033[93mGetting anime_id using graphQL query request on anilist api\033[0m")  # Orange/Yellow
  try:
    progress_and_id = Request_id(Dic_max_min_airdate)
  except requests.exceptions.RequestException as e:
      print(f"Request failed: {e}")
      return (1)
  for i in range(len(progress_and_id)):
    update_anime_progress(progress_and_id[i][0], progress_and_id[i][1]["min"])
    if (progress_and_id[i][1]["max"] != progress_and_id[i][1]["min"]):
        update_anime_progress(progress_and_id[i][0], progress_and_id[i][1]["max"])

if __name__ == "__main__":
    main()