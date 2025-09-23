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
		response.raise_for_status()
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
	key = os.getenv('PLEX_KEY')
	if (dico):
		if (dico["response"]["result"] != "success"): 
			raise (f"Json file obtained from Tautulli is not correct")
		for item in dico["response"]["data"]["data"]:
			if (item["percent_complete"] > 70 and item["stopped"] > last_synch and item["grandparent_title"]):
				season_air_time = Find_air_time(item, item["parent_rating_key"], item["media_index"])
				season_response = requests.get(key + "get_metadata", params={"rating_key": item["parent_rating_key"]}, timeout=10)
				season_data = season_response.json()
				max_episodes = season_data["response"]["data"]["children_count"]
				Title_list.append([item["grandparent_title"], item["media_index"], item["stopped"], season_air_time, max_episodes])
		print("\033[94mPRINTING ANIME LIST FROM TAUTULLI\033[0m")
		if (Title_list):
			set_key('.env', 'LAST_SYNCH', str(Title_list[0][2]))
		else:
			raise(f"No anime watch history to update")
		for i in range (len(Title_list)):
			print(Title_list[i][0], Title_list[i][1], '|', Title_list[i][3], '| Max episodes:', Title_list[i][4])
		return (Title_list)

def Find_air_time(item, parent_rating_key, media_index, filename=".airtimes.json"):
    if media_index == 1:
        string = item["originally_available_at"]
        string = string.replace('-', '')
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data[str(parent_rating_key)] = string
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return int(string)
    else:
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        air_time = data.get(str(parent_rating_key))
        return int(air_time) if air_time else None