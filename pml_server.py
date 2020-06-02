"""
This is server demo for PML
This is for a very simple multi-player game
This demo may be copied, but it is illegal to copy PML

--IF YOU COPY THIS THEN THE FBI WILL COME :: FBI WARNING NP5--

Demo made by: Peter Gutkovich
-- Contact Info --
Email: peter.mty8@gmail.com
Phone Number: 347-623-8734
"""

# import json for packing and unpacking json dict strings
from json import loads, dumps
# import the amazing pml library
import pml
# import random
from random import randint

# create game server
game_server = pml.Server(1234, 2)


# create command for handling the "get_game_info" client command
def get_game_info_command_handler(client):
    non_included_player_dict = game_server.game_data.copy()
    non_included_player_dict.pop(player_msg['player'])
    game_server.send(dumps(non_included_player_dict), client)


# function to update game data
def update_coordinates_to_game(client, update_x, update_y, player):
    # what to send to client
    send_back = ""

    # try updating to the game data
    try:
        # change the game's player's data
        game_server.setup_player_data(player=player, data={'x': update_x,
                                                           'y': update_y})
        send_back = "OK"
    except ValueError:
        send_back = "ERROR"
        print("THERE WAS AN ERROR")

    # send response
    game_server.send(data=send_back, client=client)


# put server socket into listening mode
game_server.put_server_into_listening()

# handle incoming player connections and set players their game values
for i in range(game_server.player_amount):
    game_server.handle_player_connections()

for player in game_server.players:
    game_server.setup_player_data(player=player, data={'x': randint(0, 400),
                                                       'y': randint(0, 400)})


# game loop
while True:
    # collect from each player in game
    for i in game_server.players_addr:
        # get info from player
        player_msg = game_server.receive(1024, i)
        player_msg = loads(player_msg)
        # get the command name that the player called
        fun = player_msg['function']
        # get the actual data that the player sent for the server to analyze
        client_data = loads(player_msg['data'])
        # get the player id of the player who send the data
        player = player_msg['player']

        # if command is "get_game_info" then call function
        if fun == "get_game_info":
            get_game_info_command_handler(client=i)

        # if the command is "update_coordinates" then call function
        if fun == "update_coordinates":
            update_coordinates_to_game(client=i, update_x=client_data['new_x'], update_y=client_data['new_y'], player=player)

        if fun == "get_FULL_game":
            game_server.send(client=i, data=dumps(game_server.game_data))
