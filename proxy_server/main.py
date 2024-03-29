"""
Ref:
- https://github.com/anapeksha/python-proxy-server/blob/main/src/server.py
- https://github.com/inaz2/proxy2
- 
"""

import argparse
import logging
import socket
import sys
from _thread import *

LOG_FORMAT = "%(asctime)s: %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

parser = argparse.ArgumentParser()
parser.add_argument('--listening_port', help="Maximum allowed connections", default=8080, type=int)
parser.add_argument('--max_conn', help="Maximum allowed connections", default=5, type=int)
parser.add_argument('--buffer_size', help="Number of samples to be used", default=8192, type=int)

args = parser.parse_args()
listening_port = args.listening_port
max_connection = args.max_conn
buffer_size = args.buffer_size


def start():
    """
    Main program
    :return:
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listening_port))
        sock.listen(max_connection)
        logging.info("[*] Server started successfully [ %d ]" % listening_port)
    except Exception as e:
        logging.error("[*] Unable to Initialize Socket")
        logging.error(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = sock.accept()  # Accept connection from client browser
            data = conn.recv(buffer_size)  # Receive client data
            start_new_thread(conn_string, (conn, data, addr))  # Starting a thread
        except KeyboardInterrupt:
            sock.close()
            logging.error("\n[*] Graceful Shutdown")
            sys.exit(1)


def conn_string(conn, data, addr):
    try:
        # Retrieve Web server and port to reach
        webserver, port = get_webserver(data)

        proxy_server(webserver, port, conn, addr, data)
    except Exception:
        pass

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


def proxy_server(webserver, port, conn, addr, data):
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        sock.send(data)

        while 1:
            reply = sock.recv(buffer_size)
            if (len(reply) > 0):
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                logging.debug("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
            else:
                break

        sock.close()
        conn.close()
    except socket.error :
        sock.close()
        conn.close()
        logging.error(sock.error)
        sys.exit(1)


if __name__ == "__main__":
    start()
