import pygame

from models import Shawn, Python
from utils import load_sprite, random_position, print_text

class Shawnsteroids:
    MIN_PYTHON_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("bg", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.pythons = []
        self.bullets = []
        self.shawn = Shawn((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = random_position(self.screen)
                if(
                    position.distance_to(self.shawn.position) 
                    > self.MIN_PYTHON_DISTANCE
                ):
                    break

            self.pythons.append(Python(position, self.pythons.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Shawnsteroids")

    def _get_game_objects(self):
        game_objects = [*self.pythons, *self.bullets]

        if self.shawn:
            game_objects.append(self.shawn)

        return game_objects

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or(
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif(
                self.shawn
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.shawn.shoot()

        key_press = pygame.key.get_pressed()

        if self.shawn:
            if key_press[pygame.K_RIGHT]:
                self.shawn.rotate(clockwise=True)
            elif key_press[pygame.K_LEFT]:
                self.shawn.rotate(clockwise=False)
            if key_press[pygame.K_UP]:
                self.shawn.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.shawn:
            for python in self.pythons:
                if python.collides_with(self.shawn):
                    self.shawn = None
                    self.message = "You lost!"
                    break

        for pewpew in self.bullets[:]:
            for python in self.pythons[:]:
                if python.collides_with(pewpew):
                    self.pythons.remove(python)
                    self.bullets.remove(pewpew)
                    python.split()
                    break

        for pewpew in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(pewpew.position):
                self.bullets.remove(pewpew)

        if not self.pythons and self.shawn:
            self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0,0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)