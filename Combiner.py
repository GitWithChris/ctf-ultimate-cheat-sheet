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
    for line in file1:
        output.write(line)

    output.write('\n')
    output.write('\n' * 10)  # Add 10 lines of space between input files

    # Write the name of the second input file
    output.write('=== ' + input_file2_name + ' ===\n\n')

    # Copy the contents of the second input file
    for line in file2:
        output.write(line)

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

# Console output to indicate compilation and validation are done
print("Compilation and validation are done. The combined and validated contents have been written to", output_file)
