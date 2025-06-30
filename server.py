import socket
import select
import struct


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
                print(f"New Client => {client}|| Address => {addr}")
                decode_content(client)

                try:
                    client.close()
                    print("Client socket closed successfully")
                except OSError:
                    print("Client preclosed")


def read_content(client):
    print("reading from client...")
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


def get_content_len(client):
    content_len = b''
    while len(content_len) < HEADER_LEN:
        print("getting len", len(content_len))
        chunk = client.recv(HEADER_LEN - len(content_len))
        if not chunk:
            raise ConnectionError("Socket closed?? dafuq")
        content_len += chunk

    print("done getting the header, about to read length")
    return content_len


def decode_content(client):
    content_len = get_content_len(client)
    print("length of content == > ", content_len)
    # decoded_len = content_len.decode("utf-8")
    # decoded_len = int.to_bytes(content_len, HEADER_LEN, "big")
    decoded_len = struct.unpack(">I", content_len)[0]
    print("decoded length ===> ", decoded_len)

    buffer = b''

    while len(buffer) < decoded_len:
        content = client.recv(decoded_len - len(buffer))
        # content += buffer
        buffer += content

    print("Done reading content, message from client is ->\n", str(buffer))


create_server(8000)
