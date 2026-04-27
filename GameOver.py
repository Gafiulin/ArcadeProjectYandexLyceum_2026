import arcade
from arcade.gui import UILabel, UIManager, UIFlatButton



class GameOverview(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.manager = UIManager()
        self.manager.enable()
        label = UILabel(x=self.window.width / 2 - 150, y=self.window.height / 2 + 100,
                        text="Game Over",
                        font_size=40,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.manager.add(label)
        restar_button = UIFlatButton(
            x=200,
            y=150,
            text="Возродиться",
            width=200,
            height=50
        )
        restar_button.on_click = self.on_restart_click
        self.manager.add(restar_button)
        menu_button = UIFlatButton(
            x=800,
            y=150,
            text="В Меню",
            width=200,
            height=50
        )
        menu_button.on_click = self.on_menu_click
        self.manager.add(menu_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_restart_click(self, event=None):
        from GameView import GameView
        completely_new_game = GameView(level=1)
        self.window.show_view(completely_new_game)

    def on_menu_click(self, event=None):
        from Menu import MenuView
        completely_new_game = MenuView()
        self.window.show_view(completely_new_game)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

