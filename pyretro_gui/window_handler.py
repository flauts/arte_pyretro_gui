
import sys, os
import pygame
from .app_core import app_state
from .constants import SCR_BORDER, SCREEN_PAD, SCREEN_X_POS, SCREEN_Y_POS

from .retro_screen import get_mouse_pos

if sys.platform != "win32":
    from .retro_screen import x_resize_window, x_maximize

pygame.init()

WINDOW_FLAGS    = pygame.NOFRAME

if sys.platform == "win32":
    SW_NORMAL   = 1
    SW_MAXIMIZE = 3
    SW_MINIMIZE = 6
else:
    BAR_SIZE = 50

__info = pygame.display.Info()
_win_size = (0, 0)

def move_check ():
    if not pygame.display.get_window_position or not pygame.display.set_window_position:
        print("Unable to get/set window position, update pygame-ce version! Minimum pygame-ce version is >= 2.5.x")
        os._exit(1)

def resize_screen ():
    return
    w, h = app_state.Window.get_size()
    new_size = (w - SCREEN_X_POS * 2 - SCR_BORDER, h - SCREEN_Y_POS - SCREEN_PAD - SCR_BORDER)
    new_screen = pygame.Surface(new_size)
    pygame.transform.scale(app_state.screen, new_size, new_screen)
    app_state.screen = new_screen

def _maximize_app (btn):
    app_state.windowized_size = pygame.display.get_window_size()
    app_state.windowized_pos = pygame.display.get_window_position()
    if sys.platform == "win32":
        move_check()
        pygame.display.set_mode((1, 1), pygame.RESIZABLE)
        hwnd = pygame.display.get_wm_info()["window"]

        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
        size = list(pygame.display.get_window_size()).copy()

        titlebar_h = ctypes.windll.user32.GetSystemMetrics(4)
        size[1] += titlebar_h

        pygame.display.set_mode((1, 1), app_state.flags)
        pygame.display.set_mode(size, app_state.flags)

        x, y = pygame.display.get_window_position()
        pygame.display.set_window_position((x, y - titlebar_h))

    else:
        x_maximize()

    btn.name = "windowize"
    btn.load_img()
    btn.onclick = _windowize_app

def _minimize_app (btn):
    pygame.display.iconify()

def _move_window (btn):
    move_check()

    mx, my = get_mouse_pos()
    x = mx - btn.origin_press[0]
    y = my - btn.origin_press[1]

    pygame.display.set_window_position((x, y))

def _rezize_window (border):
    move_check()
    if app_state.moving: return

    rv = border.resize_vector
    op = border.origin_press
    
    new_size = list(pygame.display.get_window_size())
    new_pos = list(pygame.display.get_window_position())

    orig_size = new_size.copy()
    orig_pos = new_pos.copy()

    mx, my = get_mouse_pos()

    # x
    if rv[0] > 0:
        new_size[0] = mx - orig_pos[0]

    if rv[0] < 0:
        s = orig_pos[0] - mx
        new_size[0] += s
        new_pos[0] = mx

    # y
    if rv[1] > 0:
        new_size[1] = my - orig_pos[1]

    if rv[1] < 0:
        # s = orig_pos[1] - my
        ns = (orig_pos[1] + orig_size[1]) - my
        # new_size[1] = s + orig_size[1]
        new_size[1] = ns
        new_pos[1] = my - op[1]


    if sys.platform == "win32":
        # this caused flickering on linux
        pygame.display.set_mode(new_size, app_state.flags)
    else:
        x_resize_window(new_size)

    pygame.display.set_window_position(new_pos)


def _windowize_app (btn):
    if sys.platform == "win32":
        hwnd = pygame.display.get_wm_info()["window"]

        import ctypes
        ctypes.windll.user32.ShowWindow(hwnd, SW_NORMAL)

    pygame.display.set_mode(app_state.windowized_size, app_state.flags)
    if sys.platform != "win32":
        pygame.display.set_window_position(app_state.windowized_pos)

    btn.name = "maximize"
    btn.load_img()
    btn.onclick = _maximize_app

