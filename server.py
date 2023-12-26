# Author:   Evan Samano
# Date:     December 26th, 2023
# Version:  0.2
# Desc:     A server to host the card game 'Auction' over a network.
#           yt-tutorial: https://www.youtube.com/watch?v=3QiPPX-KeSc

# this server needs to:
#   startup and receive client connections
#   first client to connect is Party Leader
#   Party Leader can !START the game
#   After !START is called, check if there are more than 1 and less than 5 clients
#   Pass usernames in and create Player objects to start game using auction.play

from auction import play, Player
import asyncio