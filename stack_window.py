import imgui
import glfw
import time

class Stack():
    def __init__(self, app):
        self.highlight = True
        self.items = []
        self.selected_item = -1
        self.last_pop_time = {}
        self.last_push_time = {}
        self.highlight_duration = 0.5
        
    def render(self):
        imgui.begin("Stack")
        _, self.highlight = imgui.checkbox("Highlight edits", self.highlight)
        if self.highlight:
            _, self.highlight_duration = imgui.slider_float("Duration", self.highlight_duration, 0.1, 5.0)
        imgui.separator()
        self.render_stack()
        imgui.end()

    def render_stack(self):
        for n in range(len(self.items) + 6):
            if n < len(self.items):
                text = str(self.items[n])
            else:
                text = ''
            imgui.push_style_color(imgui.COLOR_HEADER, *self.get_color(n))
            clicked, _ = imgui.selectable(text, True)#(self.selected_item == n))
            imgui.pop_style_color()
            if clicked:
                self.selected_item = n

    def push(self, item):
        self.items.append(item)
        self.last_push_time[len(self.items) - 1] = time.perf_counter()

    def pop(self, n=1):
        if n != 1:
            values = []
            for i in range(n):
                if len(self.items) == 0:
                    values.append(None)
                else:
                    values.append(self.items.pop())
                self.last_pop_time[len(self.items)] = time.perf_counter()
            return tuple(values)
        self.last_pop_time[len(self.items) - 1] = time.perf_counter()
        if len(self.items) == 0:
            return None
        return self.items.pop()
    
    def handle(self):
        pass

    def get_color(self, n):
        current = time.perf_counter()
        if n not in self.last_pop_time:
            self.last_pop_time[n] = 0
        if n not in self.last_push_time:
            self.last_push_time[n] = 0
        red = max(0.0, 1.0 - ((current - self.last_pop_time[n]) / self.highlight_duration))
        green = max(0.0, 1.0 - ((current - self.last_push_time[n]) /self.highlight_duration))
        blue = 0.0
        alpha = max(red, green) * 0.5
        return red, green, blue, alpha
        
