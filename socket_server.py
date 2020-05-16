"""Made by Peter Gutkovich 2020
Please Do Not Copy Or Reproduce"""
import socket
import json
import random

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create socket parameters
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234

# create server on ip and port
server.bind((ip, port))

# listen to client connection requests
server.listen(5)

# some player setup
players = 0
players_addr = []

# save the current game info
ID = 0
PASSWORD = ""

# connection to clients
while players < 2:
    # receive connection request from clients through TCP
    print("WAITING FOR CLIENT")
    (conn_socket, address) = server.accept()
    print("CONNECTED TO " + str(address[0]) + ", " + str(address[1]))
    players += 1
    players_addr.append(conn_socket)
    conn_socket.send("HELLO AND WELCOME TO THE MULTI-PLAYER SERVER!".encode())


# game making and API
games_info = [
    {'id': 1234,
     'password': 'peter_the_coder',
     'x-coor1': 0,
     'y-coor1': 0,
     'x-coor2': 600,
     'y-coor2': 400,
     'pickup_coorx': random.randint(0, 600),
     'pickup_coory': random.randint(0, 400),
     'pickup_points_p1': 0,
     'pickup_points_p2': 0
    },
    {'id': 4321,
     'password': 'peter_the_ultra_coder',
     'x-coor1': 200,
     'y-coor1': 200,
     'x-coor2': 20,
     'y-coor2': 50,
     'pickup_coorx': 50,
     'pickup_coory': 13,
     'pickup_points_p1': 0,
     'pickup_points_p2': 0
    }]


# function for sending to client
def send(data, client):
    client.send(data.encode())


# function for receiving from client
def receive(buff, client):
    client_msg = client.recv(buff).decode()
    return client_msg


# return game for get_coor client command
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
            game_requested = "ERROR: PASSWORD AND/OR ID ARE FALSE(error:79)"

    send(data=game_requested, client=client)


# set new player coords for new_coor client command
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


# set new coordinates for pickup item for set_new_pickup_coordinates command
def new_pickup_coords(game_id, game_password, client_to_send_back_response):

    while True:
        new_x = random.randint(0, 600)
        new_y = random.randint(0, 400)
        coordinate_duplicate = False

        # find the right game
        for i in games_info:
            if i['id'] == game_id and i['password'] == game_password:
                game_to_change = i
                if new_x == game_to_change['pickup_coorx']:
                    coordinate_duplicate = True

                if new_y == game_to_change['pickup_coory']:
                    coordinate_duplicate = True

                else:
                    # set new pickup coordinates
                    game_to_change['pickup_coorx'] = new_x
                    game_to_change['pickup_coory'] = new_y
                    coordinate_duplicate = False

                if not coordinate_duplicate:
                    games_info[games_info.index(i)] = game_to_change
                    break

                if coordinate_duplicate:
                    break

        if not coordinate_duplicate:
            break

        if coordinate_duplicate:
            continue

    send(client=client_to_send_back_response, data="OK")


# start server logs
print("\n")
print("SERVER LOGS ON THE BOTTOM")
# receive from clients forever until someone wins
while True:
    # in each loop
    for client in players_addr:
        client_msg = receive(1024, client)
        request = json.loads(client_msg)
        player = request['player']
        func = request['function']
        data = json.loads(request['data'])
        print("GOT REQUEST FROM " + str(client))
        if func == "get_coor":
            ID = int(data['id'])
            PASSWORD = data['password']
            return_game(request=data, client=client)
            print("returned requested game data to player")

        if func == "new_coor":
            set_new_coords(request=data, client=client, player=player)
            print("set new coordinates on server for player")

        if func == "set_new_pickup_coordinates":
            if data['players_interaction_with_pickup_status']:
                new_pickup_coords(game_id=ID, game_password=PASSWORD, client_to_send_back_response=client)
                # re-find current game
                for i in games_info:
                    if i['id'] == ID and i['password'] == PASSWORD:
                        # set new player points
                        game_to_change = i
                        game_to_change['pickup_points_p' + player] = data['my_points']
                        print("player_points from " + player + " " + str(data['my_points']))
                        games_info[games_info.index(i)] = game_to_change

            else:
                print("ERROR: UNKNOWN STATUS WITH PLAYER AND PICKUP, (error:3391)")
                send('you are having some issue', client=client)

        if func == "end_game":
            if data['tie'] == 'false':
                send(data="OK", client=client)
                print("\n")
                print("SUCCESSFULLY ENDED SESSION WITH PLAYERS :: WINNER WAS PLAYER " + player)
                exit()

            if data['tie'] == 'true':
                send(data="OK", client=client)
                print("\n")
                print("SUCCESSFULLY ENDED SESSION WITH PLAYERS :: IT WAS A TIE")
                exit()
