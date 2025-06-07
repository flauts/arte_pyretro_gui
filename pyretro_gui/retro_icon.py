#
# import pygame
#
# from .constants import Colors
# from .retro_button import RetroButton
#
# class RetroIcon(RetroButton):
#
#     def __init__(self, x: int, y: int, w: int = 24, h: int = 32, color: tuple = Colors.BG, border_color: tuple = Colors.TEXT, icon: pygame.Surface | None = None, anchors: list[int] = [0, 0], z_index: int = 0):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.rect = pygame.Rect(x, y, w, h)
#         self.anchors = anchors
#         self.z_index = z_index
#
#         self.color = color
#         self.border_color = border_color
#
#         self.icon = icon
#
#         self._disabled = False
#
#     def update (self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
#         pass
#
#     def render(self, win, win_size):
#         r = self.get_rect(win_size)
#         r.w += 1
#         r.h += 1
#
#         pygame.draw.rect(win, self.color, r)
#         pygame.draw.rect(win, self.border_color, r, 1)
#         pygame.draw.line(win, self.border_color, (r.x, r.y + r.h), (r.x + r.w - 1, r.y + r.h), 1)
#
#         if self.icon: win.blit(self.icon, [r.x, r.y])
import pygame

from .constants import Colors
from .retro_button import RetroButton
from .retro_text import small_font


class RetroIcon(RetroButton):

    def __init__(self, x: int, y: int, w: int = 24, h: int = 32, color: tuple = Colors.BG,
                 border_color: tuple = Colors.TEXT, icon: pygame.Surface | None = None, anchors: list[int] = [0, 0],
                 z_index: int = 0, image_path: str | None = None, label: str = "",onclick=None):
        super().__init__(x, y, w, h, [color, Colors.LIGHT_BG], anchors=anchors, z_index=z_index,onclick=onclick,image_path=image_path)
        self.label = label
        self.color = color
        self.border_color = border_color
        self._disabled = False
        self.selected = False
        self.clicked = False
        self.font = small_font
        self.icon = icon

    def update(self, mouse_pos: list[int], mouse_btns: list[bool], win_size):
        prev_pressed = getattr(self, 'pressed', False)
        super().update(mouse_pos,mouse_btns,win_size)
        r = self.get_rect(win_size)
        is_clicked =  prev_pressed and r.x < mouse_pos[0] < r.x + r.w and r.y <mouse_pos[1] < r.y + r.h
        if self.pressed and not prev_pressed:
            self.selected = not self.selected
        self.clicked = is_clicked
        self.__prev_pressed = mouse_btns[0]

    def render(self, win, win_size):
        r = self.get_rect(win_size)
        r.w += 1
        r.h += 1
        if self.clicked: r.y-= 1.5

        # Draw selection background if selected
        if self.selected:
            pygame.draw.rect(win, Colors.LIGHT_BG,r)

        pygame.draw.rect(win, self.color, r)
        pygame.draw.rect(win, self.border_color, r, 1)
        pygame.draw.line(win, self.border_color, (r.x, r.y + r.h), (r.x + r.w - 1, r.y + r.h), 1)

        if self.img:
            win.blit(self.img, [r.x, r.y])

        if self.icon:
            win.blit(self.icon, [r.x, r.y])

        if self.label:
            text_surface = self.font.render(self.label, False, Colors.TEXT)
            text_rect = text_surface.get_rect(center=(r.x + r.w // 2, r.y + r.h + 8))
            win.blit(text_surface, text_rect)
