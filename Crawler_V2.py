import os
from bs4 import BeautifulSoup
import requests
import re

# Set the main URL
main_url = 'https://resources.infosecinstitute.com/topics/capture-the-flag/'

# Number of pages to scrape (including the main URL)
num_pages = 27

# List to store the extracted information
extracted_information = []

# Set to store unique challenges
unique_challenges = set()

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
    page = requests.get(page_url)
    html_content = page.text

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the links to individual challenges on the page
    links = soup.select("a[href^='https://resources.infosecinstitute.com/topic/']")

    # Iterate over the links and extract information from each challenge page
    for link in links:
        challenge_url = link['href']
        challenge_name = challenge_url.split('/')[-2]

        # Check if the challenge has already been processed
        if (challenge_url, challenge_name) in unique_challenges:
            continue

        # Send a request to the challenge page
        challenge_page = requests.get(challenge_url)
        html_content_challenge = challenge_page.text

        # Create a BeautifulSoup object to parse the HTML content of the challenge page
        soup_challenge = BeautifulSoup(html_content_challenge, "html.parser")

        # Find all text nodes that contain '<<' and '>>'
        relevant_tags = soup_challenge.find_all(string=re.compile(r'<<.*?>>'))

        # Extract the comments from the tags
        comments = [re.search(r'<<(.*?)>>', tag).group(1).strip() for tag in relevant_tags]

        # Append the challenge information and comments to the list
        extracted_information.append(f"Challenge Name: {challenge_name}")
        extracted_information.append(f"Challenge URL: {challenge_url}")
        extracted_information.extend(comments)
        extracted_information.append('\n')

        # Add the challenge URL and name to the set of unique challenges
        unique_challenges.add((challenge_url, challenge_name))

        # Increment the challenge counter
        challenge_counter += 1

        # Print progress indicators
        print(f"Processing Challenge {challenge_counter} on Page {page_num+1}/{num_pages}")

# Get the directory path of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the output file path
output_file = os.path.join(script_directory, "extracted_commands_infosecinstitute_V2.txt")

# Insert the challenge counter at the beginning of the extracted information
extracted_information.insert(0, f"Total Challenges: {challenge_counter}\n\n")

# Save the extracted information to a text file
with open(output_file, "w") as file:
    file.write("\n".join(extracted_information))

print(f"Extracted information saved to '{output_file}'")
