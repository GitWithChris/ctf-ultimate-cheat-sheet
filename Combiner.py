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

# Console output to indicate compilation is done
print("Compilation is done. The combined contents have been written to", output_file)
