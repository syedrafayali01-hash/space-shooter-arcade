import arcade
import math


PLAYER_SPEED = 5
PLAYER_RADIUS = 20


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

        self.speed = PLAYER_SPEED
        self.radius = PLAYER_RADIUS

        self.keys_pressed = set()

    def update(self):
        if arcade.key.W in self.keys_pressed:
            self.y += self.speed

        if arcade.key.S in self.keys_pressed:
            self.y -= self.speed

        if arcade.key.A in self.keys_pressed:
            self.x -= self.speed

        if arcade.key.D in self.keys_pressed:
            self.x += self.speed

    def keep_inside_screen(self, width, height):
        self.x = max(self.radius, min(width - self.radius, self.x))
        self.y = max(self.radius, min(height - self.radius, self.y))

    def aim_at(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y

        self.angle = math.degrees(math.atan2(dy, dx))

    def draw(self):
        arcade.draw_triangle_filled(
            self.x + math.cos(math.radians(self.angle)) * 30,
            self.y + math.sin(math.radians(self.angle)) * 30,

            self.x + math.cos(math.radians(self.angle + 140)) * 20,
            self.y + math.sin(math.radians(self.angle + 140)) * 20,

            self.x + math.cos(math.radians(self.angle - 140)) * 20,
            self.y + math.sin(math.radians(self.angle - 140)) * 20,

            arcade.color.WHITE
        )