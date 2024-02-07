import imgui
import keyboard
import os
import sys
import json
import types

class Actions():
    def __init__(self, app):
        self.app = app
        self.load_actions()
        self.load_keybinds_from_file()
        self.load_keybinds()
        
        self.find_inverse_keybinds()
        self.current_keybind = ""
        self.selected_module = ""
        self.selected_function = ""

    def load_actions(self):
        self.actions = {}
        sys.path.insert(1, "actions")
        for path in os.listdir("actions"):
            try:
                action_container = __import__(path)
                actions = action_container.actions
                if hasattr(action_container, "name"):
                    name = action_container.name
                else:
                    name = path
                self.actions[name] = actions
                if hasattr(action_container, "app"):
                    action_container.app = self.app
                print(f"Loaded {len(actions)} actions from {name}")
            except Exception as e:
                print(f"Failed to import {path}: {e}")

    def save_keybinds_to_file(self):
        with open("keybinds.json", "w") as keybinds:
            json.dump(self.keybinds, keybinds, indent=True)

    def load_keybinds_from_file(self):
        try:
            with open("keybinds.json", "r") as keybinds:
                self.keybinds = json.load(keybinds)
        except Exception as e:
            print("Failed to load keybinds!")
            print(e)
            self.keybinds = {}
    
    def keybind_func_wrapper(self, mcpi, func):
        mcpi.actions_queue.put_nowait(func)
    
    def load_keybinds(self):
        try:
            keyboard.remove_all_hotkeys()
        except Exception as e:
            print(f"Keybind removal failed: {e}")
        for keybind in self.keybinds:
            action = self.keybinds[keybind]
            module = action[0]
            function = action[1]
            try:
                keyboard.add_hotkey(
                    keybind,
                    lambda func=self.actions[module][function] : self.keybind_func_wrapper(self.app.mcpi, func))
            except Exception as e:
                print(f"Failed to load keybind {keybind} : {module}.{function}")
                print(e)

    def find_inverse_keybinds(self):
        self.inverse_keybinds = {}
        for keybind in self.keybinds:
            module_name = self.keybinds[keybind][0]
            function_name = self.keybinds[keybind][1]
            if (module_name, function_name) in self.inverse_keybinds:
                self.inverse_keybinds[(module_name, function_name)].append(keybind)
            else:
                self.inverse_keybinds[(module_name, function_name)] = [keybind]
    
    def render(self):
        imgui.begin("Actions")

        if imgui.button("Add keybind"):
            self.keybinds[self.current_keybind] = [self.selected_module, self.selected_function]
            self.find_inverse_keybinds()
            self.load_keybinds()

        imgui.same_line()

        if imgui.button("Remove keybinds"):
            found_keybind = None
            for keybind in self.keybinds:
                module = self.keybinds[keybind][0]
                func = self.keybinds[keybind][1]
                if (module == self.selected_module and func == self.selected_function):
                    self.keybinds.pop(keybind, None)
            self.load_keybinds()
            self.find_inverse_keybinds()
                
        _, self.current_keybind = imgui.input_text_with_hint("", "Keybind", self.current_keybind)

        if imgui.button("Save keybinds"):
            self.save_keybinds_to_file()
            
        imgui.same_line()
        
        if imgui.button("Reload actions"):
            self.load_actions()

        imgui.separator()

        for name in self.actions:
            show, _ = imgui.collapsing_header(name)
            if show:
                for action_name in self.actions[name]:
                    saved_x = imgui.get_cursor_pos_x()
                    clicked, _ = imgui.selectable(
                        f"##{name}.{action_name}",
                        (self.selected_module == name and
                         self.selected_function == action_name))
                    imgui.same_line()
                    imgui.set_cursor_pos_x(saved_x)
                    imgui.text(action_name)
                    if (name, action_name) in self.inverse_keybinds:
                        imgui.same_line()
                        imgui.text_disabled(" ".join(self.inverse_keybinds[(name, action_name)]))
                    
                    if clicked:
                        self.selected_module = name
                        self.selected_function = action_name
            else:
                imgui.same_line(0.0, 10.0)
                imgui.text_disabled(f"({len(self.actions[name])})")
        imgui.end()

    def handle(self):
        pass
