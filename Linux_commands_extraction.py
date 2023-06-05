import os
import requests
from bs4 import BeautifulSoup

url = "https://linuxcommandlibrary.com/commands"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all <a> tags with the specified pattern
command_links = soup.find_all("a", href=lambda href: href and href.startswith("man/"))

# Extract the relevant information from each link and store it in a list
relevant_info = [link["href"].replace("man/", "") for link in command_links]

# Generate the output text
output_text = "\n".join(relevant_info)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the file path by joining the current directory with the filename
file_path = os.path.join(current_dir, "linux_commands.txt")

# Write the output text to the file
with open(file_path, "w") as file:
    file.write(output_text)

print(f"Extraction complete. Output saved in '{file_path}' file.")
