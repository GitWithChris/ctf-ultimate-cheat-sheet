import os
from bs4 import BeautifulSoup
import requests
import re

# Setting the main URL
main_url = 'https://resources.infosecinstitute.com/topics/capture-the-flag/'

# Send a request to the main webpage
main_page = requests.get(main_url)
html_content_main = main_page.text

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content_main, "html.parser")

# Find all the links on the webpage that start with the specified URL
links = soup.select("a[href^='https://resources.infosecinstitute.com/topics/capture-the-flag/']")

# List to store the extracted relevant information
relevant_information = []

# Challenge counter
challenge_counter = 0

# Unique challenges only
extracted_challenges = set()

# Iterate over the links and extract the relevant information from the challenge webpages
for link in links:
    challenge_url = link['href']
    challenge_name = challenge_url.split('/')[-2]

    # Duplicate check
    if (challenge_url, challenge_name) in extracted_challenges:
        continue

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

    # Increment challenge counter
    challenge_counter += 1

    # Add the challenge to the set of extracted challenges
    extracted_challenges.add((challenge_url, challenge_name))

# Create the directory if it doesn't exist
output_directory = "output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save the relevant information to the text file
output_file = os.path.join(output_directory, "extracted_commands_capturetheflag.txt")
with open(output_file, "w") as file:
    file.write("\n".join(relevant_information))
    file.write(f"Number of Challenges Extracted: {challenge_counter}")

print(f"Relevant information extracted and saved to '{output_file}'")
