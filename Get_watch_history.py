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
	if (response.status_code == 200):
		return (response.json())
	print("Could not access to user history")


# This function looks if an anime that appeared in the watch history is COMPLETED or REPEATING and updates to the other one if needed
# Args: Two ints anime_id which is the id for ani list to recognize the anime and progress the number of episodes watched
# Notes: One piece kai is not present on my AniList so it's hard coded since it made things I didnt watch set as watched
# Return: Nothing
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



