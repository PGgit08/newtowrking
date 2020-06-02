"""
PML(python multi-player library)
v 3.293.111
Coded in python with socket
Please make sure you are connected to the internet while using this library

(c)copyright GUTKOVICH 2020

Developer Information:
Made By Peter Gutkovich
Phone:347-623-8734
Email: peter.mty8@gmail.com

-------------------------------
Please Do Not Copy Or Reproduce
"""

from socket import socket, AF_INET, SOCK_STREAM, error, gethostbyname, gethostname
from json import dumps, loads


class Client:
    def __init__(self, host_ip, host_port, id):
        self.host_ip = host_ip
        self.host_port = host_port
        self.connection = False
        self.player = id

        try:
            c = socket(AF_INET, SOCK_STREAM)
            c.connect((self.host_ip, self.host_port))
            c.send(self.player.encode())
            self.connection = True
            self.socket = c
            _from_server = self.socket.recv(1024).decode()
            print("FROM SERVER: " + _from_server)
            if _from_server == "YOU MAY NOT JOIN THE PLAYER LIMIT ON THE SERVER REACHED THE MAXIMUM":
                exit()

        except error():
            print("YOUR COMPUTER IS HAVING CONNECTIVITY ISSUES :: error code 10923")
            exit()

    def send(self, function, data):
        send_data = {'data': data, 'function': function, 'player': self.player}
        send_data = dumps(send_data)
        self.socket.send(send_data.encode())

    def receive(self, buff):
        try:
            response = self.socket.recv(buff)
            return response

        except error():
            print("CANT RECEIVE DATA FROM SERVER :: error code 03312")
            exit()

    def send_new_command(self, command_name, data_being_sent):
        request_data = data_being_sent
        try:
            self.send(function=command_name, data=request_data)

        except error():
            print("ERROR SENDING DATA :: error code 78329")
            exit()

    def kill_connection(self):
        self.socket.close()


class Server:
    def __init__(self, port, player_amount):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.bind((gethostbyname(gethostname()), port))
            self.socket = s
            self.players_addr = []
            self.players = []
            self.game_data = {}
            self.player_amount = player_amount
            self.players_in_current_game = 0
        except error():
            print("COMPUTER CANT MAKE A SOCKET CONNECTION :: error code 33333")
            exit()

    def put_server_into_listening(self):
        self.socket.listen(self.player_amount)

    def handle_player_connections(self):
        # connect player to server when their request is received
        if self.players_in_current_game < self.player_amount:
            print("Waiting for client")
            (conn_socket, ip) = self.socket.accept()
            player_id = conn_socket.recv(1024).decode()
            self.players.append(player_id)
            self.game_data[player_id] = {}
            print(self.game_data)
            conn_socket.send("SERVER CONNECTION WORKING".encode())
            print("CONNECTED TO " + str(ip[0]) + ", " + str(ip[1]))
            self.players_addr.append(conn_socket)
            self.players_in_current_game += 1

        if self.players_in_current_game > self.player_amount:
            self.socket.listen(1)
            (conn_socket, ip) = self.socket.accept()
            player_id = conn_socket.recv(1024).decode()
            try:
                conn_socket.send("YOU MAY NOT JOIN THE PLAYER LIMIT ON THE SERVER REACHED THE MAXIMUM".encode())

            except error():
                print("CONNECTION ISSUE #$$$")
                exit()

            print(player_id + " " + "can not join this server")
            print("server reached max amount of players, this request can't be handled")

        if self.players_in_current_game == self.player_amount:
            # do nothing because all of the players are connected
            pass

    def setup_player_data(self, player, data):
        self.game_data[player] = data

    def send(self, data, client):
        try:
            client.send(data.encode())

        except error:
            print("ERROR SENDING DATA :: error code 78329")
            exit()

    def receive(self, buff, client):
        try:
            response = client.recv(buff)
            return response

        except error():
            print("CANT RECEIVE DATA FROM SERVER :: error code 03312")
            exit()
