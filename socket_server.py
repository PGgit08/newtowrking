import socket
import json

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create socket parameters
ip = socket.gethostbyname("LAPTOP-B5V26S9O")
port = 1234

# create server on ip and port
server.bind((ip, port))

# listen to client connection requests
server.listen(5)

# some player setup
players = 0
players_addr = []

# connection to clients
while players < 2:
    # receive connection request from clients through TCP
    print("WAITING FOR CLIENT")
    (conn_socket, address) = server.accept()
    print("CONNECTED TO " + str(address[0]) + ", " + str(address[1]))
    players += 1
    players_addr.append(conn_socket)
    conn_socket.send("HELLO AND WELCOME TO PETER\t'S SERVER!".encode())


# game making and API
games_info = [
    {'id': 1234,
     'password': 'peter_the_coder',
     'x-coor1': 30,
     'y-coor1': 40,
     'x-coor2': 100,
     'y-coor2': 100,
    },
    {'id': 4321,
     'password': 'peter_the_ultra_coder',
     'x-coor1': 80,
     'y-coor1': 170,
     'x-coor2': 20,
     'y-coor2': 50,
    }]


def send(data, client):
    client.send(data.encode())


def receive(buff, client):
    client_msg = client.recv(buff).decode()
    return client_msg


def return_game(request, client):
    global games_info, id, password

    credentials = request
    id = int(credentials['id'])
    password = credentials['password']
    game_requested = ""
    for game in games_info:
        if game['id'] == id and game['password'] == password:
            game_requested = json.dumps(game)
            break

        else:
            game_requested = "ERROR: PASSWORD AND/OR ID ARE FALSE"

    send(data=game_requested, client=client)


def set_new_coords(request, player, client):
    global games_info, id, password

    new_x = int(request['x'])
    new_y = int(request['y'])
    for i in games_info:
        if i['id'] == id and i['password'] == password:
            game_to_change = i
            game_to_change['x-coor' + player] = int(new_x)
            game_to_change['y-coor' + player] = int(new_y)
            games_info[games_info.index(i)] = game_to_change

    send(data="WORKING", client=client)


while True:
    # get requests from player 1
    player1_req = receive(1024, players_addr[1])
    player1_req = json.loads(player1_req)
    function_to_run_p1 = player1_req['function']
    if function_to_run_p1 == "get_coor":
        return_game(request=json.loads(player1_req['data']), client=players_addr[1])

    if function_to_run_p1 == "new_coor":
        set_new_coords(request=json.loads(player1_req['data']), player='1', client=players_addr[1])

    # get requests from player 2
    player2_req = receive(1024, players_addr[0])
    player2_req = json.loads(player2_req)
    function_to_run_p2 = player2_req['function']
    if function_to_run_p2 == "get_coor":
        return_game(request=json.loads(player2_req['data']), client=players_addr[0])

    if function_to_run_p2 == "new_coor":
        set_new_coords(request=json.loads(player2_req['data']), player='2', client=players_addr[0])
