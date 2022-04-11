from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, random_speed

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, speed):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width()/2
        self.speed = Vector2(speed)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.speed, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Shawn(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3
    def __init__(self, position, create_bullet_callback):
        self.bullet = create_bullet_callback
        UP = Vector2(0, -1)
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("shawn"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.speed += self.direction * self.ACCELERATION

    def shoot(self):
        bullet_speed = self.direction * self.BULLET_SPEED + self.speed
        bullet = PewPew(self.position, bullet_speed)
        self.bullet(bullet)

class Python(GameObject):
    def __init__(self, position, create_python_callback, size = 3):
        self.ensmallen = create_python_callback
        self.size = size

        size_scale = {
            3: 1,
            2: 0.5,
            1: 0.25
        }
        scale = size_scale[size]
        sprite = rotozoom(load_sprite("python"), 0, scale)

        super().__init__(
            position, sprite, random_speed(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                python = Python(
                    self.position, self.ensmallen, self.size - 1
                )
                self.ensmallen(python)

class PewPew(GameObject):
    def __init__(self, position, speed):
        super().__init__(position, load_sprite("bullet"), speed)
    def move(self, surface):
        self.position = self.position + self.speed