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


def file_handler(fname, flag):
    try:
        file = open(fname, flag)
        print("file operation successful")
        return file
    except (IOError, FileNotFoundError) as e:
        return e


def Packet(data):
    data_to_bytes = data.encode("utf-8")
    data_len = len(data_to_bytes)
    # this is converting the data_len to a 4 bytes uint
    # and ordering it in BigEndian
    header = struct.pack("!I", data_len)

    packet = header + data_to_bytes
    return packet


def StreamFile2():
    file = file_handler("./yogit.go", "r")
    if isinstance(file, Exception):
        print(f"An error occured in opening file\n{file}")
        return

    CHUNK_SIZE = 400
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("127.0.0.1", 8000)

    s.connect(address)

    count = 0
    while True:
        chunk = file.read(CHUNK_SIZE)
        if not chunk:
            print("no more bytes to stream")
            # file.close()
            print("closed file successfully")
            break

        packet = Packet(chunk)
        s.sendall(packet)
        count += 1
        print("current syncN -> ", count)


StreamFile2()
