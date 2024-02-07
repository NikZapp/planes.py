#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ["PYGLFW_PREVIEW"] = "YES"

from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import sys

# Import all windows
from stack_window import Stack
from mcpi_window import MCPI
from actions_window import Actions

class Application():
    def __init__(self, overlay=True):
        self.overlay = overlay
        imgui.create_context()
        self.window = self.impl_glfw_init()
        self.impl = GlfwRenderer(self.window)

        self.stack = Stack(self)
        self.mcpi = MCPI(self)
        self.actions = Actions(self)
        
    def process(self):
        
        glfw.poll_events()
        self.impl.process_inputs()

        self.mcpi.handle()
        
        imgui.new_frame()

        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.0, 0.0, 0.0, 0.4)
        
        self.stack.render()
        self.mcpi.render()
        self.actions.render()
        #imgui.show_test_window()

        imgui.pop_style_color()
        
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()

        self.impl.render(imgui.get_draw_data())
        #glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)
        glfw.swap_buffers(self.window)

    
    def start(self):
        while not glfw.window_should_close(self.window):
            self.process()
        self.stop()
    
    def stop(self):
        self.impl.shutdown()
        glfw.terminate()

    def impl_glfw_init(self):
        if self.overlay:
            width, height = 1920, 1080
        else:
            width, height = int(1920.0 / 3.0 * 0.9), int(1080.0 * 0.9)

        window_name = "Planes overlay"
        
        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        if self.overlay:
            glfw.window_hint(glfw.RESIZABLE, glfw.FALSE);
            glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
            glfw.window_hint(glfw.FLOATING, glfw.TRUE)
            glfw.window_hint(glfw.DECORATED, glfw.FALSE);
            
            glfw.window_hint(glfw.FOCUSED, glfw.FALSE);
            glfw.window_hint(glfw.FOCUS_ON_SHOW, glfw.FALSE);
            # Mouse passthrough, will be available in glfw 3.4
            # See https://github.com/FlorianRhiem/pyGLFW/issues/53
            # also imgui breaks some stuff with it
            #glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)
            
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        
        # Create a windowed mode window and its OpenGL context
        monitor = None
        if self.overlay:
            pass
            # Temporarily disabled due to the absence of mouse passthrough
            #monitor = glfw.get_primary_monitor()
        window = glfw.create_window(int(width), int(height), window_name, monitor, None)
        glfw.make_context_current(window)
        if self.overlay:
            glfw.maximize_window(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        return window


if __name__ == "__main__":
    if True:#try:
        app = Application(False)
        app.start()
    #except Exception as e:
    #    print(e)
    #    glfw.terminate()
