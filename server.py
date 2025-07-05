import socket
import select
import struct
import typing

"""
So we want to read the content from the client according
to the byte length. With the way this project might evolve we just might
make own custom protocol, just for the fun of it. We are currently using
bytes as the main language for this protocol, so a lot of string and byte
manipulation will be heavily involved. This is what the basic structure of
the protocol will look like
==========================================================================
                    Content-Length <N> \r\n
                    Content: //
==========================================================================
The`Content-Length` will have a defined size of 4 bytes, just incase things
could start getting funny, so we know a content of over 4 bytes is CRAZY
==========================================================================
So we can slice the content gotten from stream packets like this:
==========================================================================
                    packet[:contentLen]
                    decode bytes -> jpeg -> video
==========================================================================
We can make sure they communciate over STDIO, but I think tcp already does
that, or we could just use netcat to connect to the server as a client
"""

# number of bytes to read from content to retrieve content-length
HEADER_LEN = 4


def create_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    address = ("127.0.0.1", port)
    s.bind(address)
    s.listen(1)

    while True:
        connected_sockets, _, _ = select.select([s], [], [], 0)
        if connected_sockets:
            for clients in connected_sockets:
                client, addr = clients.accept()
                # print(f"\nNew Client => {client}|| Address => {addr}\n")
                while True:  
                    content_len = get_content_len(client)
                    if content_len == b'':
                        print(":CLOSING CONNECTION")
                        client.close()
                        print(":CONNECTION CLOSED")
                        break
                    else:
                        decode_content(client, content_len)


def get_content_len(client):
    content_len = b''  
    while len(content_len) < HEADER_LEN:  
        chunk = client.recv(HEADER_LEN - len(content_len))
        if not chunk:
            # print("\nDONE READING FROM CLIENT CLOSING CONNNECTION...\n")
            break
        content_len += chunk

    return content_len


def decode_content(client: socket, content_len: bytes):
    # content_len = get_content_len(client)
    # print(f"length of content bytes ==> {content_len} \n", )
    decoded_len = struct.unpack(">I", content_len)[0]
    # print(f":DECODED LENGTH: {decoded_len}\n")

    buffer = b''
    count = 0

    while len(buffer) < decoded_len:
        content = client.recv(decoded_len - len(buffer))
        # content += buffer
        buffer += content
        count += 1
        # print("server sync n -> ", count)

    # print("Done reading content, message from client is ->\n", str(buffer))
    # print(":CLIENT MESSAGE\n")
    print(buffer.decode("utf-8"))


create_server(8000)
