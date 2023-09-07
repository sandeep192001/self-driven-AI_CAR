
import random
import time
import sys
import pygame

from brain import NeuralNetwork, copy
from car import Car


WIDTH = 1920 / 1.25
HEIGHT = 1080 / 1.25
TOTAL = 2

brains = [NeuralNetwork(5, 8, 4) for _ in range(TOTAL)]


def calculate_fitness(cars):

    total_dis = sum(c.distance for c in cars)
    for c in cars: c.fitness = c.distance / total_dis

def generate_cars(cars):

    calculate_fitness(cars)

    new_cars = random.choices(list(enumerate(cars)), weights=[c.fitness for c in cars], k=TOTAL)


    for j in range(len(new_cars)):
        brains[j] = copy(brains[new_cars[j][0]])
        brains[j].mutate(0.25)

    return [Car() for _ in range(TOTAL)]

def run_simulation(GENERATION):


    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    game_map = pygame.image.load('map.png').convert()
    game_map = pygame.transform.scale(game_map, (WIDTH, HEIGHT))
    alive_font = pygame.font.SysFont("Arial", 20)
    generation_font = pygame.font.SysFont("Arial", 30)

    cur_cars = [Car() for _ in range(TOTAL)]

    while True:

        if GENERATION > 50: break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)


        for i, car in enumerate(cur_cars):
            output = list(car.predict(brains[i])[0])
            choice = output.index(max(output))

            if choice == 0:
                car.angle += 10
            elif choice == 1:
                car.angle -= 10
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2
            else:
                car.speed += 2

        alive = 0
        screen.blit(game_map, (0, 0))

        for c in cur_cars:
            if c.alive:
                alive += 1
                c.update(game_map)


        for c in cur_cars:
            if c.alive:
                c.draw(screen)

        if alive == 0:
            cur_cars = generate_cars(cur_cars)

        text = generation_font.render("Generation: " + str(GENERATION), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':

    run_simulation(1)

