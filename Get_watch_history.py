import requests 
import os
import json
from dotenv import load_dotenv

load_dotenv()

def Get_key():
	key = os.getenv('PLEX_KEY')
	print(key)
	response = requests.get(key + "get_history", params={"user": "hugoa141"})
	if (response.status_code == 200):
		return (response.json())
	print("Could not access to user history")

def Search_for_title(dico):
	Title_list = []
	if (dico):
		if (dico["response"]["result"] != "success"): 
			return 0;
		for item in dico["response"]["data"]["data"]:
			if (item["percent_complete"] > 70):
				Title_list.append([item["full_title"], item["percent_complete"]])
		for i in range (len(Title_list)):
			print(Title_list[i][0], Title_list[i][1])
	

dico = Get_key()
Search_for_title(dico)

