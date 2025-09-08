import requests 
import os
import json
from dotenv import load_dotenv


load_dotenv()

def Get_key_and_user_history():
	key = os.getenv('PLEX_KEY')
	print(key)
	response = requests.get(key + "get_history", params={"user": "hugoa141"})
	if (response.status_code == 200):
		return (response.json())
	print("Could not access to user history")


##here this works cause dico is a json of the user history
def Search_for_title(dico):
	Title_list = []
	if (dico):
		if (dico["response"]["result"] != "success"): 
			return 0;
		for item in dico["response"]["data"]["data"]:
			if (item["percent_complete"] > 70 and item["grandparent_title"]):
				Title_list.append([item["grandparent_title"], item["media_index"], item["percent_complete"]])
		print("\033[94mPRINTING ANIME LIST FROM TAUTULLI\033[0m")
		for i in range (len(Title_list)):
			print(Title_list[i][0], Title_list[i][1], '|', Title_list[i][2])
		return (Title_list)



