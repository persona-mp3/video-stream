import struct
import socket


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


TestDecoding()
