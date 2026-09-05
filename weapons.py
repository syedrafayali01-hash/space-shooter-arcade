class Weapon:
    def __init__(self, name, damage, bullet_speed, cooldown, radius):
        self.name = name
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.cooldown = cooldown
        self.radius = radius


LASER = Weapon(
    name="Laser",
    damage=1,
    bullet_speed=10,
    cooldown=0.30,
    radius=4
)

RAPID_FIRE = Weapon(
    name="Rapid Fire",
    damage=1,
    bullet_speed=13,
    cooldown=0.10,
    radius=3
)

HEAVY_SHOT = Weapon(
    name="Heavy Shot",
    damage=3,
    bullet_speed=7,
    cooldown=0.70,
    radius=7
)