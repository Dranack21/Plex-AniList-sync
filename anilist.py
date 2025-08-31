# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    anilist.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: habouda <habouda@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/08/31 15:33:51 by habouda           #+#    #+#              #
#    Updated: 2025/08/31 20:09:44 by habouda          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
import os
import json
from dotenv import load_dotenv
from Get_watch_history import Get_key
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

dico = Get_key()
Title_list = Search_for_title(dico)
progress_id = []


print("\033[92m   PRITING REQUESTS RESULTS FROM ANILIST   \033[0m")
for i in range (len(Title_list)):
  variables = {
      "search": Title_list[i][0],
      "type": "ANIME"
  }
  response = requests.post(url, json={"query":query, "variables": variables}, headers= headers)
  if (response.status_code == 200):
    dico = response.json()
    anime_id = dico["data"]["Media"]["id"]
    progress_id.append([[anime_id], [Title_list[i][1]]])
    print(response.json())


print("\033[92m   PRITING REQUESTS ID + EPISODE WATCHED  \033[0m")
print(progress_id)



def get_highest_progress(progress_id):
  id_dictionnary = {};
  for item in range(len(progress_id)):
      if (id_dictionnary[progress_id[i][0]] == None):
          id_dictionnary[progress_id[i][0]] = progress_id[i][1]
      else:
          if (id_dictionnary[progress_id[i][0]] < progress_id[i][1]):
              id_dictionnary[progress_id[i][0]] = progress_id[i][1];
  print(id_dictionnary);

get_highest_progress(progress_id)

