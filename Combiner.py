import os

# Define input file names
input_file1_name = 'extracted_commands_infosecinstitute_cleaned.txt'  # Update with the name of the first input file
input_file2_name = 'extracted_commands_hackingarticles_cleaned.txt'  # Update with the name of the second input file

# Get the absolute paths of the input and output files
input_file1 = os.path.join(os.path.dirname(__file__), input_file1_name)
input_file2 = os.path.join(os.path.dirname(__file__), input_file2_name)
output_file = os.path.join(os.path.dirname(__file__), 'Collection_Extracted_Commands.txt')

# Combine the contents of the input files into the output file
with open(input_file1, 'r') as file1, open(input_file2, 'r') as file2, open(output_file, 'w') as output:
    # Write the name of the first input file
    output.write('=== ' + input_file1_name + ' ===\n\n')

    # Copy the contents of the first input file
    num_entries_file1 = 0
    for line in file1:
        output.write(line)
        if line.startswith('Challenge Name'):
            num_entries_file1 += 1

    output.write('\n')
    output.write('\n' * 5)  # Add 10 lines of space between input files

    # Write the name of the second input file
    output.write('=== ' + input_file2_name + ' ===\n\n')

    # Copy the contents of the second input file
    num_entries_file2 = 0
    for line in file2:
        output.write(line)
        if line.startswith('Challenge Name'):
            num_entries_file2 += 1

    output.write('\n')

# Check the generated file for faulty entries and remove them
with open(output_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('Challenge Name'):
            # Check if it is a faulty entry
            if (
                i + 5 < len(lines) and
                lines[i+1].startswith('Challenge URL') and
                lines[i+2] == '\n' and
                lines[i+3] == '\n' and
                lines[i+4] == '\n' and
                lines[i+5].strip() == ''
            ):
                # Skip over the faulty entry (delete Challenge Name and Challenge URL)
                i += 6
            else:
                file.write(line)
                i += 1
        else:
            file.write(line)
            i += 1

# Count the remaining entries for each input file after the removal of faulty entries
num_entries_file1_remaining = 0
num_entries_file2_remaining = 0

with open(output_file, 'r') as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('=== ' + input_file1_name):
        i += 2
        while i < len(lines) and not lines[i].startswith('==='):
            if lines[i].startswith('Challenge Name'):
                num_entries_file1_remaining += 1
            i += 1
    elif line.startswith('=== ' + input_file2_name):
        i += 2
        while i < len(lines) and not lines[i].startswith('==='):
            if lines[i].startswith('Challenge Name'):
                num_entries_file2_remaining += 1
            i += 1
    else:
        i += 1

# Append the counts of remaining entries to the output file
with open(output_file, 'a') as file:
    file.write('\n')
    file.write(f'Summary of Website Content:\n')
    file.write(f'Number of entries from {input_file1_name}: {num_entries_file1_remaining}\n')
    file.write(f'Number of entries from {input_file2_name}: {num_entries_file2_remaining}\n')
    file.write('\n')

# Console output to indicate compilation and validation are done
print("Compilation and validation are done. The combined and validated contents have been written to", output_file)
print("Complete Command List generated.")

# Collect commands from the generated file
commands = []
with open(output_file, 'r') as file:
    for line in file:
        line = line.strip()
        if not line.startswith(('===', 'Challenge Name', 'Challenge URL', 'Summary', 'Number of')) and line != '':
            commands.append(line)

# Append the commands summarization to the output file
with open(output_file, 'a') as file:
    file.write('\n\nSummarization of all Commands used:\n')
    for command in commands:
        file.write(command + '\n')

# Console output for the commands summarization
print('Commands Summarization done')


# Unique Commands Cleaning

# Read the content of the original file after 'Summarization of all Commands used:' and store it in a list
original_commands = []
with open(output_file, 'r') as file:
    lines = file.readlines()

start_index = 0
for i, line in enumerate(lines):
    if line.strip() == 'Summarization of all Commands used:':
        start_index = i + 1  # Skip the indicator line and start from the next line
        break

original_commands = [line.strip() for line in lines[start_index:] if line.strip() != '']

# Read the content of the reference file and store it in a list
reference_file_name = 'linux_commands.txt'  # Update with the name of the reference text file
reference_file_path = os.path.join(os.path.dirname(__file__), reference_file_name)

reference_commands = []
with open(reference_file_path, 'r') as reference_file:
    reference_commands = [line.strip() for line in reference_file.readlines() if line.strip() != '']

# Create a list to store the extracted raw commands
extracted_commands = []

# Iterate through each entry in the original file's list
for entry in original_commands:
    # Split the entry into individual words using whitespace as the delimiter
    words = entry.split()

    # Check if the first word (command) exists in the reference file's list
    command = words[0]
    if command in reference_commands:
        # Add the matching raw line of the reference file to the list of extracted raw commands
        extracted_commands.append(reference_commands[reference_commands.index(command)])

# Append the extracted raw commands to the original file
with open(output_file, 'a') as file:
    file.write('\n\nComplete List of Cleaned Commands:\n')
    for extracted_command in extracted_commands:
        file.write(extracted_command + '\n')

# Console output for the matched commands
print('Complete cleaned list of all commands added to the output file.')

# Additional task: Frequency of unique commands
command_counts = {}
for command in extracted_commands:
    if command in command_counts:
        command_counts[command] += 1
    else:
        command_counts[command] = 1

# Append the command frequencies to the original file
with open(output_file,'a') as file:
    file.write('\n\nFrequency of unique commands:\n')
    for command, count in command_counts.items():
        file.write(f'{command}: {count}\n')

# Count the total number of unique commands
total_unique_commands = len(command_counts)

# Append the total count to the original file
with open(output_file, 'a') as file:
    file.write(f'Total amount of unique commands: {total_unique_commands}')

print('Frequency of unique commands added to the output file.')

# Search for the line that starts with 'Frequency of unique commands:' in the output file
with open(output_file, 'r') as file:
    lines = file.readlines()

start_index = None
for i, line in enumerate(lines):
    if line.startswith('Frequency of unique commands:'):
        start_index = i + 1
        break

# Store the string prior to ':' of each line in a list until reaching the line starting with 'Total amount'
entry_list = []
for line in lines[start_index:]:
    if line.startswith('Total amount'):
        break
    entry = line.split(':')[0].strip()
    entry_list.append(entry)

# Process each entry in the list
for entry in entry_list:
    counter = 0
    found_entry = False
    i = 0

    # Find matching lines in the file and increment the counter
    while i < len(lines):
        line = lines[i]
        if line.startswith('Challenge Name'):
            found_entry = False
        elif not found_entry and line.strip() != '':
            line_split = line.split()
            if len(line_split) > 0 and line_split[0] == entry:
                counter += 1
                found_entry = True
        i += 1

    # Append the counter and entry to the bottom of the generated text file
    with open(output_file, 'a') as file:
        file.write(f'{entry}: {counter}\n')

print('Count of commands added to the output file.')
