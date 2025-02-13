import requests
import json
from requests.auth import HTTPBasicAuth

# Constants
COMMVAULT_API_URL = "https://m036.metallic.io/"
COMMVAULT_USERNAME = "camarnathreddy@metallicsupportlab.com"
COMMVAULT_PASSWORD = "Deccom@2024#"
SHAREPOINT_SITE_URL = "http://metallicsupportlab.sharepoint.com/sites/ExampleTeamSite"

# Function to get the token
def get_commvault_token():
    url = f"{COMMVAULT_API_URL}/webconsole/api/Login"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        "username": COMMVAULT_USERNAME,
        "password": COMMVAULT_PASSWORD
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception(f"Failed to get Commvault token: {response.text}")

# Function to backup SharePoint site
def backup_sharepoint_site(token, site_url):
    url = f"{COMMVAULT_API_URL}/webconsole/api/Backup"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authtoken': token
    }
    data = {
        "taskInfo": {
            "subTasks": [{
                "subTask": {
                    "operationType": 1
                },
                "options": {
                    "backupOpts": {
                        "backupLevel": 2
                    }
                }
            }],
            "associations": [{
                "entity": {
                    "clientName": "SharePoint",
                    "appName": "SharePoint",
                    "instanceName": "DefaultInstance",
                    "backupsetName": site_url
                }
            }]
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        print(f"Backup job for {site_url} started successfully")
    else:
        raise Exception(f"Failed to start backup job: {response.text}")

def main():
    try:
        # Get Commvault token
        token = get_commvault_token()
        print("Successfully obtained Commvault token")

        # Backup SharePoint site
        backup_sharepoint_site(token, SHAREPOINT_SITE_URL)
        print("Backup process initiated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")