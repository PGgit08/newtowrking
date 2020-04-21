import socket
import json
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))


class Player:
    def __init__(self, x, y, color, s):
        self.x = x
        self.y = y
        self.color = color
        self.screen = s

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 40, 40))


p1x = 0
p1y = 0

p2x = 100
p2y = 100

p1 = Player(p1x, p1x, (255, 0, 0), screen)
p2 = Player(p2x, p2y, (255, 0, 0), screen)

connection = False

ip = socket.gethostbyname("LAPTOP-B5V26S9O")
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
print("connection made")
print(s.recv(1024).decode())
connection = True


def send(data, function):
    send_data = {'data': data, 'function': function}
    send_data = json.dumps(send_data)
    s.send(send_data.encode())


def receive(buff):
    server_msg = s.recv(buff).decode()
    return server_msg


class API:
    def __init__(self, id, password):
        self.id = id
        self.password = password

    def get_coordinates(self):
        request_data = {'id': self.id,
                        'password': self.password}

        send(data=json.dumps(request_data), function="get_coor")
        try:
            response = json.loads(receive(1024))
        except socket.error:
            response = {}
        return response

    def new_coordinates(self, x, y):
        request_data = {'x': x,
                        'y': y}
        send(data=json.dumps(request_data), function="new_coor")
        try:
            response = receive(1024)
        except socket.error:
            response = ""

        return response


if connection:
    game = API(id='1234', password='peter_the_coder')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p2.x -= 5

                if event.key == pygame.K_RIGHT:
                    p2.x += 5

                if event.key == pygame.K_UP:
                    p2.y -= 5

                if event.key == pygame.K_DOWN:
                    p2.y += 5

        coords = game.get_coordinates()
        player1x = coords['x-coor1']
        player1y = coords['y-coor1']
        print(player1x, player1y)
        p1.x = int(player1x)
        p1.y = int(player1y)

        new_x = int(p2.x)
        new_y = int(p2.y)

        if new_x > -1 and new_y > -1:
            status = game.new_coordinates(x=str(new_x), y=str(new_y))
            print(status)

        screen.fill((0, 0, 0))
        p1.draw()
        p2.draw()
        pygame.display.update()
