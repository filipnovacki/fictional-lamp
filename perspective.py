import OpenGL.GL.shaders
import glfw
import numpy as np
import pyrr
from OpenGL.GL import *

import objects

_SCREEN_WIDTH = 1366
_SCREEN_HEIGHT = 768

if not glfw.init():
    quit()

window = glfw.create_window(_SCREEN_WIDTH, _SCREEN_HEIGHT, "Pyopengl Drawing Rectangle", None, None)

if not window:
    glfw.terminate()
    quit()

glfw.make_context_current(window)

cube = objects.draw_cube(side_a=0.1, colors=True)
indices = objects._CUBE_INDICES

cube = np.array(cube, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

VERTEX_SHADER = """
#version 300 es
precision highp float;

in vec3 position;
in vec3 color;
out vec3 newColor;

uniform mat4 transform; 

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;


void main() {
    gl_Position = projection * view * model * transform * vec4(position, 1.0f);
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

view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -3.0]))
projection = pyrr.matrix44.create_perspective_projection(45.0, _SCREEN_WIDTH / _SCREEN_HEIGHT, 0.1, 100.0)
model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

view_loc = glGetUniformLocation(shader, "view")
proj_loc = glGetUniformLocation(shader, "projection")
model_loc = glGetUniformLocation(shader, "model")

glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    transformLoc = glGetUniformLocation(shader, "transform")
    glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y)

    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
glfw.terminate()

