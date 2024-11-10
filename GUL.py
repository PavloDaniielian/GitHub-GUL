import requests
import time
import keyboard
from pymongo import MongoClient

access_token = "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"
headers = { "Authorization": f"token {access_token}" }

def SleepForHour():
    try:
        for iM in range(60):
            for iS in range(60):
                if keyboard.is_pressed("space"):
                    print("\nCountdown stopped by pressing space key while 1 second.")
                    break  # Exit the inner loop
                print(f"\rSleeping during : [{59-iM:02}:{59-iS:02}]; Press any key to stop countdown.", end="")
                time.sleep(1)
            else:
                continue
            break
    except KeyboardInterrupt:
        print("\nCountdown stopped.")

iRequestCounter = 0
def requestToGit( url, params ):
    global headers
    while True:
        response = requests.get( url, params=params, headers=headers )
        if response.status_code == 200:
            return response.json()
        elif response.reason == 'Forbidden' or response.reason == 'Conflict' or response.reason == 'Unknown':
            return None
        else:
            SleepForHour()

# Connect to the local MongoDB server (default port is 27017)
client = MongoClient("mongodb://localhost:27017/")
# Access a specific database
db = client['MyDatas']  # Replace 'mydatabase' with your database name
# Access a specific collection
collectionList = db['GitHub_Users']  # Replace 'mycollection' with your collection name

dateJoinedLast = '2000-01-01T00:00:00Z'
dateJoinedFrom = '2000-01-01T00:00:00Z'
current_count = collectionList.count_documents({})
if current_count > 0:
    latest_doc = collectionList.find_one( sort=[("created_at", -1)] )
    dateJoinedFrom = latest_doc['created_at']

page = 1

while True:
    if page >= 35:
        page = 1
        dateJoinedFrom = dateJoinedLast

    # Fetch users matching the search criteria
    data = requestToGit("https://api.github.com/search/users", {'q': ("language:CSharp type:User created:>"+dateJoinedFrom), 'sort': 'joined', 'order': 'asc', 'page': page, 'per_page': 30})
    print(f"currentPage : {page}, catched_count : {current_count+(page-1)*30}")

    # Store each user's login name for detailed profile fetch
    user_logins = [user['login'] for user in data['items']]
    # Get detailed info for each user
    for login in user_logins:
        user_url = f"https://api.github.com/users/{login}"
        user_data = requestToGit(user_url,params = {})

        # get repository
        user_url = f"https://api.github.com/users/{login}/repos"
        user_repos = requestToGit(user_url, params = {'page': 1, 'per_page': 1})
        email_adr = ''
        if len(user_repos) > 0:
            repos_name = user_repos[0]['full_name']
            commit_data = requestToGit( f"https://api.github.com/repos/{repos_name}/commits", params = {'page': 1, 'per_page': 1})
            if commit_data and len(commit_data) > 0:
                email_adr = commit_data[0]['commit']['author']['email']
        
        # Extract location, email, and join date
        user_info = {
            "login": login,
            "name": user_data.get("name"),
            "company": user_data.get("company"),
            "location": user_data.get("location"),
            "email": email_adr,
            "created_at": user_data.get("created_at")
        }
        print(user_info)
        collectionList.insert_one( user_info )
        dateJoinedLast = user_data.get("created_at")

    page += 1