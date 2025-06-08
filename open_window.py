import pygame
import pyretro_gui as rg
from pyretro_gui.container import *
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
    container = MovableContainer(50, 50, container_width*2, container_height*2, content_surf)
    # Función para manejar click dentro del container (opcional)
    def container_click(container_obj, pos):
        print(f"Click dentro de container en posición relativa {pos}")
    container.onclick = container_click

    rg.add_widget(container)

def on_chat_icon_click(mouse_pos=None):
    def create_chat_content_surface_with_padding(width=400, height=300, padding_top=30):
        content_surf = pygame.Surface((width, height))
        content_surf.fill((220, 220, 240))  # Fondo claro

        font = pygame.font.SysFont("arial", 20)
        messages = [
            "Usuario1: Hola, ¿cómo estás?",
            "Usuario2: Bien, gracias.",
            "Usuario1: ¿Quieres jugar?",
            "Usuario2: Claro, vamos allá!"
        ]

        y = padding_top  # Iniciar desde el padding superior
        for msg in messages:
            text_surf = font.render(msg, True, (50, 50, 100))
            content_surf.blit(text_surf, (10, y))
            y += 30

        return content_surf

    # Luego en la creación de ChatAppWindow
    content_surface = create_chat_content_surface_with_padding()
    chat_win = ChatAppWindow(50, 50, 400, 360, content_surface,label="Chat")
    rg.add_widget(chat_win)

