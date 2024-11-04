import os
import requests
import pandas as pd
from collections import Counter
from datetime import datetime

# Function to read content from txt files
def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None

# File paths
info_folder_path = 'info_to_add'
api_key_path = os.path.join(info_folder_path, 'api_key.txt')
clan_tag_path = os.path.join(info_folder_path, 'clan_tag.txt')

# Read the API token and clan tag from the files
api_token = read_file_content(api_key_path)
clan_tag = read_file_content(clan_tag_path)

# Check if the data was loaded correctly
if not api_token:
    raise ValueError("API token not provided. Make sure 'api_key.txt' contains the token.")
if not clan_tag:
    raise ValueError("Clan tag not provided. Make sure 'clan_tag.txt' contains the tag.")

# Function to get the league information of the clan
def get_league_data(clan_tag):
    url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar/leaguegroup"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    # Perform the GET request to the API
    response = requests.get(url, headers=headers)
    
    # If the response is successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to get the last 3 wars of a clan
def get_latest_wars(clan_tag, clan_name):
    url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/warlog?limit=3"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    # Perform the GET request to the API
    response = requests.get(url, headers=headers)
    
    # If the response is successful (status code 200)
    if response.status_code == 200:
        return response.json().get("items", [])
    elif response.status_code == 403:
        print(f"Error {response.status_code}: {clan_name} denied access")
        return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to count members by town hall level
def count_members_by_th(clans):
    clan_summary = []

    for clan in clans:
        townhall_counts = Counter()

        # Iterate over the clan members and count by town hall level
        for member in clan.get("members", []):
            townhall_level = member.get("townHallLevel")
            if townhall_level:
                townhall_counts[townhall_level] += 1

        # Get the history of the last 3 wars of the clan
        clan_tag = clan.get("tag").strip("#")
        wars = get_latest_wars(clan_tag, clan.get("name"))
        
        # Process the last 3 wars
        war_results = []
        stars_wars = []
        last_war_date = ""
        last_war_participants = 0
        
        if wars:
            for war in wars:
                war_results.append(
                    "Victory" if war.get("result") == "win" else 
                    "Tie" if war.get("result") == "tie" else 
                    "Defeat"
                )
                stars_wars.append(war.get("clan").get("stars", 0))
                if not last_war_date:
                    last_war_date = datetime.strptime(war.get("endTime", "").split("T")[0], "%Y%m%d").strftime("%d/%m/%Y")
                    last_war_participants = war.get("teamSize", 0)
        
        # Create a summary for the clan
        clan_summary_entry = {
            "Clan Name": clan.get("name"),
            "TH Count": ", ".join([f"TH {th}: {count}" for th, count in sorted(townhall_counts.items(), reverse=True)]),
            "Clan Level": clan.get("clanLevel"),
            "Last War Date": last_war_date,
            "Results of Last 3 Wars": " - ".join(war_results),
            "Stars in Last 3 Wars": " - ".join(map(str, stars_wars)),
            "Participants in Last War": last_war_participants
        }
        clan_summary.append(clan_summary_entry)
    
    return clan_summary

# Function to save the data to an Excel file
def save_data_to_excel(clan_summary):
    # Convert the summary into a pandas DataFrame
    data = {
        "Clan Name": [clan["Clan Name"] for clan in clan_summary],
        "TH Count": [clan["TH Count"] for clan in clan_summary],
        "Clan Level": [clan["Clan Level"] for clan in clan_summary],
        "Last War Date": [clan["Last War Date"] for clan in clan_summary],
        "Results of Last 3 Wars": [clan["Results of Last 3 Wars"] for clan in clan_summary],
        "Stars in Last 3 Wars": [clan["Stars in Last 3 Wars"] for clan in clan_summary],
        "Participants in Last War": [clan["Participants in Last War"] for clan in clan_summary]
    }
    
    df = pd.DataFrame(data)

    # Get the current date and time for the file name
    current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # Date format dd-mm-yyyy
    file_name = f"clans_league_{current_datetime}.xlsx"
    
    # Path for the 'results' folder and creation if it doesn't exist
    results_folder = 'results'
    os.makedirs(results_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Complete path for the file in the 'results' folder
    file_path = os.path.join(results_folder, file_name)

    # Save the data to an Excel file in the 'results' folder
    df.to_excel(file_path, index=False)
    print(f"Data saved in {file_path}")

# Get the league data of the clan
league_data = get_league_data(clan_tag)

# If the data was obtained successfully, count and save it in an Excel file
if league_data:
    clan_summary = count_members_by_th(league_data["clans"])
    save_data_to_excel(clan_summary)
