"""Generate an encrypted password using the config key"""
import json
import getpass
from cryptography.fernet import Fernet


CONFIG_FILE = "config.json"

with open(CONFIG_FILE, 'r') as infile:
    config_data = json.load(infile)

key = config_data['encryption']['key'].encode("utf-8")
fernet = Fernet(key)

user_input = getpass.getpass("Input Unencrypted Password (Hidden)")

password = user_input.encode()
encrypted_password = fernet.encrypt(password)
print(str(encrypted_password)[2:-1])