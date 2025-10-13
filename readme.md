# UNO and Socket Programming

## Overview
This project is a prototype implementation of the UNO card game in Python, extended with socket programming to allow multiplayer play over a network. Players can connect through a client-server model and compete in real time by following the official UNO rules.

## Demo

Run server:
python server.py 0.0.0.0 9999 2

Run two clients:
python client.py 127.0.0.1 9999 Player1
python client.py 127.0.0.1 9999 Player2