import arcade
import math
import random


ENEMY_RADIUS = 20
ENEMY_SPEED = 2
ENEMY_HEALTH = 3


class Enemy:

    def __init__(self, screen_width, screen_height):

        self.radius = ENEMY_RADIUS
        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH

        side = random.choice(
            ["top", "bottom", "left", "right"]
        )

        if side == "top":
            self.x = random.randint(0, screen_width)
            self.y = screen_height

        elif side == "bottom":
            self.x = random.randint(0, screen_width)
            self.y = 0

        elif side == "left":
            self.x = 0
            self.y = random.randint(0, screen_height)

        else:
            self.x = screen_width
            self.y = random.randint(0, screen_height)

    def update(self, player_x, player_y):

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.hypot(dx, dy)

        if distance > 0:

            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def take_damage(self, damage):

        self.health -= damage

        return self.health <= 0

    def draw(self):

        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            arcade.color.RED
        )