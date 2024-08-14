import os
from dotenv import load_dotenv

def load_config():
    # Load environment variables from the .env.local file
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env.local')
    load_dotenv(dotenv_path=dotenv_path)
    
    # Create a configuration dictionary from the environment variables
    config = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }

    # Check if any of the config values are None (meaning they weren't found in the .env.local)
    if None in config.values():
        raise Exception("One or more environment variables are missing.")
    
    return config

if __name__ == '__main__':
    config = load_config()
    print(config)
