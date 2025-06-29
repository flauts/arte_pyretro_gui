
import pygame

from .retro_button import RetroButton
from .app_core import app_state
from .constants import Colors

from .scrollbar import ScrollBar

class Container():
    def __init__ (self, x: int, y: int, w: int, h: int, content_surf: pygame.Surface, onclick = None, onpressed = None, anchors: list[int] = [0, 0], z_index = -100,label="Test"):

        self.x, self.y = x, y
        self.w, self.h = w, h
        self._surface = pygame.Surface((w, h))
        self.label=label
        self.content_surf = content_surf
        self.content_size = list(content_surf.get_size())

        self.onclick = onclick
        self.onpressed = onpressed
        self.anchors = anchors
        self.z_index = z_index

        self.pressed = False
        self.__prev_pressed = self.pressed

        self.mpos_inside = None
        self._prev_pos_inside = None

        self.is_scroll_x = self.content_size[0] > w
        self.is_scroll_y = self.content_size[1] > h

        self.scrollbars = []

        if self.is_scroll_x:
            self.scrollbars.append(ScrollBar(0, 0, w - 16, self.content_size[0], horizontal = True, anchors = [0, 1]))
            self.content_size[0] += ScrollBar.SCRLBAR_WIDTH

        if self.is_scroll_y:
            self.scrollbars.append(ScrollBar(0, 0, h, self.content_size[1], anchors = [1, 0]))
            self.content_size[1] += ScrollBar.SCRLBAR_WIDTH



    def get_surface (self):
        return self._surface

    def get_rect (self, win_size):
        r = [self.x, self.y, self.w, self.h]
        if self.anchors[0]: r[0] = win_size[0] - r[0] - r[2]
        if self.anchors[1]: r[1] = win_size[1] - r[1] - r[3]

        return pygame.Rect(r)

    def get_content_dif (self):
        return [abs(self.content_size[0] - self.w), abs(self.content_size[1] - self.h)]

    def get_x_scrollbar (self):
        for s in self.scrollbars:
            if s.horizontal: return s
        return None

    def get_y_scrollbar (self):
        for s in self.scrollbars:
            if not s.horizontal: return s
        return None

    def update (self, mouse_pos, mouse_btns, win_size):

        for event in app_state.events:
            if event.type == pygame.MOUSEWHEEL:
                s = self.get_x_scrollbar() if pygame.key.get_pressed()[pygame.K_LSHIFT] else self.get_y_scrollbar()
                if s is not None:
                    if event.y < 0:
                        s.down(None)
                    elif event.y > 0:
                        s.up(None)

                sx = self.get_x_scrollbar()
                if sx is not None:
                    if event.x < 0:
                        sx.up(None)
                    elif event.x > 0:
                        sx.down(None)

        r = self.get_rect(win_size)

        self.focused = r.collidepoint(mouse_pos)
        self.__prev_pressed = self.pressed
        self.pressed = self.focused and mouse_btns[0] and not app_state.resizing

        self._prev_pos_inside = self.mpos_inside if self.mpos_inside is not None else (mouse_pos[0] - r.x, mouse_pos[1] - r.y)
        self.mpos_inside = (mouse_pos[0] - r.x, mouse_pos[1] - r.y)

        # pressed
        if self.pressed and self.onpressed:
            if not self.__prev_pressed:
                self.origin_press = mouse_pos

            self.onpressed(self, self.mpos_inside)

        # clicked
        if not self.pressed and self.__prev_pressed and self.focused:
            if self.onclick:
                self.onclick(self, self.mpos_inside)

        for s in self.scrollbars:
            s.update(mouse_pos, mouse_btns, self.get_rect(win_size).topleft, self._surface.get_rect())

    def close_container(self,mouse_pos):
        app_state.widgets.remove(self)

    def render (self, win, _):
        self._surface.fill((0, 0, 0))
        dif = self.get_content_dif()
        xp = 0 if not self.is_scroll_x else - dif[0] * self.get_x_scrollbar().progress
        yp = 0 if not self.is_scroll_x else - dif[1] * self.get_y_scrollbar().progress
        self._surface.blit(self.content_surf, (xp, yp))

        for s in self.scrollbars:
            s.render(self._surface, _, self._surface.get_rect())


        pygame.draw.rect(self._surface, Colors.TEXT, self._surface.get_rect(), 1)
        win.blit(self._surface, self.get_rect(win.get_size()).topleft)

from .move_button import MoveButton  # importar MoveButton

class MovableContainer(Container):
    _max_z_index = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragging = False
        self.drag_offset = (0, 0)

        icon_size = RetroButton.ICON_SIZE
        pad = RetroButton.PAD
        icon_pad = RetroButton.PAD//2

        self.move_button = MoveButton(self.x, self.y+60, 10, 20,label=self.label)
        # Poner z_index alto
        MovableContainer._max_z_index += 1
        self.z_index = MovableContainer._max_z_index
        self.close_button = RetroButton(self.x, icon_size, w = icon_size, h = icon_size, colors=[Colors.CLOSE, Colors.CLOSE_HOVER],
                                        onclick=self.close_container, z_index=self.z_index, name="close")


    def update(self, mouse_pos, mouse_btns, win_size):
        self.move_button.x = self.x
        self.move_button.y = self.y
        self.move_button.w = self.w
        self.close_button.x = self.x + self.w - self.close_button.w - self.close_button.PAD//2
        self.close_button.y = self.y
        self.close_button.update(mouse_pos,mouse_btns,win_size)

        # Obtener rect del container
        rect = self.get_rect(win_size)
        mouse_inside = rect.collidepoint(mouse_pos)

        # Comprobar si self es el container con z_index más alto bajo el cursor
        if mouse_inside:
            # Filtrar todos los MovableContainer que contienen el mouse
            containers_under_mouse = [
                w for w in app_state.widgets
                if isinstance(w, MovableContainer) and w.get_rect(win_size).collidepoint(mouse_pos)
            ]
            # Encontrar el z_index máximo
            max_z = max(w.z_index for w in containers_under_mouse) if containers_under_mouse else -1
            # Solo permitir arrastrar si self tiene este z_index máximo
            can_drag = (self.z_index == max_z)
        else:
            can_drag = False

        for event in app_state.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and can_drag:
                    # Mouse presionado dentro y es el container más arriba
                    if self.get_rect(win_size).collidepoint(mouse_pos):
                        self.dragging = True
                        self.drag_offset = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
                        # Subir el z_index para estar arriba
                        MovableContainer._max_z_index += 1
                        self.z_index = MovableContainer._max_z_index

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

            elif event.type == pygame.MOUSEWHEEL:
                # misma lógica scroll existente
                s = self.get_x_scrollbar() if pygame.key.get_pressed()[pygame.K_LSHIFT] else self.get_y_scrollbar()
                if s is not None:
                    if event.y < 0:
                        s.down(None)
                    elif event.y > 0:
                        s.up(None)

                sx = self.get_x_scrollbar()
                if sx is not None:
                    if event.x < 0:
                        sx.up(None)
                    elif event.x > 0:
                        sx.down(None)

        if self.dragging:
            self.x = mouse_pos[0] - self.drag_offset[0]
            self.y = mouse_pos[1] - self.drag_offset[1]

        super().update(mouse_pos, mouse_btns, win_size)

    def render(self, win, win_size):
        super().render(win, win_size)
        self.move_button.render(win, win_size)
        self.close_button.render(win, win_size)



from .retro_button import RetroButton
from .constants import Colors
from .retro_text import font


class ChatAppWindow(MovableContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.content_surf = pygame.Surface((self.w, self.h - 100))
        self.chat_list = ["Chat con Ana", "Chat con Pedro", "Grupo Amigos"]
        self.chats = {
            "Chat con Ana": ["Hola!", "¿Cómo estás?"],
            "Chat con Pedro": ["¿Viste el partido?", "Qué locura!"],
            "Grupo Amigos": ["🤙", "Vamos a juntarnos!"]
        }
        self.selected_chat = None
        self.input_options = ["👍", "Gracias", "Hasta luego"]
        self.state = "list"  # 'list' o 'chat'

        self.buttons = []  # Botones para la lista o las opciones
        self.back_button = RetroButton(10, 10, 80, 24, [Colors.BG, Colors.LIGHT_BG],
                                       label="< Volver", onclick=self.back_to_list)
        self.back_button.z_index = 10

        self.create_list_buttons()

    def create_list_buttons(self):
        self.buttons.clear()
        btn_y_start = 50
        btn_h = 30
        for i, chat_name in enumerate(self.chat_list):
            btn = RetroButton(10, btn_y_start + i * btn_h, self.w - 20, btn_h,
                              [Colors.BG, Colors.LIGHT_BG],
                              label=chat_name, onclick=self.make_select_chat_callback(chat_name))
            btn.z_index = 5
            self.buttons.append(btn)

    def make_select_chat_callback(self, chat_name):
        def select_chat(btn):
            self.selected_chat = chat_name
            self.state = "chat"
            self.create_chat_buttons()

        return select_chat

    def create_chat_buttons(self):
        self.buttons.clear()
        btn_y_start = self.h - 100
        btn_h = 30
        btn_w = (self.w - 40) // len(self.input_options)
        for i, option in enumerate(self.input_options):
            btn = RetroButton(10 + i * (btn_w + 5), btn_y_start, btn_w, btn_h,
                              [Colors.BG, Colors.LIGHT_BG], Colors.TEXT, Colors.SHADOW,
                              label=option, onclick=self.make_send_message_callback(option))
            btn.z_index = 5
            self.buttons.append(btn)

    def make_send_message_callback(self, message):
        def send_message(btn):
            if self.selected_chat:
                self.chats[self.selected_chat].append(message)

        return send_message

    def back_to_list(self, btn=None):
        self.state = "list"
        self.selected_chat = None
        self.create_list_buttons()

    def update(self, mouse_pos, mouse_btns, win_size):
        super().update(mouse_pos, mouse_btns, win_size)

        self.back_button.update(mouse_pos, mouse_btns, win_size)
        for btn in self.buttons:
            btn.update(mouse_pos, mouse_btns, win_size)

    def render(self, win, win_size):
        super().render(win, win_size)
        # surf = self.content_surf
        # surf.fill(Colors.BG)

        if self.state == "list":
            # Título chats
            title = font.render("Chats", True, Colors.TEXT)
            # surf.blit(title, (10, 10))

        elif self.state == "chat":
            # Botón volver
            # self.back_button.render(surf, win_size)

            # Título chat activo
            chat_title = font.render(self.selected_chat or "", True, Colors.TEXT)
            # surf.blit(chat_title, (100, 15))

            # Mostrar mensajes
            y = 50
            for msg in self.chats.get(self.selected_chat, []):
                msg_txt = font.render(msg, True, Colors.TEXT)
                # surf.blit(msg_txt, (10, y))
                y += 30

        # Renderizar botones (lista chats u opciones)
        for btn in self.buttons:
            pass# btn.render(surf, win_size)

        # Finalmente bliteamos todo al win
        # win.blit(surf, (self.x, self.y))

