import requests
import time
import keyboard
from pymongo import MongoClient

access_token = "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"
headers = { "Authorization": f"token {access_token}" }

def SleepFor10Seconds():
    try:
        for iS in range(10):
            if keyboard.is_pressed("space"):
                print("\nCountdown stopped by pressing space key while 1 second.")
                break  # Exit the inner loop
            print(f"\rSleeping during : [00:{59-iS:02}]; Press any key to stop countdown.", end="")
            time.sleep(1)
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
            SleepFor10Seconds()

# Connect to the local MongoDB server (default port is 27017)
client = MongoClient("mongodb://localhost:27017/")
# Access a specific database
db = client['MyDatas']  # Replace 'mydatabase' with your database name
# Access a specific collection
collectionList = db['GitHub_Users']  # Replace 'mycollection' with your collection name

dateJoinedFrom = '2011-01-07T15:32:22Z'
user_datas = collectionList.find({"created_at": {"$gt": dateJoinedFrom}})
iCount = 0
for user in user_datas:
    user_name = user['login']
    user_url = f"https://api.github.com/users/{user_name}/repos"
    user_repos = requestToGit(user_url, params = {})
    repos_count = len(user_repos)
    new_data = {"$set": {"repos_count": repos_count}}
    collectionList.update_one( {'login': user_name}, new_data )
    iCount += 1
    print( f"\rcurrent : {iCount}, {user_name}, repos_count: {repos_count}, created_at: {user['created_at']}                                                  ", end="" )