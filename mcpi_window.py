from mcpi import minecraft
import imgui
import queue
import keyboard

class MCPI():
    def __init__(self, app):
        self.app = app
        self.attempt_connection()
        self.extended = True
        self.handle_input = True
        self.actions_queue = queue.Queue()
        
    def attempt_connection(self):
        try:
            self.mc = minecraft.Minecraft.create()
            self.mc.conn.drain()
            self.connected = True
        except ConnectionRefusedError:
            self.connected = False
    
    def render(self):
        imgui.begin("MCPI connection")
        if imgui.button("Connect"):
            self.attempt_connection()
        imgui.same_line()
        if self.connected:
            imgui.text_colored("Connected", 0.0, 1.0, 0.0)
        else:
            imgui.text_colored("Not connected", 1.0, 0.0, 0.0)
            
        if self.connected:
            _, self.extended = imgui.checkbox("Extended API", self.extended)
            _, self.handle_input = imgui.checkbox("Push hits onto stack", self.handle_input)

        imgui.text_wrapped("Press B to convert to a block automatically")
        imgui.end()

    def handle(self):
        self.handle_stack_input(self.app.stack)
        self.handle_actions()
        
    def handle_stack_input(self, stack):
        if not self.connected:
            return

        try:
            hits = self.mc.events.pollBlockHits()
        except:
            self.connected = False
            return
        
        for hit in hits:
            if self.handle_input:
                if keyboard.is_key_pressed('b'):
                    stack.push(self.mc.getBlockWithData(hit.pos))
                else:
                    stack.push(hit.pos)

    def handle_actions(self):
        while not self.actions_queue.empty():
            action = self.actions_queue.get_nowait()
            try:
                action()
            except Exception as e:
                print("Error during action handling:", e)
