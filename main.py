
import pyretro_gui as rg
from pyretro_gui import Colors, RetroIcon
from pyretro_gui.container import MovableContainer
import pygame
from open_window import *
rg.create_window(940, 680, "Test App title", "testicon.png")
def file_new(click):
    print("File -> New clicked!")

def file_exit(click):
    print("File -> Exit clicked!")
    rg.app_state.running = False

def help_about(click):
    print("Help -> About clicked!")

# Example button click function
def on_start_game_click():
    print("Start Game button clicked!")
file_dropdown = rg.DropDown([
    rg.MenuItem("New", onclick=file_new),
    rg.MenuItem("Open"),
    rg.MenuItem("Save"),
    rg.MenuItem("Exit", onclick=file_exit, shortcut="Alt+4")
])

help_dropdown = rg.DropDown([
    rg.MenuItem("About", onclick=help_about)
])

menu_items = [
    rg.MenuItem("File", letter_index=0, dropdown=file_dropdown),
    rg.MenuItem("Edit", letter_index=0),
    rg.MenuItem("Help", letter_index=0, dropdown=help_dropdown)
]

rg.add_widget(rg.MenuBar(menu_items))



# Drawing Rectangle
def abrir_mi_computadora(btn):
    print("¡Mi Computadora abierta!")

computer_icon = RetroIcon(100, 100, image_path="testicon2.png",label="computer")
mail_icon = RetroIcon(200, 100, image_path="testicon2.png",label="mail")
canvas_icon = RetroIcon(300, 100, image_path="testicon2.png",label="canvas",onclick=abrir_mi_computadora)
chat_icon = RetroIcon(400, 100, image_path="testicon2.png",label="chat",onclick=on_chat_icon_click)

rg.add_widget(chat_icon)
rg.add_widget(computer_icon)
rg.add_widget(mail_icon)
rg.add_widget(canvas_icon)




icon = RetroIcon(x=300, y=150, image_path="testicon.png",onclick=on_icon_click)
rg.add_widget(icon)

while rg.app_state.running:
    rg.window_update()
    rg.window_render() #desktop background