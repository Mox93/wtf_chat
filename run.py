from app import app, socket_IO, config
import json


if __name__ == "__main__":
    socket_IO.run(app, host=config["host"])
