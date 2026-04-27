import arcade

from Menu import MenuView


def main():
    window = arcade.Window(1200, 800, "Menu")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()