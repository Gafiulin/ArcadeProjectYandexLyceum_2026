import arcade
from arcade.gui import UIManager, UILabel


class VictoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.LIGHT_BLUE
        self.manager = UIManager()
        self.manager.enable()
        self.results_text2 = ""
        lines = []
        with open("results.txt", 'r', encoding='utf-8') as r:
            for line in r:
                lines.append(line.strip())
            rek = int((lines[0].split(" "))[-1].split(":")[0]) * 60 + int((lines[0].split(" "))[-1].split(":")[1])
            run_result = int((lines[1].split(" "))[-1].split(":")[0]) * 60 + int((lines[1].split(" "))[-1].split(":")[1])
            if run_result == rek:
                results_text = f"Новый рекорд {(lines[0].split(" "))[-1]}!"
            else:
                results_text = f"Вы прошли игру за {(lines[1].split(" "))[-1]}!"
                self.results_text2 = f"Рекордное время {(lines[0].split(" "))[-1]}"
        win_label = UILabel(x=self.window.width / 2 - 150, y=self.window.height / 2 + 100,
                            text="Victory",
                            font_size=40,
                            text_color=arcade.color.RED,
                            width=300,
                            align="center",
                            bold="semibold")
        self.manager.add(win_label)
        label = UILabel(x=self.window.width / 2 - 180, y=self.window.height / 2,
                        text="Нажмите ESC для выхода в меню",
                        font_size=25,
                        text_color=arcade.color.GRAY,
                        width=300,
                        align="center",
                        italic=True)
        self.manager.add(label)
        results = UILabel(x=self.window.width / 2 - 180, y=self.window.height / 2 - 50,
                        text=results_text,
                        font_size=25,
                        text_color=arcade.color.GRAY,
                        width=300,
                        align="center",
                        italic=True)
        self.manager.add(results)
        if self.results_text2:
            results2 = UILabel(x=self.window.width / 2 - 180, y=self.window.height / 2 - 100,
                          text=self.results_text2,
                          font_size=25,
                          text_color=arcade.color.GRAY,
                          width=300,
                          align="center",
                          italic=True)
            self.manager.add(results2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.go_to_menu()

    def go_to_menu(self):
        from Menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
