"""Made by Peter Gutkovich 2020
Please Do Not Copy Or Reproduce"""
import socket
import json
import pygame
import time
import easygui as eg

print("LAUNCHING MULTI-PLAYER GAME PLATFORM. MADE BY PETER CONTACT AT 347-623-8724. THANK YOU FOR USING THIS SERVICE")
time.sleep(3)
print("\n")

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("player2")


class Player:
    def __init__(self, x, y, color, s):
        self.x = x
        self.y = y
        self.color = color
        self.screen = s
        self.pickup_interaction_status = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 40, 40))

    # collision function
    def check_pickup_collision(self, x1, x2, y1, y2, w1, w2):
        if x2 < x1 + w1:
            if x2 > x1:
                if x2 + w2 < x1 + w1:
                    if x2 + w2 > x1:
                        if y2 < y1 + w1:
                            if y2 > y1:
                                if y2 + w2 < y1 + w1:
                                    if y2 + w2 > y1:
                                        self.pickup_interaction_status = True


class Pickup:
    def __init__(self, x, y, color, s):
        self.x = x
        self.y = y
        self.color = color
        self.screen = s

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 10, 10))


connection = False

ip = '10.0.1.14'
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
print("connection made")
print(s.recv(1024).decode())
print("TCP HANDSHAKE ESTABLISHED")
connection = True


def send(data, function, player):
    send_data = {'data': data, 'function': function, 'player': player}
    send_data = json.dumps(send_data)
    s.send(send_data.encode())


def receive(buff):
    server_msg = s.recv(buff).decode()
    return server_msg


class API:
    def __init__(self, id, password, player):
        self.id = id
        self.password = password
        self.player = player

    def get_starters(self):
        request_data = {'id': self.id,
                        'password': self.password,
                        }

        send(data=json.dumps(request_data), function="get_coor", player=self.player)
        try:
            response = json.loads(receive(1024))
        except socket.error:
            response = {}
        return response

    def get(self):
        request_data = {'id': self.id,
                        'password': self.password,
                        }

        send(data=json.dumps(request_data), function="get_coor", player=self.player)
        try:
            response = json.loads(receive(1024))
        except socket.error:
            response = {}
        return response

    def update_player_coordinates(self, x, y):
        request_data = {'x': x,
                        'y': y,
                        }

        # send request data to server which will then update to game
        send(data=json.dumps(request_data), function="new_coor", player=self.player)
        try:
            response = receive(1024)
        except socket.error:
            response = ""

        return response

    # communication server that player uses if they collide with the pickup item
    def update_pickup_status_to_server(self, points):
        request_data = {'players_interaction_with_pickup_status': p2.pickup_interaction_status, 'my_points': points}
        send(data=json.dumps(request_data), function="set_new_pickup_coordinates", player=self.player)
        p2.pickup_interaction_status = False

        try:
            response = receive(1024)
        except socket.error:
            response = ""

        print(response)

    def kill_game(self, tie=None):
        request_data = {'tie': 'false'}
        if tie:
            request_data = {'tie': 'true'}

        send(data=json.dumps(request_data), function="end_game", player=self.player)
        try:
            response = receive(1024)

        except socket.error:
            response = ""

        return response


if connection:
    game = API(id='4321', password='peter_the_ultra_coder', player='2')
    starters = game.get_starters()
    p1x = int(starters['x-coor1'])
    p1y = int(starters['y-coor1'])

    p2x = int(starters['x-coor2'])
    p2y = int(starters['y-coor2'])

    pux = int(starters['pickup_coorx'])
    puy = int(starters['pickup_coory'])
    print(pux, puy)

    p1 = Player(p1x, p1x, (255, 0, 0), screen)
    p2 = Player(p2x, p2y, (0, 200, 0), screen)
    pickup_item = Pickup(pux, puy, (255, 255, 0), screen)
    pickup_points_p2 = 0

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    s.close()
                    pygame.quit()

                status = ""
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        p2.x -= 5
                        new_x = int(p2.x)
                        new_y = int(p2.y)
                        status = game.update_player_coordinates(x=str(new_x), y=str(new_y))

                    if event.key == pygame.K_RIGHT:
                        p2.x += 5
                        new_x = int(p2.x)
                        new_y = int(p2.y)
                        status = game.update_player_coordinates(x=str(new_x), y=str(new_y))

                    if event.key == pygame.K_UP:
                        p2.y -= 5
                        new_x = int(p2.x)
                        new_y = int(p2.y)
                        status = game.update_player_coordinates(x=str(new_x), y=str(new_y))

                    if event.key == pygame.K_DOWN:
                        p2.y += 5
                        new_x = int(p2.x)
                        new_y = int(p2.y)
                        # just to update player coordinates to server + 3 of the above
                        status = game.update_player_coordinates(x=str(new_x), y=str(new_y))

                    if status != "WORKING":
                        print("CANT UPDATE YOUR COORDINATES :: error code 1")

            coords = game.get()
            player1x = coords['x-coor1']
            player1y = coords['y-coor1']
            pux = coords['pickup_coorx']
            puy = coords['pickup_coory']
            p1.x = int(player1x)
            p1.y = int(player1y)
            pickup_item.x = int(pux)
            pickup_item.y = int(puy)
            p1_pickup_points = coords['pickup_points_p1']
            print("YOUR POINTS: " + str(pickup_points_p2))
            print("OTHER PLAYER\'S POINTS: " + str(p1_pickup_points))

            # check collision with player and pickup item
            p2.check_pickup_collision(p2.x, pickup_item.x, p2.y, pickup_item.y, 40, 10)
            if p2.pickup_interaction_status:
                pickup_points_p2 += 1
                game.update_pickup_status_to_server(pickup_points_p2)

            screen.fill((0, 0, 0))
            p1.draw()
            p2.draw()
            pickup_item.draw()
            pygame.display.update()

            # check if player 2 won
            if pickup_points_p2 == 5 and pickup_points_p2 > p1_pickup_points:
                eg.msgbox("The Winner Of This Game Is You!!")
                # right here player 2 will tell the server that they won and the server will shutdown
                res = game.kill_game()
                if res == "OK":
                    print("server allows ending")
                    break

            # check if player 1 won
            if p1_pickup_points == 5 and p1_pickup_points > pickup_points_p2:
                eg.msgbox("The Winner Of This Game Is The Other Player")
                # automatic shutdown because server will already be shutdown
                break

            # player 2 is the unique one and they send the tie message to the server
            if pickup_points_p2 == 5 and p1_pickup_points == 5:
                res = game.kill_game(tie=True)
                if res == "OK":
                    print("server allows tie ending")
                    eg.msgbox("There Was A Tie Between You And The Other Player")
                    break

    pygame.quit()
    print("\n")
    print("Your Session is Over")
    exit()

if not connection:
    print("can\'t connect to server :: client error 10029")
