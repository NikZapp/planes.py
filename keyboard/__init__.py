from pynput import keyboard

hotkeys = {}
hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
hotkey_listener.daemon = True
hotkey_listener.start()

key_aliases = {
    "back" : 65288,
    "bksp" : 65288,
    "backspace" : 65288,
    "<b>" : 65288,
    "up" : 65362,
    "down" : 65364,
    "left" : 65361,
    "right" : 65363
}

def parse_hotkey(line):
    keys = line.split("+")
    actual_keys = []
    for key in keys:
        if len(key) <= 1:
            actual_keys.append(key)
        elif key in key_aliases:
            actual_keys.append(f"<{key_aliases[key]}>")
        elif key in ["plus", ""]:
            actual_keys.append("=")
        elif key[0] == "<":
            actual_keys.append(key)
        else:
            actual_keys.append(f"<{key}>")
    return "+".join(actual_keys)

def remove_all_hotkeys():
    global hotkeys
    hotkeys = {}
    restart_hotkey_listener()
    
def restart_hotkey_listener():
    global hotkeys
    global hotkey_listener
    hotkey_listener.stop()
    hotkey_listener.join()
    hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
    hotkey_listener.start()
    
def add_hotkey(hotkey, func):
    global hotkeys
    hotkeys[parse_hotkey(hotkey)] = func
    restart_hotkey_listener()

pressed_keys = {}
def on_press(key):
    global pressed_keys
    pressed_keys[key] = True

def on_release(key):
    global pressed_keys
    pressed_keys[key] = False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.daemon = True
listener.start()

def is_key_pressed(key):
    global pressed_keys
    keycode = keyboard.KeyCode(char=key)
    if keycode in pressed_keys:
        return pressed_keys[keycode]
    return False

