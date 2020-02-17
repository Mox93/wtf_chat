from app import app, socket_IO
from config import HOST


if __name__ == "__main__":
    socket_IO.run(app, host=HOST)
