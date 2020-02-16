from app import app, socket_IO, HOST


if __name__ == "__main__":
    socket_IO.run(app, host=HOST)
