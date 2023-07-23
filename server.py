# Author:   Evan Samano
# Date:     July 22nd, 2023
# Version:  1.0
# Desc:     A server to host the card game 'Auction' over a network.
# yt-tutorial: https://www.youtube.com/watch?v=3QiPPX-KeSc


from auction import play
from socket import *
from threading import Thread, active_count

HEADER = 4
PORT = 25000
IP = gethostbyname(gethostname())
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONN_MSG = '!DISCONNECT'

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(ADDR)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        if msg_len := conn.recv(HEADER).decode(FORMAT): # if we receive a msg
            msg_len = int(msg_len) # then store the header (first msg) as the length of the next msg
            msg = conn.recv(msg_len).decode(FORMAT) # then listen for the body (second msg) since we know its length
            if msg == DISCONN_MSG:
                connected = False
            
            print(f'[{addr}] {msg}')
            conn.send('MSG received'.encode(FORMAT))
    
    conn.close()


def start():
    sock.listen()
    print(f'Server is listening on {IP}:{PORT}')
    while True:
        conn, addr = sock.accept()
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {active_count() - 1}')


if __name__ == '__main__':
    print('[STARTING] Server is starting now...')
    start()


# establish socket opening on port
# wait for connections
# wait for input
#   utilize the round robin task scheduler demonstrated in the Dave talk from Pycon 2015?