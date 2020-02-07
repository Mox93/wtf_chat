from flask_socketio import emit
from app import socket_IO

@socket_IO.on("say hi")
def message(msg):
    print(msg)
    return msg
