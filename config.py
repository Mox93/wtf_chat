# Config
import json

err_msg = """==================================================
Please create a "config.json" file in the project's root directory with the following fields:
    - host : <str: i.e. "0.0.0.0">
    - port : <int: i.e. 5000>
    - secret : <str: i.e. "a random value" >
    - namespace : <str: i.e. "/dev">
Once you've done that press Enter to continue."""

while True:
    try:
        with open("config.json", "r") as config:
            config = json.load(config)
        HOST = config["host"]
        SECRET = config["secret"]
        PORT = config["port"]
        NAMESPACE = config["namespace"]
        break

    except (FileNotFoundError, KeyError):
        input(err_msg)
