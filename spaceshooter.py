import arcade
import math

from player import Player
from enemy import Enemy
from weapons import LASER, RAPID_FIRE, HEAVY_SHOT


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter"

ENEMY_SPAWN_TIME = 1.5

PLAYER_MAX_HEALTH = 3
DAMAGE_COOLDOWN = 1.0


class Bullet:
    def __init__(self, x, y, angle, weapon):
        self.x = x
        self.y = y
        self.angle = angle

        self.speed = weapon.bullet_speed
        self.damage = weapon.damage
        self.radius = weapon.radius
        self.weapon = weapon

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        if self.weapon.name == "Laser":
            arcade.draw_line(
            self.x,
            self.y,
            self.x - math.cos(math.radians(self.angle)) * 15,
            self.y - math.sin(math.radians(self.angle)) * 15,
            arcade.color.CYAN,
            4
        )

        elif self.weapon.name == "Rapid Fire":
            arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            arcade.color.YELLOW
        )

        elif self.weapon.name == "Heavy Shot":
            arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            arcade.color.ORANGE
        )
        

    def is_off_screen(self):
        return (
            self.x < 0
            or self.x > SCREEN_WIDTH
            or self.y < 0
            or self.y > SCREEN_HEIGHT
        )


class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE
        )

        arcade.set_background_color(arcade.color.BLACK)

        self.reset_game()

    def reset_game(self):

        self.player = Player(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

        self.bullets = []
        self.enemies = []

        self.shoot_cooldown = 0
        self.enemy_spawn_timer = 0
        self.damage_timer = 0

        self.score = 0
        self.health = PLAYER_MAX_HEALTH

        self.game_over = False

        # Start with Laser
        self.current_weapon = LASER

    def on_draw(self):

        self.clear()

        if self.game_over:

            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 30,
                arcade.color.RED,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                f"Final Score: {self.score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 20,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 60,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )

            return

        # Player
        self.player.draw()

        # Bullets
        for bullet in self.bullets:
            bullet.draw()

        # Enemies
        for enemy in self.enemies:
            enemy.draw()

        # Score
        arcade.draw_text(
            f"Score: {self.score}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

        # Health
        arcade.draw_text(
            f"Health: {self.health}/{PLAYER_MAX_HEALTH}",
            SCREEN_WIDTH - 180,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            18
        )

        # Current weapon
        arcade.draw_text(
            f"Weapon: {self.current_weapon.name}",
            20,
            20,
            arcade.color.YELLOW,
            18
        )

        # Controls
        arcade.draw_text(
            "1: Laser   2: Rapid Fire   3: Heavy Shot",
            SCREEN_WIDTH // 2,
            20,
            arcade.color.WHITE,
            14,
            anchor_x="center"
        )

    def on_update(self, delta_time):

        if self.game_over:
            return

        self.shoot_cooldown -= delta_time
        self.enemy_spawn_timer -= delta_time
        self.damage_timer -= delta_time

        # ---------------- PLAYER ----------------

        self.player.update()

        self.player.keep_inside_screen(
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

        # ---------------- BULLETS ----------------

        for bullet in self.bullets[:]:

            bullet.update()

            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        # ---------------- ENEMY SPAWNING ----------------

        if self.enemy_spawn_timer <= 0:

            self.enemies.append(
                Enemy(
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )
            )

            self.enemy_spawn_timer = ENEMY_SPAWN_TIME

        # ---------------- ENEMY MOVEMENT ----------------

        for enemy in self.enemies:

            enemy.update(
                self.player.x,
                self.player.y
            )

        # ---------------- BULLET / ENEMY COLLISION ----------------

        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                distance = math.hypot(
                    bullet.x - enemy.x,
                    bullet.y - enemy.y
                )

                if distance < bullet.radius + enemy.radius:

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if enemy.take_damage(bullet.damage):
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

                        self.score += 1

                    break

        # ---------------- ENEMY / PLAYER COLLISION ----------------

        if self.damage_timer <= 0:

            for enemy in self.enemies[:]:

                distance = math.hypot(
                    enemy.x - self.player.x,
                    enemy.y - self.player.y
                )

                if distance < enemy.radius + self.player.radius:

                    self.enemies.remove(enemy)

                    self.health -= 1

                    self.damage_timer = DAMAGE_COOLDOWN

                    if self.health <= 0:
                        self.game_over = True

                    break

    def shoot(self):

        if self.shoot_cooldown <= 0:

            x = (
                self.player.x
                + math.cos(math.radians(self.player.angle)) * 30
            )

            y = (
                self.player.y
                + math.sin(math.radians(self.player.angle)) * 30
            )

            self.bullets.append(
                Bullet(
                    x,
                    y,
                    self.player.angle,
                    self.current_weapon
                )
            )

            self.shoot_cooldown = self.current_weapon.cooldown

    def on_key_press(self, key, modifiers):

        if self.game_over:

            if key == arcade.key.R:
                self.reset_game()

            return

        self.player.keys_pressed.add(key)

        # Shoot
        if key == arcade.key.SPACE:
            self.shoot()

        # Weapon switching
        if key == arcade.key.KEY_1:
            self.current_weapon = LASER

        elif key == arcade.key.KEY_2:
            self.current_weapon = RAPID_FIRE

        elif key == arcade.key.KEY_3:
            self.current_weapon = HEAVY_SHOT

    def on_key_release(self, key, modifiers):

        if key in self.player.keys_pressed:
            self.player.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):

        self.player.aim_at(x, y)


def main():

    GameWindow()

    arcade.run()


if __name__ == "__main__":
    main()