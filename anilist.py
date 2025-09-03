# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    anilist.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: habouda <habouda@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/08/31 15:33:51 by habouda           #+#    #+#              #
#    Updated: 2025/09/03 18:05:47 by habouda          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
import os
import json
from dotenv import load_dotenv
from Get_watch_history import Get_key_and_user_history
from Get_watch_history import Search_for_title

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

def Request_id_and_progress(Title_list):
  progress_id = []
  for i in range(len(Title_list)):
    variables = {
        "search": Title_list[i][0], ##anime name
        "type": "ANIME"
    }
    response = requests.post(url, json={"query":query, "variables": variables}, headers= headers)
    if (response.status_code == 200):
      dico = response.json()
      anime_id = dico["data"]["Media"]["id"] ##we only requested anime id graphql
      progress_id.append([anime_id, Title_list[i][1]]) #list of anime id + episode watched
      print(response.json())
  return (progress_id)



# Parses a list of list that contains pairs of anime_id + progress and makes a dictionnary with the highest episode watched of each anime_id 
# Args: A list of list that contains an anime_id + an anime episode watched ([4501, 45],[1701, 17])
# Notes: When accessing a dictionnary key that doesnt exist python throws an KeyError exepction
# Return: A dictionnary with key being an anime id and value highest episode watched

def get_highest_progress(progress_id):

  id_dictionnary = {};  
  for i in range(len(progress_id)):
    try:
      if (id_dictionnary[progress_id[i][0]] and progress_id[i][1] > id_dictionnary[progress_id[i][0]]):
        id_dictionnary[progress_id[i][0]] = progress_id[i][1]
    except KeyError:
      id_dictionnary[progress_id[i][0]] = progress_id[i][1]
  return(id_dictionnary)

def update_anime_progress(anime_id, progress):
  variables = {
    "mediaId": anime_id,
    "progress": progress
  }
  response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
  print(anime_id, response.status_code)

def main():
  print("\033[94mGetting user History using Rest and Tautulli API\033[0m")  # Blue
  dico = Get_key_and_user_history()
  print("\033[92mFetching anime name + progress watched from precedent tautulli api request\033[0m")  # Green
  Title_list = Search_for_title(dico)
  print("\033[93mGetting anime_id using graphQL query request on anilist api\033[0m")  # Orange/Yellow
  progress_id = Request_id_and_progress(Title_list)
  print("\033[91mMaking a dictionnary with only the highest episode watched\033[0m")  # Red
  id = get_highest_progress(progress_id);
  print(id);
  for anime_id, progress, in id.items():
    update_anime_progress(anime_id, progress)
if __name__ == "__main__":
    main()