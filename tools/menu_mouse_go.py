#!/usr/bin/env python3
"""menu_mouse_go.py -- move the flat game's own mouse arrow from the bottom-right corner, and click only when told.

    python menu_mouse_go.py <dx> <dy>            park in the corner, then move dx, dy (negative = left / up)
    python menu_mouse_go.py --click              left click where the arrow is now (look first!)

For leaving a page the keys cannot leave (2026-11-22: Settings > Controls, where Esc and Tab do nothing and BACK is
outside the list the keys walk). The game reads the mouse as relative moves, so: park (menu_mouse_park.py's way),
move, LOOK (menu_shot.py), then --click. Refuses when the game's window is not in front.
"""
import ctypes
import sys
import time

import menu_keys as m

PARK_STEPS, PARK_PX, STEP_PX, GAP_S = 40, 120, 20, 0.02
MOVE, LEFT_DOWN, LEFT_UP = 0x0001, 0x0002, 0x0004


def send(dx, dy, flags):
    i = m.INPUT(0, m.U(mi=m.MI(dx, dy, 0, flags, 0, None)))
    m.u.SendInput(1, ctypes.byref(i), ctypes.sizeof(i))
    time.sleep(GAP_S)


def front():
    hwnd = m.game_window()
    if not hwnd:
        sys.exit("the game's window is not there")
    m.to_front(hwnd)
    time.sleep(0.5)
    if m.exe_of(m.u.GetForegroundWindow()) != m.GAME_EXE:
        sys.exit("the game is not in front: nothing done")


def main(argv):
    front()
    if argv == ["--click"]:
        send(0, 0, LEFT_DOWN); time.sleep(0.1); send(0, 0, LEFT_UP)
        print("clicked")
        return
    dx, dy = int(argv[0]), int(argv[1])
    for _ in range(PARK_STEPS):
        send(PARK_PX, PARK_PX, MOVE)
    n = max(abs(dx), abs(dy)) // STEP_PX + 1
    for k in range(n):
        send(dx // n + (1 if k < dx % n else 0) if dx >= 0 else -((-dx) // n + (1 if k < (-dx) % n else 0)),
             dy // n + (1 if k < dy % n else 0) if dy >= 0 else -((-dy) // n + (1 if k < (-dy) % n else 0)), MOVE)
    print(f"arrow moved {dx}, {dy} from the corner")


if __name__ == "__main__":
    main(sys.argv[1:])
