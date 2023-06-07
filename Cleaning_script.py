import os
import re

# Function to compare the string preceding the first space of two strings
def compare_strings(string1, string2):
    return string1.split(' ')[0] == string2

# Name of the input files (wildcard for user input)
input_file_name = 'extracted_commands_infosecinstitute.txt'      # Input-File = Extrahierten Commands
linux_commands_file_name = 'linux_commands.txt'                 # Linux-Command Collection for Comparison

# Percentage wildcard for matching strings
match_percentage = 10  # You can change this value

# Get the current directory
current_dir = os.getcwd()
print(f'Current directory: {current_dir}')

# Construct the input file path
input_file_path = os.path.join(current_dir, input_file_name)
print(f'Input file path: {input_file_path}')

# Construct the Linux commands file path
commands_file_path = os.path.join(current_dir, linux_commands_file_name)
print(f'Linux commands file path: {commands_file_path}')

# Read the input file
with open(input_file_path, 'r') as input_file:
    input_lines = input_file.readlines()

# Read the Linux commands file
with open(commands_file_path, 'r') as commands_file:
    commands_lines = commands_file.readlines()

# Initialize the cleaned lines list
cleaned_lines = []

# Loop through each line of the input file
for line in input_lines:
    # Strip the line of leading/trailing whitespaces
    line = line.strip()
    
    # Skip lines starting with 'Challenge Name' and 'Challenge URL'
    if line.startswith('Challenge Name') or line.startswith('Challenge URL') or line == '':
        continue
    
    # Flag to check if any match is found
    match_found = False
    
    # Loop through each line of the commands file
    for command in commands_lines:
        # Strip the command of leading/trailing whitespaces
        command = command.strip()
        
        # Compare the string preceding the first space of the current line and command
        if compare_strings(line, command):
            match_found = True
            break
    
    # If a match is found, add the line to the cleaned lines
    if match_found:
        cleaned_lines.append(line)

# Generate the output cleaned file name
cleaned_file_name = input_file_name.rsplit('.', 1)[0] + '_cleaned.txt'

# Construct the cleaned file path
cleaned_file_path = os.path.join(current_dir, cleaned_file_name)

# Write the cleaned lines to the output file
with open(cleaned_file_path, 'w') as cleaned_file:
    # Write the total number of challenges at the beginning of the file
    cleaned_file.write(f'Total number of challenges: {len(cleaned_lines)}\n\n')
    cleaned_file.write('\n'.join(cleaned_lines))

print(f'Cleaned file "{cleaned_file_name}" has been generated.')
