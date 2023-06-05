# Library import
import os                           # Provides functions to interact with the operating system f.e. creating, deleting directories
from bs4 import BeautifulSoup       # BeautifulSoup = Python library for web scraping (provides methods for parsing HTML and XML content)
import requests                     # Used for making HTTP requests (Sending requests and handling the response)
import re                           # Regular expressions (Tool for pattern matching and manipulation of strings)

# Set the main URL
main_url = 'https://resources.infosecinstitute.com/topics/capture-the-flag/'

# Number of pages to scrape (including the main URL)
num_pages = 27

# List to store the extracted information
extracted_information = []      # Creating empty list

# Set to store unique challenges
unique_challenges = set()       # Set() = Ungeordnete Sammlung von einzigartigen Elementen --> Vermeiden von URL Duplikaten, jede URL wird nur einmal herangezogen

# Counter for the total number of challenges
challenge_counter = 0

# Iterate over each page
for page_num in range(num_pages):
    # Set the URL for the current page
    if page_num == 0:
        page_url = main_url
    else:
        page_url = main_url + f'page/{page_num}/'

    # Send a request to the page
    page = requests.get(page_url)       # Retrieves the content of the referrenced URL and stores the response in a variable
    html_content = page.text            # Extracts the (written) HTML content of the response

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")       # Soup Objekt erstellen. Übergebenen Argumente sind der zu parsende HTML content (html_content_main) und der parser tyo (html.parser)

    # Find all the links to individual challenges on the page
    links = soup.select("a[href^='https://resources.infosecinstitute.com/topic/']")     # soup.select um alle ('a') tags zu finden, welche mit der spezifischen URL (= main URL bis ...topic/) anfangen ('href'). soup.select returnt eine Liste (--> links = list)

    # Iterate over the links and extract information from each challenge page
    for link in links:
        challenge_url = link['href']                        # pro Iteration wird die aktuelle URL aus der Liste in eine Variable gespeichert
        challenge_name = challenge_url.split('/')[-2]       # Challenge Name wird extrahiert, indem man die URL am '/' aufsplitted und die Inhalte ab dem zweitletzten '/' nimmt ([-2])

        # Check if the challenge has already been processed
        if (challenge_url, challenge_name) in unique_challenges:        # falls Challenge_URL und Challenge_name schon im set geführt werden -->
            continue                                                    # --> Überspringen des Loops. Andernfalls wird die Schleife fortgesetzt

        # Check if the URL meets the filtering criteria
        if 'walkthrough' not in challenge_url:                          # URL muss 'walkthrough' enthalten
            continue
        if 'ctf' not in challenge_url and 'capture-the-flag' not in challenge_url:      # zusätzlich muss die URL entweder 'ctf' oder 'capture-the-flag' enthalten
            continue

        # Send a request to the challenge page
        challenge_page = requests.get(challenge_url)
        html_content_challenge = challenge_page.text

        # Create a BeautifulSoup object to parse the HTML content of the challenge page
        soup_challenge = BeautifulSoup(html_content_challenge, "html.parser")

        # Find all text nodes that contain '<<' and '>>'
        relevant_tags = soup_challenge.find_all(string=re.compile(r'<<.*?>>'))  # Find relevant tags using existing method

        # Extract the commands from the tags
        commands = [re.search(r'<<(.*?)>>', tag).group(1).strip() for tag in relevant_tags]

        # Check if the commands list is empty
        if not commands:
            # Find all <em> tags in the HTML
            em_tags = soup_challenge.find_all('em')

            # Extract the relevant information from the <em> tags
            commands = [em_tag.text.strip() for em_tag in em_tags]

        # Check if the commands list is still empty
        if not commands:
            # Find all <strong> tags in the HTML
            strong_tags = soup_challenge.find_all('strong')

            # Iterate over the <strong> tags and extract relevant information
            for strong_tag in strong_tags:
                if strong_tag.text.startswith('Command used:'):
                    commands.append(strong_tag.text.replace('Command used:', '').strip())

        # Append the challenge information and commands to the list
        extracted_information.append(f"Challenge Name: {challenge_name}")
        extracted_information.append(f"Challenge URL: {challenge_url}")
        extracted_information.append("")
        extracted_information.extend(commands)
        extracted_information.append('\n\n')

        # Add the challenge URL and name to the set of unique challenges
        unique_challenges.add((challenge_url, challenge_name))      # pro Iteration: aktuelle Challenge in set mit aufnehmen

        # Increment the challenge counter
        challenge_counter += 1

        # Print progress indicators
        print(f"Processing Challenge {challenge_counter} on Page {page_num+1}/{num_pages}")     # Verfolgen des Compiling-Prozesses

# Get the directory path of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the output file path
output_file = os.path.join(script_directory, "extracted_commands_infosecinstitute.txt")

# Insert the challenge counter at the beginning of the extracted information
extracted_information.insert(0, f"Total Challenges: {challenge_counter}\n\n")

# Save the extracted information to a text file
with open(output_file, "w") as file:                    # Öffnen / Anlegen einer Txt-Datei
    file.write("\n".join(extracted_information))        # die Inhalte der Liste werden in die Txt-Datei geschrieben. Join-Befehl fügt die einzelnen Einträge der Liste mit jeweils einem Absatz in der Txt-Datei zusammen

print(f"Extracted information saved to '{output_file}'")        # Konsolenmeldung
