"""Generate an encryption key and store it in config"""
import json
from cryptography.fernet import Fernet


CONFIG_FILE = "config.json"

with open(CONFIG_FILE, 'r') as infile:
    config_data = json.load(infile)

key = Fernet.generate_key()
config_data['encryption']['key'] = str(key)[2:-1]

with open(CONFIG_FILE, "w") as outfile:
    json.dump(config_data, outfile, indent=4)
