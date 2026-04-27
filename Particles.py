import random
import arcade
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval

DUST = arcade.make_soft_circle_texture(5, arcade.color.LIGHT_GRAY, 180, 50)
JUMP = arcade.make_soft_circle_texture(8, arcade.color.LIGHT_GRAY, 220, 80)
LAND_TEX = arcade.make_soft_circle_texture(8, arcade.color.LIGHT_GRAY, 200, 80)
HOOK_SPARK_TEX = [
    arcade.make_soft_circle_texture(10, arcade.color.RED, 255, 120),
    arcade.make_soft_circle_texture(9, arcade.color.YELLOW, 255, 150),
    arcade.make_soft_circle_texture(7, arcade.color.GRAY, 255, 100),
    arcade.make_soft_circle_texture(8, arcade.color.ORANGE, 255, 180),
]


def dust_mutator(p):
    p.change_x *= 0.95
    p.change_y *= 0.95


def jump_mutator(p):
    p.change_y += -0.02
    p.change_x *= 0.92


def hook_mutator(p):
    p.change_x *= 0.97
    p.change_y += 0.02
    p.angle += random.uniform(-2, 2)


def land_mutator(p):
    p.change_x *= 0.93
    p.change_y *= 0.93
    p.scale = (p.scale[0] * 0.95, p.scale[1] * 0.95)
    p.alpha *= 0.95


def make_dust(x, y):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitInterval(0.02),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=DUST,
            change_xy=(random.uniform(2.0, 4.0), random.uniform(1.0, 3.0)),
            lifetime=random.uniform(1.0, 1.5),
            scale=random.uniform(1.2, 1.8),
            start_alpha=255,
            end_alpha=0,
            mutation_callback=dust_mutator,
        ),
    )


def make_jump_sparks(x, y):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(15),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=JUMP,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 2.5),
            lifetime=random.uniform(0.4, 0.7),
            scale=random.uniform(0.3, 0.6),
            start_alpha=180, end_alpha=0,
            mutation_callback=jump_mutator,
        ),
    )


def make_dust_on_landing(x, y):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(20),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=LAND_TEX,
            change_xy=(random.uniform(-4.5, 4.5), random.uniform(0.3, 2.5)),
            lifetime=random.uniform(0.3, 0.7),
            scale=random.uniform(0.4, 1.5),
            start_alpha=160, end_alpha=0,
            mutation_callback=land_mutator,
        ),
    )


def make_hook_is_attach(x, y):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(15),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(HOOK_SPARK_TEX),
            change_xy=arcade.math.rand_on_circle((0.0, 0.0), 3),
            lifetime=random.uniform(0.2, 0.5),
            scale=random.uniform(0.3, 0.8),
            start_alpha=random.randint(180, 220),
            end_alpha=0,
            mutation_callback=hook_mutator,
        ),
    )


class ParticleSystem:
    def __init__(self):
        self.emitters = []
        self.walk_emitter = None
        self.is_walking = False
        self.hook_emitter = None
        self.was_on_earth = True

    def grappling_hook(self, x, y):  # Зацепление крюка
        self.emitters.append(make_hook_is_attach(x, y))

    def jump(self, x, b):  # Прыжок
        self.emitters.append(make_jump_sparks(x, b))

    def particles_landing(self, x, b):  # Пыль при приземлении
        self.emitters.append(make_dust_on_landing(x, b))

    def start_walking(self, x, b):  # Пыль из-под ног
        if not self.walk_emitter:
            self.walk_emitter = make_dust(x, b)
            self.emitters.append(self.walk_emitter)
        self.is_walking = True

    def stop_walking(self):  # Пыль заканчивается
        self.is_walking = False
        if self.walk_emitter and self.walk_emitter in self.emitters:
            self.emitters.remove(self.walk_emitter)
            self.walk_emitter = None

    def update(self, delta_time, player_x=None, player_y=None,
               player_bottom=None):
        if self.walk_emitter and self.is_walking and player_x is not None:
            self.walk_emitter.center_x = player_x
            self.walk_emitter.center_y = player_bottom

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap() and e != self.walk_emitter:
                self.emitters.remove(e)


    def draw(self):
        for e in self.emitters:
            e.draw()


    def landing_check(self, is_jump):
        if not self.was_on_earth and is_jump:
            self.was_on_earth = True
            return True
        elif self.was_on_earth and not is_jump:
            self.was_on_earth = False
        return False
