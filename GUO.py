import requests
import time
import keyboard
from pymongo import MongoClient

access_token = "asd"
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

def SleepByNextRequest():
    try:
        for iS in range(60):
            if keyboard.is_pressed("space"):
                print("\nCountdown stopped by pressing space key while 1 second.")
                break  # Exit the inner loop
            print(f"\rSleeping for [00:{59-iS:02}]; Press any key to stop countdown.", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCountdown stopped.")

iRequestCounter = 0
def requestToGit( url, params ):
    global headers
    while True:
        try:
            response = requests.get( url, params=params, headers=headers )
            if response.status_code == 200:
                return response.json()
            elif response.reason == 'Forbidden' or response.reason == 'Conflict' or response.reason == 'Unknown':
                return None
            else:
                SleepByNextRequest()
        except:
            print("Network Error")
            SleepByNextRequest()
            print("\nNow Trying Again...")

login = "riceboyler"

# get repository
user_url = f"https://api.github.com/users/{login}/repos"
user_repos = requestToGit(user_url, params = {'page': 1, 'per_page': 1})
user_name = ''
email_adr = ''
if len(user_repos) > 0:
    repos_name = user_repos[0]['full_name']
    commit_data = requestToGit( f"https://api.github.com/repos/{repos_name}/commits", params = {'page': 1, 'per_page': 1})
    if commit_data and len(commit_data) > 0:
        user_name = commit_data[0]['commit']['author']['name']
        email_adr = commit_data[0]['commit']['author']['email']

# Extract location, email, and join date
user_info = {
    "login": login,
    "name": user_name,
    "email": email_adr
}
print(f"result: {user_info}")