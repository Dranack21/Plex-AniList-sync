import requests
import os
import json
from dotenv import load_dotenv

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

variables = {
    "search": "Kyoto Animation"
}



response = requests.post(url, json={"query":query, "variables": variables}, headers= headers)
print(response)
print(response.json())	

