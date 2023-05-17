# Importing the necessary libraries 
from bs4 import BeautifulSoup       # BeautifulSoup = Python library for web scraping (provides methods for parsing HTML and XML content)
import requests                     # Used for making HTTP requests (Sending requests and handling the response)
import re                           # Regular expressions (Tool for pattern matching and manipulation of strings)

# Setting URL of the main webpage
main_url = 'https://resources.infosecinstitute.com/topic/empire-breakout-vulnhub-ctf-walkthrough/'

# Send a request to the main webpage
main_page = requests.get(main_url)      # Retrieves the content of the referrenced URL and stores the response in a variable
html_content_main = main_page.text      # Extracts the (written) HTML content of the response

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content_main, "html.parser")      # Soup Objekt erstellen. Übergebenen Argumente sind der zu parsende HTML content (html_content_main) und der parser tyo (html.parser)

# Find all the links on the webpage that start with the specified URL
links = soup.select("a[href^='https://resources.infosecinstitute.com/topic/']")     # soup.select um alle ('a') tags zu finden, welche mit der spezifischen URL (= main URL bis ...topic/) anfangen ('href'). soup.select returnt eine Liste (--> links = list)

# List to store the extracted relevant information
relevant_information = []       # leere Liste initialisieren


# Iterate over the links and extract the relevant information from the challenge webpages
for link in links:      
    challenge_url = link['href']                        # pro Iteration wird die aktuelle URL aus der Liste in eine Variable gespeichert
    challenge_name = challenge_url.split('/')[-2]       # Challenge Name wird extrahiert, indem man die URL am '/' aufsplitted und die Inhalte ab dem zweitletzten '/' nimmt ([-2])
    
    # Send a request to the challenge webpage
    challenge_page = requests.get(challenge_url)
    html_content_challenge = challenge_page.text

    # Create a BeautifulSoup object to parse the HTML content of the challenge webpage
    soup_challenge = BeautifulSoup(html_content_challenge, "html.parser")
    
    # Find all text nodes that contain '<<' and '>>'
    relevant_tags = soup_challenge.find_all(string=re.compile(r'<<.*?>>'))      # alle text nodes in der HTML finden (.find_all(string)) mit einem vorgegebenen Muster (re.compile(r'<<.*?>>')). re.compile --> bei häufigen, ähnlichen Abfragen
    
    # Append the challenge name and URL as a header
    relevant_information.append(f"Challenge Name: {challenge_name}\n")      # Challenge Name pro Iteration in Liste schreiben
    relevant_information.append(f"Challenge URL: {challenge_url}\n")        # Challenge URL pro Iteration in Liste schreiben
    
    # Extract the relevant information from the tags and append to the list
    for tag in relevant_tags:
        relevant_information.append(re.search(r'<<(.*?)>>', tag).group(1).strip())      # nur die Inhalte extrahieren, welche zwischen '<< ' und ' >>' stehen. Diese anschließend an Liste anhängen
    
    # Add a separator between challenge contents
    relevant_information.append('\n\n')


# Save the relevant information to the text file
with open("extracted_commands_infosecinstitute.txt", "w") as file:      # Öffnen / Anlegen einer Txt-Datei
    file.write("\n".join(relevant_information))                         # die Inhalte der Liste werden in die Txt-Datei geschrieben. Join-Befehl fügt die einzelnen Einträge der Liste mit jeweils einem Absatz in der Txt-Datei zusammen

print("Relevant information extracted and saved to 'extracted_commands_infosecinstitute'")      # Konsolenmeldung, um Ende des Durchlaufes zu Visualisieren

