import arcade
import math
import random

# ------------------ CONSTANTS ------------------

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter - Portfolio Version"

PLAYER_SPEED = 5
PLAYER_RADIUS = 20

BULLET_SPEED = 10
BULLET_COOLDOWN = 0.25

ENEMY_SPEED = 2
ENEMY_SPAWN_TIME = 1.5

PLAYER_LIVES = 3


# ------------------ BULLET CLASS ------------------

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = 4

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * BULLET_SPEED
        self.y += math.sin(math.radians(self.angle)) * BULLET_SPEED

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.YELLOW)

    def off_screen(self):
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT
        )


# ------------------ ENEMY CLASS ------------------

class Enemy:
    def __init__(self):
        self.x = random.choice([0, SCREEN_WIDTH])
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = 20

    def update(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * ENEMY_SPEED
        self.y += math.sin(angle) * ENEMY_SPEED

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.RED)


# ------------------ GAME WINDOW ------------------

class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.reset_game()

    def reset_game(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0

        self.bullets = []
        self.enemies = []

        self.score = 0
        self.lives = PLAYER_LIVES

        self.keys_pressed = set()

        self.bullet_timer = 0
        self.enemy_timer = 0

        self.game_over = False

    # ---------------- DRAW ----------------

    def on_draw(self):
        self.clear()

        if self.game_over:
            arcade.draw_text("GAME OVER",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                             arcade.color.WHITE, 40,
                             anchor_x="center")

            arcade.draw_text("Press R to Restart",
                             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                             arcade.color.WHITE, 20,
                             anchor_x="center")
            return

        # Draw player
        arcade.draw_triangle_filled(
            self.player_x + math.cos(math.radians(self.player_angle)) * 30,
            self.player_y + math.sin(math.radians(self.player_angle)) * 30,

            self.player_x + math.cos(math.radians(self.player_angle + 140)) * 20,
            self.player_y + math.sin(math.radians(self.player_angle + 140)) * 20,

            self.player_x + math.cos(math.radians(self.player_angle - 140)) * 20,
            self.player_y + math.sin(math.radians(self.player_angle - 140)) * 20,
            arcade.color.WHITE
        )

        for bullet in self.bullets:
            bullet.draw()

        for enemy in self.enemies:
            enemy.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 10,
                         arcade.color.WHITE, 14)

        arcade.draw_text(f"Lives: {self.lives}",
                         SCREEN_WIDTH - 100, 10,
                         arcade.color.WHITE, 14)

    # ---------------- UPDATE ----------------

    def on_update(self, delta_time):

        if self.game_over:
            return

        self.bullet_timer -= delta_time
        self.enemy_timer -= delta_time

        # Movement
        if arcade.key.W in self.keys_pressed:
            self.player_y += PLAYER_SPEED
        if arcade.key.S in self.keys_pressed:
            self.player_y -= PLAYER_SPEED
        if arcade.key.A in self.keys_pressed:
            self.player_x -= PLAYER_SPEED
        if arcade.key.D in self.keys_pressed:
            self.player_x += PLAYER_SPEED

        self.player_x = max(0, min(SCREEN_WIDTH, self.player_x))
        self.player_y = max(0, min(SCREEN_HEIGHT, self.player_y))

        # Spawn enemies
        if self.enemy_timer <= 0:
            self.enemies.append(Enemy())
            self.enemy_timer = ENEMY_SPAWN_TIME

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen():
                self.bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player_x, self.player_y)

            # Enemy hits player
            if math.hypot(enemy.x - self.player_x,
                          enemy.y - self.player_y) < enemy.radius + PLAYER_RADIUS:
                self.enemies.remove(enemy)
                self.lives -= 1

                if self.lives <= 0:
                    self.game_over = True

        # Bullet hits enemy
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if math.hypot(bullet.x - enemy.x,
                              bullet.y - enemy.y) < enemy.radius:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    break

    # ---------------- INPUT ----------------

    def shoot(self):
        if self.bullet_timer <= 0:
            x = self.player_x + math.cos(math.radians(self.player_angle)) * 30
            y = self.player_y + math.sin(math.radians(self.player_angle)) * 30
            self.bullets.append(Bullet(x, y, self.player_angle))
            self.bullet_timer = BULLET_COOLDOWN

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if key == arcade.key.SPACE:
            self.shoot()

        if key == arcade.key.R and self.game_over:
            self.reset_game()

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player_x
        dy = y - self.player_y
        self.player_angle = math.degrees(math.atan2(dy, dx))


# ------------------ MAIN ------------------

def main():
    Game()
    arcade.run()


if __name__ == "__main__":
    main()