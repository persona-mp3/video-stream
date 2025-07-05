import socket
import select
import struct
import typing


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
                print(f"\nNew Client => {client}|| Address => {addr}\n")
                # is_eof = client.recv(HEADER_LEN)
                while True:  # if is_eof != b'':
                    content_len = get_content_len(client)
                    if content_len != b'': 
                        decode_content(client, content_len)
                    else:
                        print("No more content to read from clinet")
                        break

                # try:
                #     client.close()
                #     print("Client socket closed successfully")
                # except OSError:
                #     print("Client preclosed")


def read_content(client):
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
    content_len = b''  # bytes 
    while len(content_len) < HEADER_LEN:  # int
        chunk = client.recv(HEADER_LEN - len(content_len))
        if not chunk:
            raise ConnectionError("Socket closed?? wtf")
        content_len += chunk

    print(f" {type(HEADER_LEN)}o====o{type(content_len)} {
          content_len == HEADER_LEN}\n {content_len}o===o{HEADER_LEN} ")
    return content_len


def decode_content(client: socket, content_len: bytes):
    # content_len = get_content_len(client)
    print(f"length of content bytes ==> {content_len} \n", )
    decoded_len = struct.unpack(">I", content_len)[0]
    print(f"decoded length ===> {decoded_len}\n")

    buffer = b''
    count = 0

    while len(buffer) < decoded_len:
        content = client.recv(decoded_len - len(buffer))
        # content += buffer
        buffer += content
        count += 1
        print("server sync n -> ", count)

    # print("Done reading content, message from client is ->\n", str(buffer))
    print("client message\n")
    print(buffer.decode("utf-8"))

    # so if we have 3 packets its something like this 
    # packet, packet, packet
    # {400, blob} { 321, blob }, { 21, blob }
    # total-len => 4*3 + ( 400 + 321 + 21 ) = 8904 bytes 
    # so when we read the first packet, we know we have 
    # remains = -packet_size + total_len ===== 8904 - (4bytes + 400 ) = 8500
    # and then we could just update our curr_len to remains
    # total_len = remains
    # but we can't tel how many packets we have unless we start using ACK numbers 
    # but since we are streaming i dont think those matter, so the best thing is to 
    # always check if there are more bytes to read
    # but we also need to know where we stopped out last read... 
    # and we def not want recursion on out servers

    # =============================================================================
    #           if client.recv(HEADER_LEN) != b'':
    #               decode_content(client)
    # =============================================================================


def check_content(client):
    # so we need to also read from the client again, kinda like to make it 
    # recursice, you feel me>>??
    # so if theres still more content to read, we call decode content again?YYESS
    # but we also need to know when to stop, we could just use a clever as while loop 
    pass


def recv_content(client: socket, after: bytes, before: bytes, current: bytes):
    """
    ===============================================================================
        current = 0 
        before = 0 

        header_len  = b''
        while len(header_len) < HEADER_LEN:
            data = client.recv(HEADER_LEN - len(header_len))
            if data == b'':
                print("end of socket reached")
                break

            header_len += data

            if header_len == HEADER_LEN:
                print("we can give this to the next function for processing...")
                return header_len


    i mean we can have a function that just reads content from the socket, and another one
    that tells it where to read

    read_from(client, x,)
    ===============================================================================

    """
    pass


create_server(8000)
