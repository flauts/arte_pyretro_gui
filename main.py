
import pyretro_gui as rg
from pyretro_gui import Colors, RetroIcon
from pyretro_gui.container import MovableContainer
import pygame
rg.create_window(1000, 1000, "Test App title", "testicon.png")
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


rg.add_widget(computer_icon)
rg.add_widget(mail_icon)
rg.add_widget(canvas_icon)
containers = []

def on_icon_click(mouse_pos):
    # Crear superficie de contenido más grande que el container para activarlo scroll
    content_width, content_height = 600, 400
    content_surf = pygame.Surface((content_width, content_height))
    content_surf.fill((220, 220, 240))  # Fondo claro

    # Dibujar algo en el contenido para demostrar scroll
    font = pygame.font.SysFont(None, 24)
    for y in range(0, content_height, 40):
        txt = font.render(f"Línea en y={y}", True, (50, 50, 100))
        content_surf.blit(txt, (10, y))

    # Crear un Container más pequeño que el contenido para activar scroll
    container_width, container_height = 300, 200
    container = MovableContainer(50, 50, container_width, container_height, content_surf)

    # Para darle borde, pinta borde en su surface (z_index lo puedes ajustar si quieres)
    border_color = (0, 0, 0)
    pygame.draw.rect(container._surface, border_color, container._surface.get_rect(), 2)

    # Función para manejar click dentro del container (opcional)
    def container_click(container_obj, pos):
        print(f"Click dentro de container en posición relativa {pos}")
    container.onclick = container_click

    rg.add_widget(container)


icon = RetroIcon(x=300, y=150, image_path="testicon.png",onclick=on_icon_click)
rg.add_widget(icon)

while rg.app_state.running:
    rg.window_update()
    rg.window_render() #desktop background