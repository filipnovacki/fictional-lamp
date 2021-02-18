import OpenGL.GL.shaders
import glfw
import numpy as np
import pyrr
from OpenGL.GL import *

import objects

if not glfw.init():
    quit()

screen_width = 1366
screen_height = 768

window = glfw.create_window(screen_width, screen_height, "Pyopengl Drawing Rectangle", None, None)

if not window:
    glfw.terminate()
    quit()

glfw.make_context_current(window)

cube = objects.draw_cube(side_a=0.1, colors=True)
indices = objects._CUBE_INDICES
print(cube)

cube = np.array(cube, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)
print(indices)

VERTEX_SHADER = """
#version 300 es
precision highp float;

in vec3 position;
in vec3 color;
out vec3 newColor;

uniform mat4 transform; 

void main() {
    gl_Position = transform * vec4(position, 1.0f);
    newColor = color;
}
"""

FRAGMENT_SHADER = """
#version 300 es
precision highp float;

in vec3 newColor;
out vec4 outColor;

void main() {
    outColor = vec4(newColor, 1.0f);
}
"""


shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                          OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(
    GL_ARRAY_BUFFER,
    len(cube)*cube.itemsize,
    cube,
    GL_STATIC_DRAW
)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(
    GL_ELEMENT_ARRAY_BUFFER,
    len(indices)*indices.itemsize,
    indices,
    GL_STATIC_DRAW
)

position = glGetAttribLocation(shader, 'position')
glVertexAttribPointer(
    position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0)
)
glEnableVertexAttribArray(position)

color = glGetAttribLocation(shader, 'color')
glVertexAttribPointer(
    color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12)
)
glEnableVertexAttribArray(color)

glUseProgram(shader)

glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.2 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(np.pi)

    transformLoc = glGetUniformLocation(shader, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y)

    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
glfw.terminate()

