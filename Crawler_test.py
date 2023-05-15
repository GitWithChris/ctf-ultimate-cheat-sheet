from bs4 import BeautifulSoup
import requests

# URL of the main webpage
main_url = 'https://resources.infosecinstitute.com/topic/empire-breakout-vulnhub-ctf-walkthrough/'

# Send a request to the main webpage
main_page = requests.get(main_url)
html_content_main = main_page.text

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content_main, "html.parser")

# Find all the links on the webpage that start with the specified URL
links = soup.select("a[href^='https://resources.infosecinstitute.com/topic/']")

# List to store the extracted challenge HTML contents
challenge_contents = []

# Iterate over the links and extract the HTML contents of the challenge webpages
for link in links:
    challenge_url = link['href']
    
    # Send a request to the challenge webpage
    challenge_page = requests.get(challenge_url)
    html_content_challenge = challenge_page.text

    # Append the HTML content to the list
    challenge_contents.append(html_content_challenge)

# Save the HTML contents to a text file
with open("Test123.txt", "w") as file:
    file.write("\n\n".join(challenge_contents))

print("HTML contents of all challenges saved to 'Test123.txt'")


