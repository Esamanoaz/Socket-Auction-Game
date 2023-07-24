# Author:   Evan Samano
# Date:     July 22nd, 2023
# Version:  1.0
# Desc:     A server to host the card game 'Auction' over a network.
#           yt-tutorial: https://www.youtube.com/watch?v=3QiPPX-KeSc

# this server needs to:
#   startup and receive client connections
#   first client to connect is Party Leader
#   Party Leader can !START the game
#   After !START is called, check if there are more than 1 and less than 5 clients
#   Pass usernames in and create Player objects to start game using auction.play

from auction import play, Player
from socket import *
from threading import Thread, active_count, Lock

HEADER = 4
PORT = 25000
IP = gethostbyname(gethostname())
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONN_MSG = '!DISCONNECT'
LOCK = Lock()

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(ADDR)


def safe_print(*a, **b):
    '''Thread safe print function
    https://bramcohen.livejournal.com/70686.html'''
    with LOCK:
        print(*a, **b)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        if msg_len := conn.recv(HEADER).decode(FORMAT): # if we receive a msg
            msg_len = int(msg_len) # then store the header (first msg) as the length of the next msg
            msg = conn.recv(msg_len).decode(FORMAT) # then listen for the body (second msg) since we know its length
            if msg == DISCONN_MSG:
                connected = False
            
            safe_print(f'[{addr}] {msg}')
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
    IP = gethostbyname(gethostname())
    setup = input('[SETUP] Set port to 25000? (y/n): ')
    if setup.lower() == 'n':
        PORT = int(input('[PORT]: '))
    else:
        PORT = 25000
        print(f'[SETUP] Set up by default to {IP}:{PORT}')
    ADDR = (IP, PORT)

    print('[STARTING] Server is starting now...')
    start()


# establish socket opening on port
# wait for connections
# wait for input
#   utilize the round robin task scheduler demonstrated in the Dave talk from Pycon 2015?