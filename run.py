from app import app, socket_IO


if __name__ == "__main__":
    socket_IO.run(app)  # , host="192.168.0.113")
