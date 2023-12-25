# Author:   Evan Samano
# Date:     July 22nd, 2023
# Version:  1.0
# Desc:     A client to play the card game 'Auction' over a network.
#           yt-tutorial: https://www.youtube.com/watch?v=3QiPPX-KeSc


from socket import *
#from threading import Thread

# server setup stuff
HEADER = 4
FORMAT = 'utf-8'
DISCONN_MSG = '!DISCONNECT'
NAME_MSG = '!NAME '


def send(_msg):
    # note: the purpose of the header is to indicate how long the following msg will be
    msg = _msg.encode(FORMAT)
    msg_len = len(msg)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len) # msg header
    client.send(msg) # msg body
    print(client.recv(12).decode(FORMAT))

if __name__ == '__main__':
    print(f'[INFO] Local IP is {gethostbyname(gethostname())} \n       Default port should be 25000\n')
    IP = input('[IP]: ')
    PORT = int(input('[PORT]: '))
    name = input('[DISPLAY NAME]: ')[:16] # limit length to 16 characters
    print(f'[SETUP] Connecting to {IP}:{PORT}')
    
    ADDR = (IP, PORT)
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDR)

    # send display name first:
    send(NAME_MSG + name)

    while connected := True:
        msg = input('[ENTER MSG]: ')
        if msg == DISCONN_MSG:
            send(msg)
            break
        send(msg)