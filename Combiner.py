import os

# Define input file names
input_file1_name = 'extracted_commands_infosecinstitute_cleaned.txt'  # Update with the name of the first input file
input_file2_name = 'extracted_commands_hackingarticles_cleaned.txt'  # Update with the name of the second input file

# Get the absolute paths of the input and output files
input_file1 = os.path.join(os.path.dirname(__file__), input_file1_name)
input_file2 = os.path.join(os.path.dirname(__file__), input_file2_name)
output_file = os.path.join(os.path.dirname(__file__), 'Collection_Extracted_Commands.txt')

# Check the generated file for faulty entries and remove them
with open(output_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:
    num_entries_file1_remaining = 0
    num_entries_file2_remaining = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('=== ' + input_file1_name):
            num_entries_file1_remaining += 1
            i += 2
            while i < len(lines) and not lines[i].startswith('==='):
                if lines[i].startswith('Challenge Name'):
                    num_entries_file1_remaining += 1
                i += 1
        elif line.startswith('=== ' + input_file2_name):
            num_entries_file2_remaining += 1
            i += 2
            while i < len(lines) and not lines[i].startswith('==='):
                if lines[i].startswith('Challenge Name'):
                    num_entries_file2_remaining += 1
                i += 1
        else:
            file.write(line)
            i += 1

    # Write the counts of remaining entries to the top of the generated text file
    file.write(f'Total amount of challenges extracted from {input_file1_name}: {num_entries_file1_remaining}\n')
    file.write(f'Total amount of challenges extracted from {input_file2_name}: {num_entries_file2_remaining}\n\n')

    # Copy the remaining contents of the file
    for line in lines:
        file.write(line)

# Console output to indicate compilation and validation are done
print("Compilation and validation are done. The combined and validated contents have been written to", output_file)
print("Total amount of challenges extracted from", input_file1_name, ":", num_entries_file1_remaining)
print("Total amount of challenges extracted from", input_file2_name, ":", num_entries_file2_remaining)
