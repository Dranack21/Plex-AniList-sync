import requests
import os
import json
from dotenv import load_dotenv
from Get_watch_history import Get_key
from Get_watch_history import Search_for_title

load_dotenv()
ACCESS_TOKEN = os.getenv('ANI_TOKEN')
url =  "https://graphql.anilist.co"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
query = '''
query Studio($search: String) {
  Studio(search: $search) {
    siteUrl
    name
    isAnimationStudio
    id
  }
}
'''

dico = Get_key()


Title_list = Search_for_title(dico)

for i in range (len(Title_list)):
  variables = {
      "search": ""
  }

response = requests.post(url, json={"query":query, "variables": variables}, headers= headers)
print(response)
print(response.json())	

