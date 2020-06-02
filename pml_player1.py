"""
This is a client demo for PML
This is a very simple multi-player game
This demo may be copied, but it is illegal to copy PML

--IF YOU COPY THIS THEN THE FBI WILL COME :: FBI WARNING NP5--

Demo made by: Peter Gutkovich
-- Contact Info --
Email: peter.mty8@gmail.com
Phone Number: 347-623-8734
"""

# import pml
import pml
# import json for packing and unpacking dicts into and from json strings
from json import dumps, loads
# import pygame for graphics
from pygame import init, display, draw, event, quit, QUIT
import pygame

# init pygame and create background with caption
init()
game_background = display.set_mode((400, 400))


# create simple player object
class Player:
    def __init__(self, length, width, color, starter_x, starter_y, screen, name):
        self.length = length
        self.width = width
        self.color = color
        self.x = starter_x
        self.y = starter_y
        self.background = screen

        font = pygame.font.Font(None, 20)
        self.text = font.render(name, True, (0, 200, 0), (0, 0, 128))

    def draw(self):
        draw.rect(self.background, self.color, (self.x, self.y, self.length, self.width))

    def label(self, on=None):
        if on:
            textRect = self.text.get_rect()
            textRect.center = (self.x + 20, self.y + 20)
            self.background.blit(self.text, textRect)

        if not on:
            pass


# this is a dictionary that will be containing all of the object players in the current game
players = {}

# create client that connects to server and port 1234, alice is the client's id for the server
id = 'shrek'
this_player = pml.Client('10.0.1.8', 1234, id)

display.set_caption(id)


# function for getting all information from players in the game
def get_game():
    # in pml data must always be sent to the server in dict form, but here we don't need any data
    send_data = {'': ''}
    # send a new command to the server called get_game_info, and the data being send is send_data
    this_player.send_new_command(command_name="get_game_info", data_being_sent=dumps(send_data))
    # get server response after server handles the command and data sent by this player
    response = this_player.receive(1024)
    return response


# function for getting full game
def get_FULL_game():
    # in pml data must always be sent to the server in dict form, but here we don't need any data
    send_data = {'': ''}
    # send a new command to the server called get_game_info, and the data being send is send_data
    this_player.send_new_command(command_name="get_FULL_game", data_being_sent=dumps(send_data))
    # get server response after server handles the command and data sent by this player
    response = this_player.receive(1024)
    return response


def update_coordinates_to_game(update_x, update_y):
    # our data to send to the server is the new x and y coordinates of this player
    send_data = {'new_x': update_x,
                 'new_y': update_y}
    # send send_data and command name to server which is "update_coordinates"
    this_player.send_new_command(command_name="update_coordinates", data_being_sent=dumps(send_data))
    # get server response after server handles the command and data sent by this player
    response = this_player.receive(1024)
    return response


# setup this players starting coordinates
x = 0
y = 0

p = loads(get_FULL_game())
for player_id in p:
    players[player_id] = Player(length=40, width=40, color=(0, 200, 0), starter_x=p[player_id]['x'],
                                starter_y=p[player_id]['y'],
                                screen=game_background, name=player_id)
    print(player_id)
    if player_id == id:
        x = p[player_id]['x']
        y = p[player_id]['y']

change_x = 0
change_y = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            this_player.kill_connection()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_x = 0
                change_y = -0.1

            if event.key == pygame.K_DOWN:
                change_x = 0
                change_y = 0.1

            if event.key == pygame.K_LEFT:
                change_y = 0
                change_x = -0.1

            if event.key == pygame.K_RIGHT:
                change_y = 0
                change_x = 0.1

    x += change_x
    y += change_y

    # call our get game function to get information about other players
    game_data = loads(get_game())

    # get each player's info from the game
    for player in game_data:
        players[player].x = game_data[player]['x']
        players[player].y = game_data[player]['y']

    if x > 360:
        x = 0

    if x < 0:
        x = 360

    if y > 360:
        y = 0

    if y < 0:
        y = 360

    # here we update this players coordinates to the server by calling the update_coordinates_to_game function
    status = update_coordinates_to_game(x, y)

    # check server's response to the request and check if everything worked
    if status == "OK":
        pass

    if status == "ERROR":
        print("there is an error :: error code 11111(regular systematic error code)")
        exit()

    players[id].x = x
    players[id].y = y

    game_background.fill((0, 0, 0))
    for i in players:
        players[i].draw()
        players[i].label(on=True)

    # here the graphics will be controlled (players will be drawn to screen)
    display.update()
