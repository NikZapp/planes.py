from mcpi.vec3 import Vec3
from mcpi import minecraft

name = "Builtin"
# if an app variable exists, it will be set.
app = None

def echo():
    message = app.stack.pop()
    app.mcpi.mc.postToChat(message)

def remove():
    app.stack.pop()
    
def to_block():
    pos = app.stack.pop()
    if type(pos) != Vec3:
        app.stack.push(pos)
        return
    app.mcpi.attempt_connection()
    app.stack.push(app.mcpi.mc.getBlockWithData(pos))
    
def fill():
    block, pos1, pos2 = app.stack.pop(3)
    if type(pos1) != Vec3:
        block, pos1 = pos1, block
    if type(pos2) != Vec3:
        block, pos2 = pos2, block
    app.mcpi.mc.setBlocks(pos1, pos2, block)
    
def duplicate():
    value = app.stack.pop()
    app.stack.push(value)
    app.stack.push(value)

def place():
    block, positions = app.stack.pop(2)
    if type(block) == list:
        block, positions = positions, block
    if type(positions) != list:
        positions = [positions]
    for pos in positions:
        app.mcpi.mc.setBlock(pos, block)

def cycle():
    a, b, c = app.stack.pop(3)
    app.stack.push(b)
    app.stack.push(a)
    app.stack.push(c)
    
def swap():
    a, b = app.stack.pop(2)
    app.stack.push(a)
    app.stack.push(b)
    
actions = {
    "Remove" : remove,
    "Echo" : echo,
    "Duplicate" : duplicate,
    "Swap top" : swap,
    "Cycle (3)" : cycle,
    "Pos to block" : to_block,
    "Place" : place,
    "Fill" : fill
}
