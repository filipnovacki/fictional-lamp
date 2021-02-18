import OpenGL.GL.shaders
import glfw
import numpy as np
from OpenGL.GL import *

import objects


def main():
    if not glfw.init():
        return

    window = glfw.create_window(720, 600, "Pyopengl Drawing Rectangle", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    obj = objects.draw_rectangle()

    rectangle = obj['vertices']
    rectangle = np.array(rectangle, dtype=np.float32)

    indices = obj['indices']
    indices = np.array(indices, dtype=np.uint32)

    VERTEX_SHADER = """
        #version 300 es
        precision highp float;
        in vec3 position;
        in vec3 color;
        out vec3 newColor;

        void main() {
            gl_Position = vec4(position, 1.0);
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

    # Compile The Program and shaders
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, rectangle.itemsize * len(rectangle), rectangle, GL_STATIC_DRAW)

    # Create EBO
    # Element buffer object
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    # get the position from  shader
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # get the color from  shader
    color = glGetAttribLocation(shader, 'color')
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)
    glClearColor(0.0, 1.0, 0.0, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
