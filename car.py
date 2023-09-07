
import math
import pygame
from brain import NeuralNetwork


CAR_SIZE_X = 60 / 1.25
CAR_SIZE_Y = 60 / 1.25
CAR_POS_X = 820 / 1.25
CAR_POS_Y = 920 / 1.25

BORDER_COLOR = (255, 255, 255, 255)

class Car:

    def __init__(self):
        self.img = pygame.image.load('car.png').convert()
        self.img = pygame.transform.scale(self.img, (CAR_SIZE_X, CAR_SIZE_Y))

        self.rotated_img = self.img

        self.pos = [CAR_POS_X, CAR_POS_Y]

        self.center = [ self.pos[0] + 0.5 * CAR_SIZE_X, self.pos[1] + 0.5 * CAR_SIZE_Y ]

        self.count = 0

        self.angle = 0
        self.speed = 0
        self.radar = []
        self.drawing_radars = []

        self.alive = True
        self.distance = 0
        self.time = 0
        self.speed_set = False
        self.fitness = 0

    def draw(self, screen):
        screen.blit(self.rotated_img, self.pos)
        self.draw_radar(screen)



    def collison(self, game_map):
        self.alive = True

        for point in self.corners :
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                return True

        return False

    def update(self, game_map):

        if not self.speed_set:
            self.speed = 10
            self.speed_set = True

        if self.time % 60 == 0:
            self.distance += 1

        self.rotated_img = self.rotate_center(self.img, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed

        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.center = [ self.pos[0] + 0.5 * CAR_SIZE_X, self.pos[1] + 0.5 * CAR_SIZE_Y ]

        length = 0.75 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.complete(game_map)
        if self.count == 2:
            print('complete')

        self.collison(game_map)

        self.radar.clear()

        for d in range(-90, 120, 45):
            self.check_rader(d, game_map)

    def draw_radar(self, screen):
        for radar in self.radar:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_rader(self, angle, game_map):
        length  = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * length)

        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * length)

        dist = math.sqrt(math.pow(x-self.center[0], 2) + math.pow(y-self.center[1], 2))
        self.radar.append([(x, y), dist])

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def get_data(self):
        radars = self.radar
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def predict(self, brain):
        return brain.predict(self.get_data())


    def complete(self, game_map):
        for point in self.corners :
            if game_map.get_at((int(point[0]), int(point[1]))) not in (BORDER_COLOR, (0, 0, 0, 0)):
                self.count += 1
