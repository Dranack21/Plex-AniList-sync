import requests 
import json

# # Here we define our query as a multi-line string
# query = '''
# query ($id: Int)# Define which variables will be used in the query (id)
# { 
#   Media (id: $id, type: ANIME) # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
#   { 
#     id
#     title {
#       romaji
#       english
#       native
#     }
#   }
# }
# '''

# # Define our query variables and values that will be used in the query request
# variables = {
#     'id': 15125
# }

# url = 'https://graphql.anilist.co'

# # Make the HTTP Api request
# response = requests.post(url, json={'query': query, 'variables': variables})
# dico2 = response.json()
# print (dico2["romaji"])

def Get_key():
	f = open(".env")
	key = f.readline().strip('\n')
	response = requests.get(key + "get_history", params={"user": "hugoa141"})
	if (response.status_code == 200):
		return (response.json())
	else:
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