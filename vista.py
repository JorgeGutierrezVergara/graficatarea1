"""
Esta sería la clase vista. Contiene el ciclo de la aplicación y ensambla
las llamadas para obtener el dibujo de la escena.
"""

import glfw
from OpenGL.GL import *
import sys

from modelos import *
from controller import Controller

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1200
    height = 650

    window = glfw.create_window(width, height, 'Chansey E P I C', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.34, 0.7, 1, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # HACEMOS LOS OBJETOS
    chansey = Chansey()
    HUD = HUD_y_vel()
    eggs = EggCreator()
    nube = NubeCreator()
    rev = Rev()
    alt = Alt()
    cab = Cab()
    bot = Boton()

    controlador.set_model(chansey)
    controlador.set_eggs(eggs)
    controlador.set_nube(nube)

    t0 = 0

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input

        # Calculamos el dt
        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti


        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        eggs.create_egg()  # Aleatorio
        eggs.update(0.5 * dt)  # 0.001
        nube.create_nube()  # Aleatorio
        nube.update(0.5 * dt)
        chansey.update(dt)

        # Reconocer la logica
        chansey.collide(eggs)  # ---> RECORRER TODOS LOS HUEVOS

        # DIBUJAR LOS MODELOS
        nube.draw(pipeline)
        chansey.draw(pipeline)
        eggs.draw(pipeline)
        HUD.draw(pipeline)
        rev.draw(pipeline)
        alt.draw(pipeline)
        cab.draw(pipeline)
        bot.draw(pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
