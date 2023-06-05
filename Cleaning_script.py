import difflib
import subprocess

# Replace 'input_file.txt' with the actual file name
input_file = 'input_file.txt'

# Create a new file name with '_cleaned' appended
output_file = input_file.replace('.txt', '_cleaned.txt')

# Execute compgen -c command to get the Linux commands
command_output = subprocess.check_output(['compgen', '-c'])
linux_commands = command_output.decode().splitlines()

# Define the similarity threshold for fuzzy matching
similarity_threshold = 0.5

# Define keywords for exceptions
exceptions = ['Challenge Name', 'Challenge URL']

# Flag to indicate if the lines should be deleted
delete_line = False

# Counter for challenges
total_challenges_pre_cleaning = 0
total_challenges_after_cleaning = 0

# List to store extracted lines
extracted_lines = []

# Function to check similarity using fuzzy matching
def check_similarity(line, command):
    return difflib.SequenceMatcher(None, line[:5], command[:5]).ratio()

# Open the input and output files
with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
    # Loop through each line in the input file
    for line in file_in:
        # Check if the line starts with an exception keyword
        if line.startswith('Challenge Name'):
            file_out.write(line.replace('Total Challenges', 'Total Challenges pre cleaning'))
            total_challenges_pre_cleaning = int(line.split()[-1])
            continue
        elif line.startswith('Challenge URL'):
            file_out.write(line)
            continue
        
        # Check if the line contains a command based on similarity with the Linux commands
        if any(check_similarity(line, command) >= similarity_threshold for command in linux_commands):
            # Write the line to the output file
            file_out.write(line)
            extracted_lines.append(line)
            total_challenges_after_cleaning += 1
        else:
            # Set the flag to delete the line
            delete_line = True
        
        # Check if the line contains the end of a command sequence
        if line.strip() == 'cat r00t.txt':
            # Reset the flag after the end of a command sequence
            delete_line = False
        
        # Delete the line if the flag is set
        if delete_line:
            continue
        
        # Print the line to the console
        print(line.strip())

# Open the cleaned file and append extracted lines
with open(output_file, 'a') as file_out:
    file_out.write('\n\nTotal Challenges after cleaning: ' + str(total_challenges_after_cleaning) + '\n\n')
    file_out.write('Extracted Lines:\n')
    for extracted_line in extracted_lines:
        file_out.write(extracted_line)
    file_out.write('\n\n')

print("Script execution completed successfully!")