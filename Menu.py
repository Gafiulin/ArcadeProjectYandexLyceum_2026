import arcade
from arcade.gui import UITextureButton, UIManager

from pyglet.graphics import Batch
from GameView import GameView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/menu_textura/menu_textura.jpg")
        self.manager = UIManager()
        self.manager.enable()
        self.batch = Batch()
        self.main_text = arcade.Text("Бегун с крюком", self.window.width / 2, self.window.height / 2 + 100,
                                     arcade.color.BLACK, font_size=40, anchor_x="center", batch=self.batch)
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        self.texture_button = UITextureButton(x=self.window.width / 2 - 100, y=self.window.height / 2,
                                              texture=texture_normal,
                                              texture_hovered=texture_hovered,
                                              texture_pressed=texture_pressed,
                                              scale=1.0, text="Начать игру")
        self.texture_button.on_click = self.on_texture_button_click
        self.manager.add(self.texture_button)
        self.space_text = arcade.Text("Нажми, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.description_text = arcade.Text("Используй AD и SPACE для движения, клик правой кнопки мыши для использования крюка",
                                            self.window.width / 2, self.window.height / 2 - 100,
                                            arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.window.width / 2, self.window.height / 2,
                                                                self.window.width, self.window.height))
        self.batch.draw()
        self.manager.draw()

    def on_texture_button_click(self, event=None):
        game_view = GameView(level=1)
        self.window.show_view(game_view)


