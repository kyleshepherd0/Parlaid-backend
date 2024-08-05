import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    
    # Check if the file exists and print the absolute path
    abs_path = os.path.abspath(filename)
    print(f"Looking for file at: {abs_path}")
    if not os.path.exists(filename):
        raise Exception(f"File not found: {filename}")

    # Read the file and print its contents
    with open(filename, 'r') as file:
        contents = file.read()
        print("File contents:")
        print(contents)

    parser.read(filename)

    # Debug print to see what sections are found
    print(f"Sections found: {parser.sections()}")

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)  # Print the loaded configuration for debugging
