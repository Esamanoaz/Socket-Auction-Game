# Author:   Evan Samano
# Date:     July 22nd, 2023
# Version:  1.0
# Desc:     A client to play the card game 'Auction' over a network.
# yt-tutorial: https://www.youtube.com/watch?v=3QiPPX-KeSc


from auction import play
from socket import *
from threading import Thread, activeCount

HEADER = 4
PORT = 25000
IP = gethostbyname(gethostname())
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONN_MSG = '!DISCONNECT'

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

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
    send("hello howdy pal you the best!!!! :D")
    send(input('[ENTER MSG]: '))
    send(DISCONN_MSG)