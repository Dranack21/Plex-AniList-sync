import requests 
import os
import json
from dotenv import load_dotenv, set_key


load_dotenv()

# This function gets plex key from hidden venv and returns the user history as a json 
# Args: none
# Notes: User is hard coded for now
# Return: The json with user watch history from tautulli

def Get_key_and_user_history():
	key = os.getenv('PLEX_KEY')
	if not key:
		raise Exception("PLEX_KEY environment variable not found")
	try:
		response = requests.get(key + "get_history", params={"user": "hugoa141"}, timeout=10)
		response.raise_for_status()  # Raise exception for 4XX/5XX responses
		print(f"Request successful: {response.status_code}")
		return response.json()
	except requests.exceptions.Timeout:
		raise Exception("Request to Tautulli timed out. Service might be down.")
	except requests.exceptions.ConnectionError:
		raise Exception("Failed to connect to Tautulli. Service might be down.")
	except requests.exceptions.HTTPError as e:
		raise Exception(f"HTTP error occurred: {e}")
	except json.JSONDecodeError:
		raise Exception("Could not parse response from Tautulli")
	except Exception as e:
		raise Exception(f"Unexpected error accessing user history: {str(e)}")


# This function takes a json as a parameter and fetches anime name + progress_id
# Args: a json that is rest api result from tautulli request
# Notes: we only count something as finished if I watched 70percent or more
# Return: A list of list containung title + progress_index + percent complete
def Search_for_title(dico):
	Title_list = []
	last_synch = os.getenv('LAST_SYNCH')
	last_synch = int(last_synch);
	if (dico):
		if (dico["response"]["result"] != "success"): 
			raise (f"Json file obtained from Tautulli is not correct")
		for item in dico["response"]["data"]["data"]:
			if (item["percent_complete"] > 70 and item["stopped"] > last_synch and item["grandparent_title"]):
				Title_list.append([item["grandparent_title"], item["media_index"], item["stopped"]])
		print("\033[94mPRINTING ANIME LIST FROM TAUTULLI\033[0m")
		if (Title_list):
			set_key('.env', 'LAST_SYNCH', str(Title_list[0][2]))
		else:
			raise(f"No anime watch history to update")
		for i in range (len(Title_list)):
			print(Title_list[i][0], Title_list[i][1], '|', Title_list[i][2])
		return (Title_list)



