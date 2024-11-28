import requests
import time
import keyboard
from pymongo import MongoClient

access_token = "asd"
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

dateJoinedFrom = '2012-05-23T08:45:22Z'
originCount = collectionList.count_documents({"created_at": {"$lte": dateJoinedFrom}})
iCount = 0
user_datas = collectionList.find({"created_at": {"$gt": dateJoinedFrom}})
for user in user_datas:
    user_name = user['login']
    user_url = f"https://api.github.com/users/{user_name}"
    user_data = requestToGit(user_url, params = {})
    new_data = { "$set":
                { "repos_count": user_data['public_repos'],
                "gists": user_data.get("public_gists"),
                "followers": user_data.get("followers"),
                "following": user_data.get("following"),
                "updated_at": user_data.get("updated_at") } }
    collectionList.update_one( {'login': user_name}, new_data )
    iCount += 1
    print( f"\rcount : {originCount+iCount}/{iCount}, {user_name}, repos_count: {user_data['public_repos']}, created_at: {user_data['created_at']}, gists: {user_data['public_gists']}, followers: {user_data['followers']}, following: {user_data['following']}, updated_at: {user_data['updated_at']}                ", end="" )