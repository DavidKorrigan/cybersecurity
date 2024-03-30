"""
Ref:
- https://github.com/anapeksha/python-proxy-server/blob/main/src/server.py
- https://github.com/inaz2/proxy2

Test:
- curl --proxy https://proxy.home.md:8443 https://webhook.site/5092a2e9-db1e-4f5b-bd77-e9db989938dd
- curl --proxy https://proxy.home.md:8443 http://webhook.site/5092a2e9-db1e-4f5b-bd77-e9db989938dd
- curl --proxy http://proxy.home.md:8443 https://webhook.site/5092a2e9-db1e-4f5b-bd77-e9db989938dd
- curl --proxy http://proxy.home.md:8443 http://webhook.site/5092a2e9-db1e-4f5b-bd77-e9db989938dd
"""

import argparse
import logging
import socket
import ssl
import sys
from _thread import *

LOG_FORMAT = "%(asctime)s: %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

parser = argparse.ArgumentParser()
parser.add_argument('--protocol', help="Proxy protocol", default="https", choices=['http', 'https'])
parser.add_argument('--listening_port', help="Listening Port", default=8443, type=int)
parser.add_argument('--listening_interface', help="Listening interface", default="proxy.home.md", type=str)
parser.add_argument('--max_conn', help="Maximum allowed connections", default=5, type=int)
parser.add_argument('--buffer_size', help="Number of samples to be used", default=8192, type=int)

args = parser.parse_args()
protocol = args.protocol
listening_port = args.listening_port
listening_interface = args.listening_interface
max_connection = args.max_conn
buffer_size = args.buffer_size


def start():
    """
    Main program
    :return:
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((listening_interface, listening_port))
        sock.listen(max_connection)

        if protocol == "https":
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain('conf/certchain.pem', 'conf/private.key')
            ssock = context.wrap_socket(sock, server_side=True)

        logging.info("[*] Server started successfully [ %s://%s:%d ]" % (protocol, listening_interface, listening_port))
    except Exception as e:
        logging.error("[*] Unable to Initialize Socket")
        logging.error(e)
        sys.exit(2)

    while True:
        try:
            if protocol == "https":
                conn, addr = ssock.accept()  # Accept connection from TLS client
            else:
                conn, addr = sock.accept()  # Accept connection from client
            data = conn.recv(buffer_size)  # Receive client data
            start_new_thread(handle_client_request, (conn, data, addr))  # Starting a thread
        except KeyboardInterrupt:
            sock.close()
            logging.error("\n[*] Graceful Shutdown")
            sys.exit(1)


def handle_client_request(conn, data, addr):
    """
    Handle client requests
    """
    try:
        logging.debug("Received data from client %s:%d" % addr)
        # Retrieve Web server and port to reach
        webserver, port = get_webserver(data)

        if b'CONNECT' in data:
            https_forward_data(webserver, port, conn)
        else:
            http_forward_data(webserver, port, conn, addr, data)
    except Exception as e:
        logging.error("Error handling client request: %s" % e)
        conn.close()


def https_forward_data(webserver, port, conn):
    """
    Forward data between client and destination server
    """

    # Establish connection to destination server
    dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_sock.connect((webserver, port))
    conn.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")

    while True:
        data = conn.recv(buffer_size)
        if not data:
            break
        dest_sock.sendall(data)

        data = dest_sock.recv(buffer_size)
        if not data:
            break
        conn.sendall(data)

    conn.close()
    dest_sock.close()


def get_webserver(data):
    """
    Extract web server and port from received data on the socket
    :param data: byte
    :return: string and integer
    """
    logging.debug(data.decode())

    # 1- Get the first line
    first_line = data.split(b'\n')[0]
    logging.debug("First line: %s", first_line.decode())

    # 2- Get the URL
    url = first_line.split()[1]
    logging.info("URL: %s", url.decode())

    # 3- Finding the position of :// to remove http or https
    http_pos = url.find(b'://')
    if (http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]

    # 4- Find the port position
    port_pos = temp.find(b':')

    # 5- Remove endpoint
    webserver_pos = temp.find(b'/')
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1
    if (port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = temp[:port_pos]

    logging.debug("Web server: %s", webserver.decode())
    logging.debug("Port: %i", port)

    return webserver, port


def http_forward_data(webserver, port, conn, addr, data):
    """
    Send data to the target
    :param webserver: Destination host
    :param port: Destination port
    :param conn: Socket
    :param addr: Address of the client
    :param data: Data to carry
    """
    try:
        logging.debug("Proxy Server data: %s", data.decode())
        dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest_sock.connect((webserver, port))
        dest_sock.send(data)

        while True:
            reply = dest_sock.recv(buffer_size)
            if not data:
                break
            conn.send(reply)

            dar = float(len(reply))
            dar = float(dar / 1024)
            dar = "%.3s" % (str(dar))
            dar = "%s KB" % (dar)
            logging.debug("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))

        dest_sock.close()
        conn.close()

    except socket.error:
        dest_sock.close()
        conn.close()
        logging.error(dest_sock.error)
        sys.exit(1)


if __name__ == "__main__":
    start()
