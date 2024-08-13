from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    # Get the absolute path of the configuration file
    base_path = os.path.dirname(__file__)
    abs_path = os.path.join(base_path, filename)
    print(f"Looking for file at: {abs_path}")
    
    parser = ConfigParser()
    if not os.path.exists(abs_path):
        raise Exception(f"File not found: {abs_path}")

    # Read the file and print its contents for debugging
    with open(abs_path, 'r') as file:
        contents = file.read()
        print("File contents:")
        print(contents)

    parser.read(abs_path)

    # Debug print to see what sections are found
    print(f"Sections found: {parser.sections()}")

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {abs_path} file")

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)
