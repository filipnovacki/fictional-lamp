import OpenGL.GL.shaders
import glfw
import numpy as np
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glGenBuffers, glBindBuffer, GL_ARRAY_BUFFER, glBufferData, \
    GL_STATIC_DRAW, glGetAttribLocation, glVertexAttribPointer, GL_FLOAT, GL_FALSE, glEnableVertexAttribArray, \
    glUseProgram, GL_COLOR_BUFFER_BIT, glClear, GL_TRIANGLE_FAN, glClearColor, glDrawArrays, ctypes, GL_TRIANGLES

import objects

screen_width = 600
screen_height = 600

if not glfw.init():
    quit()

window = glfw.create_window(screen_width, screen_height, "PyOpenGL", None, None)

if not window:
    glfw.terminate()
    quit()

glfw.make_context_current(window)

segments = 100
colors = True
circle = objects.draw_circle(segments=segments, r=1, colors=colors)
circle = np.array(circle, dtype=np.float32)

VERTEX_SHADER = """
#version 300 es
precision highp float;
in vec4 position;
in vec3 color;
out vec3 newColor;
void main() {
    gl_Position = position;
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
    circle.itemsize * len(circle),
    circle,
    GL_STATIC_DRAW
)

position = glGetAttribLocation(shader, 'position')
glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
glEnableVertexAttribArray(position)

color = glGetAttribLocation(shader, 'color')
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(8))
glEnableVertexAttribArray(color)

glUseProgram(shader)
glClearColor(1.0, 1.0, 1.0, 0.0)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(circle))
    glfw.swap_buffers(window)

glfw.terminate()
