import json
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load settings from JSON file
def load_settings():
    # Get the directory path of the current script (main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    logging.info("Dir Path for settings file: " + current_dir)
    
    # Path to the settings file
    settings_file = os.path.join(current_dir, 'Settings.json')
    logging.info("settings file: " + settings_file)
    with open(settings_file, 'r') as f:
        settings = json.load(f)
        logging.info("settings loaded")
    return settings

def load_mystring():
    mystr = ""
    # Get the directory path of the current script (main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
     # Path to the settings file
    settings_file = os.path.join(current_dir, 'stringdata.json')
    with open(settings_file, 'r') as f:
      mystr = json.load(f)
    return mystr