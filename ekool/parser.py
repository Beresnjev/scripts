import re
import os


def parse_text_file(file_path):
    # Dictionary to store the mappings of code to name
    code_name_mapping = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Regular expression pattern to match the code pattern
        code_pattern = re.compile(r' {4}s(\d+)\.id = (.+);')

        for line in lines:
            # Try to match the line against the code pattern
            code_match = code_pattern.match(line)
            if code_match:
                id_number = code_match.group(1)
                code = code_match.group(2).strip()

                # Generate the name pattern using the extracted ID
                name_pattern = re.compile(r'    s{}\.name = (.+);'.format(id_number))

                # Search for the corresponding name pattern using the dynamically generated pattern
                for name_line in lines:
                    name_match = name_pattern.match(name_line)
                    if name_match:
                        name = name_match.group(1).strip()
                        # Add to the dictionary
                        code_name_mapping[code] = name
                        break

    return code_name_mapping


# Example usage:
# file_path = "test"
# mapping = parse_text_file(file_path)
# print(mapping)
