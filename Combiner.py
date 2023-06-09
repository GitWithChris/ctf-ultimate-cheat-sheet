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
    output.write('\n' * 10)  # Add 10 lines of space between input files

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
    file.write(f'Summary:\n')
    file.write(f'Number of entries from {input_file1_name}: {num_entries_file1_remaining}\n')
    file.write(f'Number of entries from {input_file2_name}: {num_entries_file2_remaining}\n')

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


# Additional tasks

# Go through the generated text file until 'Summarization of all Commands used:' is reached
with open(output_file, 'r') as file:
    lines = file.readlines()

start_index = 0
for i, line in enumerate(lines):
    if line.strip() == 'Summarization of all Commands used:':
        start_index = i + 1  # Skip the indicator line and start from the next line
        break

# Read the reference file
reference_file_name = 'linux_commands.txt'  # Update with the name of the reference text file
reference_file_path = os.path.join(os.path.dirname(__file__), reference_file_name)

with open(reference_file_path, 'r') as reference_file:
    reference_lines = reference_file.readlines()

reference_lines = [ref_line.strip() for ref_line in reference_lines]

matched_lines = []  # To store the matched lines

for i in range(start_index, len(lines)):
    current_line = lines[i].strip()
    if current_line != '':
        current_line_parts = current_line.split(' ', 1)
        if len(current_line_parts) > 1:
            command_name = current_line_parts[0]
            command_description = current_line_parts[1]

            matched_reference_lines = []
            for ref_line in reference_lines:
                if ref_line.startswith(command_name):
                    matched_reference_lines.append(ref_line)

            if matched_reference_lines:
                # Find the line from the reference file that matches the most with the current line
                best_match = max(matched_reference_lines, key=lambda x: len(set(x.split()).intersection(set(command_description.split()))))

                # Check if the matched line has already been added to the generated text file
                is_existing = False
                for j in range(start_index, i):
                    if lines[j].strip() == best_match:
                        is_existing = True
                        break

                if is_existing:
                    # Modify the existing line by adding the amount of appearances
                    count = 0
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() == best_match:
                            count += 1
                    if count > 1:
                        lines[i] = f"{best_match}: '{count}'\n"
                else:
                    # Add the matched line to the generated text file
                    matched_lines.append(best_match)
                    lines[i] = best_match + '\n'

# Write the modified lines back to the generated text file
with open(output_file, 'w') as file:
    file.writelines(lines)

# Append the matched lines to the output file
with open(output_file, 'a') as file:
    file.write('\n\nMatched Lines from Reference File:\n')
    for matched_line in matched_lines:
        file.write(matched_line + '\n')

# Console output for the matched lines
print('Matched lines from the reference file added to the output file.')
