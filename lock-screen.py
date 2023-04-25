import os
import time
from Xlib import display
import pyautogui
from pynput import keyboard, mouse
import threading

pyautogui.FAILSAFE = False

def ft_lock():
    keyboard.Controller().press(keyboard.Key.esc)
    keyboard.Controller().release(keyboard.Key.esc)
    os.system("ft_lock")
    print("Program exited properly.")
    os._exit(0)

def mouse_position():
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]

def mouse_starting_position():
    last_x, last_y = mouse_position()
    return last_x, last_y

def countdown(total_minutes):
    total_seconds = total_minutes * 60
    while total_seconds > 0:
        hrs, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)
        timer = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        print(timer, end="\r")
        time.sleep(1)
        total_seconds -= 1
    print(f"\n{total_minutes} min countdown end...\nLocking screen...")
    ft_lock()

def delay_before_lock(minutes):
    countdown(minutes)

def lock_if_mouse_moves():
    while not exit_event.is_set():
        x, y = mouse_position()
        if x != initial_x or y != initial_y:
            print(f"Mouse moved!\nx ===> {x}/{initial_x}\ny ===> {y}/{initial_y}...\nLocking screen...")
            ft_lock()

pressed_keys = set()

def on_key_press(key):
    pressed_keys.add(key)
    time.sleep(0.1)
    if keyboard.Key.home in pressed_keys and keyboard.Key.end in pressed_keys:
        print(f"Keys pressed: home and end...\nProgram exited properly...")
        os._exit(0)
    elif key not in {keyboard.Key.home, keyboard.Key.end, keyboard.Key.esc}:
        print(f"Key pressed: {key}...\nLocking screen...")
        ft_lock()

def on_key_release(key):
    pressed_keys.discard(key)

def on_mouse_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse button {button} pressed...\nLocking screen...")
        ft_lock()

def on_mouse_scroll(x, y, dx, dy):
    print(f"Mouse wheel scrolled...\nLocking screen...")
    ft_lock()

if __name__ == "__main__":
    start_x = 1919
    fixed_y = 0

    delay_minutes = int(input("Enter the delay in minutes for delay_before_lock: "))
    pyautogui.click(start_x, fixed_y, button='left')

    exit_event = threading.Event()

    move_pointer_thread = threading.Thread(target=delay_before_lock, args=(delay_minutes,))
    move_pointer_thread.start()

    initial_x, initial_y = mouse_starting_position()

    monitor_mouse_thread = threading.Thread(target=lock_if_mouse_moves)
    monitor_mouse_thread.start()

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as key_listener, \
         mouse.Listener(on_click=on_mouse_click, on_scroll=on_mouse_scroll) as mouse_listener:
        key_listener.join()
        mouse_listener.join()

    exit_event.set()
    move_pointer_thread.join()
    monitor_mouse_thread.join()
    print("Program exited properly.")
