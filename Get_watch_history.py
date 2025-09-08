import requests 
import os
import json
from dotenv import load_dotenv


load_dotenv()

# This function gets plex key from hidden venv and returns the user history as a json 
# Args: none
# Notes: User is hard coded for now
# Return: The json with user watch history from tautulli

def Get_key_and_user_history():
    key = os.getenv('PLEX_KEY')
    response = requests.get(key + "get_history", params={"user": "hugoa141"})
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Could not access user history. Status code: {response.status_code}")


# This function takes a json as a parameter and fetches anime name + progress_id
# Args: a json that is rest api result from tautulli request
# Notes: we only count something as finished if I watched 70percent or more
# Return: A list of list containung title + progress_index + percent complete
def Search_for_title(dico):
	Title_list = []
	if (dico):
		if (dico["response"]["result"] != "success"): 
			raise (f"Json file obtained from Tautulli is not correct")
		for item in dico["response"]["data"]["data"]:
			if (item["percent_complete"] > 70 and item["grandparent_title"]):
				Title_list.append([item["grandparent_title"], item["media_index"], item["percent_complete"]])
		print("\033[94mPRINTING ANIME LIST FROM TAUTULLI\033[0m")
		for i in range (len(Title_list)):
			print(Title_list[i][0], Title_list[i][1], '|', Title_list[i][2])
		return (Title_list)



