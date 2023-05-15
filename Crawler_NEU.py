from bs4 import BeautifulSoup
import requests
import re

# URL of the main webpage
main_url = 'https://resources.infosecinstitute.com/topic/empire-breakout-vulnhub-ctf-walkthrough/'

# Send a request to the main webpage
main_page = requests.get(main_url)
html_content_main = main_page.text

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content_main, "html.parser")

# Find all the links on the webpage that start with the specified URL
links = soup.select("a[href^='https://resources.infosecinstitute.com/topic/']")

# List to store the extracted relevant information
relevant_information = []

# Iterate over the links and extract the relevant information from the challenge webpages
for link in links:
    challenge_url = link['href']
    challenge_name = challenge_url.split('/')[-2]
    
    # Send a request to the challenge webpage
    challenge_page = requests.get(challenge_url)
    html_content_challenge = challenge_page.text

    # Create a BeautifulSoup object to parse the HTML content of the challenge webpage
    soup_challenge = BeautifulSoup(html_content_challenge, "html.parser")
    
    # Find all text nodes that contain '<<' and '>>'
    relevant_tags = soup_challenge.find_all(string=re.compile(r'<<.*?>>'))
    
    # Append the challenge name and URL as a header
    relevant_information.append(f"Challenge Name: {challenge_name}\n")
    relevant_information.append(f"Challenge URL: {challenge_url}\n")
    
    # Extract the relevant information from the tags and append to the list
    for tag in relevant_tags:
        relevant_information.append(re.search(r'<<(.*?)>>', tag).group(1).strip())
    
    # Add a separator between challenge contents
    relevant_information.append('\n\n')

# Save the relevant information to the text file
with open("extracted_commands.txt", "w") as file:
    file.write("\n".join(relevant_information))

print("Relevant information extracted and saved to 'extracted_commands'")
