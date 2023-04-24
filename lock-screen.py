import os
import time
from Xlib import display
import pyautogui
from pynput import keyboard
import threading

pyautogui.FAILSAFE = False
ctrl_pressed = False
shift_pressed = False
esc_pressed = False

def ft_lock():
    os.system("ft_lock")
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
    pyautogui.click(exit_x, fixed_y, button='left')

def delay_before_lock(minutes):
    countdown(minutes)

def lock_if_mouse_moves():
    while not exit_event.is_set():
        x, y = mouse_position()
        if x != initial_x or y != initial_y:
            pyautogui.click(exit_x, fixed_y, button='left')
            ft_lock()

def on_key_press(key):
    global ctrl_pressed, shift_pressed, esc_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = True
    elif key == keyboard.Key.shift:
        shift_pressed = True
    elif key == keyboard.Key.esc:
        esc_pressed = True
    else:
        pyautogui.click(exit_x, fixed_y, button='left')

    if ctrl_pressed and shift_pressed and esc_pressed:
        os._exit(0)

def on_key_release(key):
    global ctrl_pressed, shift_pressed, esc_pressed

    if key == keyboard.Key.ctrl:
        ctrl_pressed = False
    elif key == keyboard.Key.shift:
        shift_pressed = False
    elif key == keyboard.Key.esc:
        esc_pressed = False

if __name__ == "__main__":
    start_x = 1919
    exit_x = 1111
    fixed_y = 0

    delay_minutes = int(input("Enter the delay in minutes for delay_before_lock: "))
    pyautogui.click(start_x, fixed_y, button='left')

    exit_event = threading.Event()

    move_pointer_thread = threading.Thread(target=delay_before_lock, args=(delay_minutes,))
    move_pointer_thread.start()

    initial_x, initial_y = mouse_starting_position()

    monitor_mouse_thread = threading.Thread(target=lock_if_mouse_moves)
    monitor_mouse_thread.start()

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

    exit_event.set()
    move_pointer_thread.join()
    monitor_mouse_thread.join()
    print("Program exited properly.")
