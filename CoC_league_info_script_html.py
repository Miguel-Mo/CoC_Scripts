import os
import requests
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

# Read API token and clan tag from files
api_token = read_file_content(api_key_path)
clan_tag = read_file_content(clan_tag_path)

# Check if data loaded correctly
if not api_token:
    raise ValueError("API token not provided. Ensure 'api_key.txt' contains the token.")
if not clan_tag:
    raise ValueError("Clan tag not provided. Ensure 'clan_tag.txt' contains the tag.")

# Function to get the clan league information
def get_league_data(clan_tag):
    url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar/leaguegroup"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    # Perform GET request to the API
    response = requests.get(url, headers=headers)
    
    # If the response is successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to get the last 3 wars of a clan
def get_last_wars(clan_tag, clan_name):
    url = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/warlog?limit=3"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    # Perform GET request to the API
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

# Function to count members by town hall level and sort clans
def count_members_by_th(clans):
    clan_summary = []

    for clan in clans:
        townhall_counts = Counter()

        # Iterate through clan members and count by town hall level
        for member in clan.get("members", []):
            townhall_level = member.get("townHallLevel")
            if townhall_level:
                townhall_counts[townhall_level] += 1

        # Filter only up to the first 15 levels (TH17, TH15, ..., TH2)
        filtered_count = {th: townhall_counts[th] for th in range(17, 1, -1)}
        
        # Get the history of the last 3 wars of the clan
        clan_tag = clan.get("tag").strip("#")
        wars = get_last_wars(clan_tag, clan.get("name"))
        
        # Process the last 3 wars
        war_results = []
        war_stars = []
        last_war_date = ""
        last_war_participants = 0
        
        if wars:
            for war in wars:
                war_results.append(
                    "Victory" if war.get("result") == "win" else 
                    "Tie" if war.get("result") == "tie" else 
                    "Defeat"
                )
                war_stars.append(war.get("clan").get("stars", 0))
                if not last_war_date:
                    last_war_date = datetime.strptime(war.get("endTime", "").split("T")[0], "%Y%m%d").strftime("%d/%m/%Y")
                    last_war_participants = war.get("teamSize", 0)
        
        # Create a summary for the clan
        clan_summary_entry = {
            "Clan Name": clan.get("name"),
            "TH Count": ", ".join([f"TH {th}: {count}" for th, count in filtered_count.items() if count > 0]),
            "Clan Level": clan.get("clanLevel"),
            "Last War Date": last_war_date,
            "Results of the Last 3 Wars": " - ".join(war_results),
            "Stars in the Last 3 Wars": " - ".join(map(str, war_stars)),
            "Participants in the Last War": last_war_participants,
            "TH Order": [filtered_count.get(th, 0) for th in range(16, 1, -1)]
        }
        clan_summary.append(clan_summary_entry)
    
    # Sort clans by TH level in descending order
    clan_summary = sorted(clan_summary, key=lambda x: x["TH Order"], reverse=True)

    return clan_summary

# Function to save data to an HTML file
def save_data_to_html(clan_summary):
    # Create HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clan League Prediction and Info</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f4f4f4;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #009688;
                color: white;
            }
            h1 {
                text-align: center;
                color: #009688;
            }
            .green-bg {
                background-color: #e6f9e6; /* Very pale green */
            }
            .red-bg {
                background-color: #fde8e8; /* Very pale red */
            }
        </style>
    </head>
    <body>
        <h1>Clan League Prediction and Info</h1>
        <table>
            <tr>
                <th>Clan Name</th>
                <th>TH Count</th>
                <th>Clan Level</th>
                <th>Last War Date</th>
                <th>Results of the Last 3 Wars</th>
                <th>Stars in the Last 3 Wars</th>
                <th>Participants in the Last War</th>
            </tr>
    """

    # Add rows to the table for each clan
    for index, clan in enumerate(clan_summary):
        # Apply colors to the rows based on their position
        row_class = ""
        if index < 2:
            row_class = "green-bg"  # Very pale green for the first two rows
        elif index >= len(clan_summary) - 2:
            row_class = "red-bg"  # Very pale red for the last two rows

        html_content += f"""
            <tr class="{row_class}">
                <td>{clan['Clan Name']}</td>
                <td>{clan['TH Count']}</td>
                <td>{clan['Clan Level']}</td>
                <td>{clan['Last War Date']}</td>
                <td>{clan['Results of the Last 3 Wars']}</td>
                <td>{clan['Stars in the Last 3 Wars']}</td>
                <td>{clan['Participants in the Last War']}</td>
            </tr>
        """
    
    # Closing the HTML
    html_content += """
            </table>
        </body>
    </html>
    """

    # Save the HTML file
    current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") 
    file_name = f"clans_league_{current_date_time}.html"
    results_folder = os.path.abspath('results')
    os.makedirs(results_folder, exist_ok=True)

    file_path = os.path.join(results_folder, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Data saved in {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Get and process clan league data
league_data = get_league_data(clan_tag)
if league_data:
    clan_summary = count_members_by_th(league_data["clans"])
    save_data_to_html(clan_summary)
else:
    print("No league data obtained.")
