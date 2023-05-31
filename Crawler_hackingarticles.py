# Library import
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Set the main URL
main_url = 'https://www.hackingarticles.in/ctf-challenges-walkthrough/'

# List to store the extracted information
extracted_information = []

# Set to store unique challenges
unique_challenges = set()

# Counter for the total number of challenges
challenge_counter = 0

# Send a request to the main page
main_page = requests.get(main_url)
html_content_main = main_page.text

# Create a BeautifulSoup object to parse the HTML content of the main page
soup_main = BeautifulSoup(html_content_main, "html.parser")

# Find the div section containing the individual challenges
div_section = soup_main.find("div", class_="post-excerpt entry-content")

# Find all the <strong> tags within the div section
strong_tags = div_section.find_all("strong")

# Iterate over the strong tags and extract information from each challenge
for strong_tag in strong_tags:
    # Find the <a> tag within the strong tag
    a_tag = strong_tag.find("a")
    if a_tag is None:
        continue

    # Find the URL of the challenge
    url = a_tag['href']

    # Check if the URL meets the filtering criteria
    if 'hackthebox' not in url and 'tryhackme' not in url and 'vulnhub-walkthrough' not in url and 'hack-the-box' not in url and 'ctf-challenge' not in url:
        continue

    # Check if the challenge URL has already been processed
    if url in unique_challenges:
        continue

    # Store the challenge URL in the set of unique challenges
    unique_challenges.add(url)

    # Check if the URL is missing the scheme and add it if necessary
    if not url.startswith("http"):
        url = urljoin(main_url, url)

    # Send a request to the challenge page
    challenge_page = requests.get(url)
    html_content_challenge = challenge_page.text

    # Create a BeautifulSoup object to parse the HTML content of the challenge page
    soup_challenge = BeautifulSoup(html_content_challenge, "html.parser")

    # Extract the relevant information based on the URL pattern
    if 'hackthebox' in url or 'tryhackme' in url:
        relevant_tags = soup_challenge.select("div.enlighter-raw, pre.EnlighterJSRAW")
        commands = [tag.text.strip() for tag in relevant_tags] if relevant_tags else []
    elif 'vulnhub-walkthrough' in url or 'hack-the-box' in url or 'ctf-challenge' in url:
        relevant_tags = soup_challenge.find_all("pre", class_="lang:default decode:true")
        commands = [tag.text.strip() for tag in relevant_tags] if relevant_tags else []
    else:
        commands = []

    # Skip writing to the text file if no commands are extracted
    if not commands:
        continue

    # Append the challenge information and commands to the list
    extracted_information.append(f"Challenge URL: {url}")
    extracted_information.extend(commands)
    extracted_information.append('\n\n')

    # Increment the challenge counter
    challenge_counter += 1

    # Print progress indicators
    print(f"Processed {challenge_counter} challenges")

# Save the extracted information to a text file
output_file = "extracted_commands_hackingarticles.txt"
script_directory = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_directory, output_file)

with open(output_path, "w") as file:
    file.write("\n".join(extracted_information))

print(f"Extracted information saved to '{output_path}'")
