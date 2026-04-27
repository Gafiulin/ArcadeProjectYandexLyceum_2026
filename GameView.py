import time

import arcade

from Hero import Hero
from Particles import ParticleSystem

GRAVITY = 1.5
PLAYER_SPEED = 5
JUMP_SPEED = 20

CAMERA_LERP = 0.12
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class GameView(arcade.View):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.start_time = int(round(time.time()))
        self.time_text = arcade.Text("00:00", SCREEN_WIDTH - 20,
                                     SCREEN_HEIGHT - 20, arcade.color.WHITE, 24, anchor_x="right")
        self.particles = ParticleSystem()
        arcade.set_background_color(arcade.color.BLACK)
        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.harpoonn = arcade.SpriteList()
        if level == 1:
            map_name = "maps/first_level.tmx"
        elif level == 2:
            map_name = "maps/second_level.tmx"
            liner = []
            with open("results.txt", 'r', encoding='utf-8') as r:
                for line in r:
                    liner.append(line.strip())
                self.map1_time = int(((liner[1]).split(" "))[-1].split(":")[0]) * 60 + int(((liner[1]).split(" "))[-1].split(":")[1])

        self.harpoon_sprite = arcade.Sprite("images/harpoon.png", scale=0.1)
        self.tile_map = arcade.load_tilemap(map_name)
        self.walls = self.tile_map.sprite_lists["blocks"]
        self.lava = self.tile_map.sprite_lists["lava"]
        self.exit = self.tile_map.sprite_lists["exit"]
        self.decorations = self.tile_map.sprite_lists["decorations"]
        self.decorate_background = self.tile_map.sprite_lists["decorate background"]
        self.background = self.tile_map.sprite_lists["background"]
        self.collision_list = self.tile_map.sprite_lists["blocks"]

        self.player_sprite = Hero()

        self.up = False
        self.left = False
        self.right = False
        self.harpoon = False

        self.xx = 0
        self.yy = 0

        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100

        self.harpoon_sprite.center_x = self.xx
        self.harpoon_sprite.center_y = self.yy

        self.player_list.append(self.player_sprite)
        self.harpoonn.append(self.harpoon_sprite)

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.walls,
        )

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.walls.draw()
        self.lava.draw()
        self.exit.draw()
        self.decorations.draw()
        self.decorate_background.draw()
        self.background.draw()
        self.particles.draw()
        self.player_list.draw()
        if self.harpoon:
            if arcade.check_for_collision_with_list(self.harpoon_sprite, self.walls):
                self.harpoonn.draw()
                arcade.draw_line(
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    self.xx,
                    self.yy,
                    arcade.color.BLACK,
                    2
                )
        self.gui_camera.use()
        self.time_text.draw()

    def on_update(self, delta_time):
        self.engine.update()
        self.player_list.update(delta_time)
        is_jump = self.engine.can_jump(y_distance=5)
        self.time_now = int(round(time.time()))
        if self.level == 2:
            self.elaps_time = self.time_now - self.start_time + self.map1_time
        else:
            self.elaps_time = self.time_now - self.start_time
        self.time_text = arcade.Text(f"{self.elaps_time // 60:02d}:{self.elaps_time % 60:02d}",
                                     SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20,
                                     arcade.color.WHITE, font_size=24, anchor_x="right", anchor_y="top")

        if self.up:
            if is_jump:
                self.engine.jump(JUMP_SPEED)
                self.particles.jump(self.player_sprite.center_x, self.player_sprite.bottom)
                self.up = False
        if self.particles.landing_check(is_jump):
            self.particles.particles_landing(self.player_sprite.center_x, self.player_sprite.bottom)

        if self.harpoon:
            if arcade.check_for_collision_with_list(self.harpoon_sprite, self.walls):
                dx = self.xx - self.player_sprite.center_x
                dy = self.yy - self.player_sprite.center_y
                if dx != 0 or dy != 0:
                    length = (dx ** 2 + dy ** 2) ** 0.5
                    if length > 0:
                        dx /= length
                        dy /= length
                        power = 25
                        self.player_sprite.center_x += dx * power
                        self.player_sprite.center_y += dy * power
                        self.player_sprite.change_y = 0

        if arcade.check_for_collision_with_list(self.player_sprite, self.lava):
            from GameOver import GameOverview
            game_over_view = GameOverview()
            self.window.show_view(game_over_view)

        if arcade.check_for_collision_with_list(self.player_sprite, self.exit):
            self.next_level()

        if (self.left or self.right) and is_jump and not self.harpoon:
            self.particles.start_walking(
                self.player_sprite.center_x,
                self.player_sprite.bottom)
        else:
            self.particles.stop_walking()

        self.particles.update(
            delta_time,
            player_x=self.player_sprite.center_x,
            player_y=self.player_sprite.center_y,
            player_bottom=self.player_sprite.bottom)

        self.camera_player()

    def next_level(self):
        lines = []
        self.level += 1
        with open("results.txt", 'r', encoding='utf-8') as r:
            for line in r:
                lines.append(line.strip())
            rek_line = lines[0]
            rek = int((rek_line.split(" "))[-1].split(":")[0]) * 60 + int((rek_line.split(" "))[-1].split(":")[1])
            if (self.elaps_time < rek or rek == 0) and self.level == 3:
                rek_line = f"Рекорд времени прохождения {self.elaps_time // 60}:{self.elaps_time % 60}"
            else:
                rek_line = f"Рекорд времени прохождения {rek // 60}:{rek % 60}"
        for i, line in enumerate(lines):
            if "Пройдено за " in line:
                lines[i] = f"Пройдено за {self.elaps_time // 60}:{self.elaps_time % 60}"
            elif "Рекорд времени прохождения " in line:
                lines[i] = rek_line
        with open("results.txt", 'w', encoding='utf-8') as r:
            r.write('\n'.join(lines) + '\n')
        if self.level == 3:
            from GameWin import VictoryView
            game_win_view = VictoryView()
            self.window.show_view(game_win_view)
            self.level = 1
        else:
            game_view = GameView(level=self.level)
            self.window.show_view(game_view)

    def camera_player(self):
        tx, ty = self.player_sprite.center_x, self.player_sprite.center_y
        cam_x, cam_y = self.world_camera.position
        new_x, new_y = cam_x + (tx - cam_x) * CAMERA_LERP, cam_y + (ty - cam_y) * CAMERA_LERP
        min_x = SCREEN_WIDTH // 2
        min_y = SCREEN_HEIGHT // 2
        max_x = self.tile_map.tile_width * self.tile_map.width
        max_y = self.tile_map.height * self.tile_map.tile_height
        target = (max(min(max_x, new_x), min_x), max(min(max_y, new_y), min_y))

        self.world_camera.position = target

    def on_key_press(self, key, modifiers):
        match key:
            case arcade.key.A:
                self.left = True
            case arcade.key.D:
                self.right = True
            case arcade.key.SPACE:
                self.up = True
        self.update_movement()

    def on_key_release(self, key, modifiers):
        match key:
            case arcade.key.A:
                self.left = False
            case arcade.key.D:
                self.right = False
        self.update_movement()

    def update_movement(self):
        if self.left and not self.right:
            self.player_sprite.change_x = -PLAYER_SPEED
            self.player_sprite.start_Lmoving()

        elif self.right and not self.left:
            self.player_sprite.change_x = PLAYER_SPEED
            self.player_sprite.start_Rmoving()

        else:
            self.player_sprite.change_x = 0
            self.player_sprite.stop_moving()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            camera_x, camera_y = self.world_camera.position
            world_x = x + camera_x - SCREEN_WIDTH // 2
            world_y = y + camera_y - SCREEN_HEIGHT // 2
            self.xx = world_x
            self.yy = world_y
            self.harpoon_sprite.center_x = world_x
            self.harpoon_sprite.center_y = world_y
            self.harpoon = True
            self.particles.grappling_hook(world_x, world_y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.harpoon = False
