import arcade

SCALE = 0.1
ANIMATION_TIMER = 0.05
SPEED = 5

class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.anim1 = []
        self.anim2 = []
        self.stand = []
        self.is_Rmoving = False
        self.is_Lmoving = False
        for i in range(7):
            sprite = arcade.Sprite(f"images/hero_textura/animation_frames/anim{i + 1}.png")
            self.anim1.append(sprite)
        for i in range(7):
            sprite = arcade.Sprite(f"images/hero_textura/animation_frames/anim{(i + 1) * 11}.png")
            self.anim2.append(sprite)
        for i in range(2):
            sprite = arcade.Sprite(f"images/hero_textura/hero{i + 1}.png")
            self.stand.append(sprite)
        self.anim_timer = 0
        self.scale = SCALE
        self.cur_texture = 0
        self.center_x = 504
        self.center_y = 288
        self.texture = self.stand[0].texture
        self.side = 0

    def start_Rmoving(self):
        self.is_Rmoving = True
        self.is_Lmoving = False
        self.side = 0

    def start_Lmoving(self):
        self.is_Lmoving = True
        self.is_Rmoving = False
        self.side = 1

    def stop_moving(self):
        self.is_Rmoving = False
        self.is_Lmoving = False


    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.is_Rmoving:
            self.anim_timer -= delta_time
            if self.anim_timer <= 0:
                self.texture = self.anim1[self.cur_texture].texture
                self.cur_texture = (self.cur_texture + 1) % 7
                self.anim_timer = ANIMATION_TIMER
        elif self.is_Lmoving:
            self.anim_timer -= delta_time
            if self.anim_timer <= 0:
                self.texture = self.anim2[self.cur_texture].texture
                self.cur_texture = (self.cur_texture + 1) % 7
                self.anim_timer = ANIMATION_TIMER
        else:
            self.texture = self.stand[self.side].texture
            self.anim_timer = 0

