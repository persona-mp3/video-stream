import struct
import socket
from pathlib import Path


def TestDecoding():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("127.0.0.1", 8000)

    s.connect(address)

    msg = "Welcome to NewYork in 1970"
    msg_bytes = msg.encode("utf-8")
    print(msg_bytes)

    msg_len = len(msg_bytes)
    content_len = struct.pack("!I", msg_len)
    packet = content_len + msg_bytes

    s.sendall(packet)


def StreamFile():
    try:
        file_handler = open("./yogit.go", "r")
        print(file_handler.read(225))
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"An exception error occured:\n {e}")
    finally:
        file_handler.close()


# StreamFile()


def StreamFile2():
    p = Path("yogit.go")
    print(dir(p))
    x = dir(p)
    for i, b in enumerate(x, 0):
        print(f"{i} : {b}")


StreamFile2()
