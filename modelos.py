"""
Este archivo generaría todos los modelos que tiene la aplicación. En programas más complicados
tendríamos una cosa así:

src/models/actor/chansey.py
src/models/actor/egg.py
src/models/factory/eggcreator.py

...
Y este archivo sería algo como
src/models/model.py --> sólo importaría los objetos que usa el resto de la aplicación, sin tocar el detalle mismo

from src.models.actor.chansey import Chansey
from src.models.actor.factory import EggCreator
...

Pero aquí, como nuestra app es sencilla, definimos todas las clases aquí mismo.
1. Chansey
2. Los huevos
"""

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from OpenGL.GL import glClearColor
import random
from typing import List


class Chansey(object):

    def __init__(self):
        #creamos el avion

        # Figuras básicas
        gpu_body_quad   = es.toGPUShape(bs.createColorQuad(0.65, 0.65, 0.65))      # gris
        gpu_tail_triangle   = es.toGPUShape(bs.createColorTriangle(0.65, 0.65, 0.65))  # gris
        gpu_nose_triangle   = es.toGPUShape(bs.createColorTriangle(0.65, 0.65, 0.65))  # gris
        gpu_wing_quad = es.toGPUShape(bs.createColorQuad(0.32, 0.32, 0.32))  # gris oscuro
        gpu_window_quad = es.toGPUShape(bs.createColorQuad(0, 1, 0.86))  # celeste

        #creamos el "cuerpo"

        body = sg.SceneGraphNode('body')
        body.transform = tr.scale(2.5,0.7,1)  #alargamos el "cuerpo" del avion
        body.childs += [gpu_body_quad]

        # Creamos las ventanas
        window = sg.SceneGraphNode('window')  # ventana generica
        window.transform = tr.scale(0.25, 0.25, 1)
        window.childs += [gpu_window_quad]

                # prueba dos ventanas
        window_1 = sg.SceneGraphNode('window_1')
        window_1.transform = tr.translate(1, 0.14, 0)  # tr.matmul([])..
        window_1.childs += [window]

        window_2 = sg.SceneGraphNode('window_2')
        window_2.transform = tr.translate(0.65, 0.14, 0)  # tr.matmul([])..
        window_2.childs += [window]

        window_3 = sg.SceneGraphNode('window_3')
        window_3.transform = tr.translate(0.3, 0.14, 0)  # tr.matmul([])..
        window_3.childs += [window]

        # cola
        tail = sg.SceneGraphNode('tail') #ventana generica
        tail.transform = tr.rotationZ(0.46) #dejamos el borde trasero del triangulo ortogonal al cuerpo uwu
        tail.childs += [gpu_tail_triangle]

        tail_back = sg.SceneGraphNode('eyeLeft')
        tail_back.transform = tr.matmul([tr.translate(-1.0092, 0.4, 0), tr.scale(1.1,1.1,0)])
        tail_back.childs += [tail]

        # nariz
        nose = sg.SceneGraphNode('nose') #ventana generica
        nose.transform = tr.matmul([tr.rotationZ(0.465),tr.translate(1.26, -0.55, 0), tr.scale(0.64,0.64,0)])
        nose.childs += [gpu_nose_triangle]

        #ala
        wing = sg.SceneGraphNode('wing')
        wing.transform = tr.matmul([tr.rotationZ(-0.55),tr.translate(0.1, -0.5, 0), tr.scale(0.3,1,0)])
        wing.childs += [gpu_wing_quad]


        # Ensamblamos el mono
        mono = sg.SceneGraphNode('chansey')
        mono.transform = tr.matmul([tr.scale(0.1, 0.2, 0), tr.translate(-8, 2, 0)])
        mono.childs += [body, window_1, window_2, window_3, tail_back, nose, wing]

        transform_mono = sg.SceneGraphNode('chanseyTR')
        transform_mono.childs += [mono]

        self.model = transform_mono
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def move_left(self):
        self.model.transform = tr.translate(0, -0.7, 0)
        self.pos = -1

    def move_right(self):
        self.model.transform = tr.translate(0, 0.7, 0)
        self.pos = 1

    def move_center(self):
        self.model.transform = tr.translate(0, 0, 0)
        self.pos = 0

    def collide(self, eggs: 'EggCreator'):
        if not eggs.on:  # Si el jugador perdió, no detecta colisiones
            return

        deleted_eggs = []
        for e in eggs.eggs:
            if e.pos_y < -0.7 and e.pos_x != self.pos:
                print('MUERE, GIT GUD')  # YOU D   I   E   D, GIT GUD
                """
                En este caso, podríamos hacer alguna pestaña de alerta al usuario,
                cambiar el fondo por alguna textura, o algo así, en este caso lo que hicimos fue
                cambiar el color del fondo de la app por uno rojo.
                """
                eggs.die()  # Básicamente cambia el color del fondo, pero podría ser algo más elaborado, obviamente
            elif -0.25 >= e.pos_y >= -0.7 and self.pos == e.pos_x:
                # print('COLISIONA CON EL HUEVO')
                deleted_eggs.append(e)
        eggs.delete(deleted_eggs)


class HUD(object):

    def __init__(self):
        # Figuras básicas
        gpu_tablero_quad   = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))      # gris

        #creamos el tablero

        tablero = sg.SceneGraphNode('tablero')
        tablero.transform = tr.scale(2,1,1)
        tablero.childs += [gpu_tablero_quad]

        # Ensamblamos el mono
        fondo = sg.SceneGraphNode('hud')
        fondo.transform = tr.translate(0,-0.8,0)
        fondo.childs += [tablero]

        transform_fondo = sg.SceneGraphNode('hudTR')
        transform_fondo.childs += [fondo]

        self.model = transform_fondo
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')



class Egg(object):

    def __init__(self):
        gpu_egg = es.toGPUShape(bs.createColorQuad(0.7, .7, .7))

        egg = sg.SceneGraphNode('egg')
        egg.transform = tr.scale(0.1, 0.2, 1)
        egg.childs += [gpu_egg]

        egg_tr = sg.SceneGraphNode('eggTR')
        egg_tr.childs += [egg]

        self.pos_x = 1
        self.pos_y = 0  # LOGICA
        self.model = egg_tr

    def draw(self, pipeline):
        self.model.transform = tr.translate(0.7 * self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        self.pos_x -= dt


class EggCreator(object):
    eggs: List['Egg']

    def __init__(self):
        self.eggs = []
        self.on = True

    def die(self):  # DARK SOULS
        glClearColor(1, 0, 0, 1.0)  # Cambiamos a rojo
        self.on = False  # Dejamos de generar huevos, si es True es porque el jugador ya perdió

    def create_egg(self):
        if len(self.eggs) >= 10:  # No puede haber un máximo de 10 huevos en pantalla
            return
        if random.random() < 0.001:
            self.eggs.append(Egg())

    def draw(self, pipeline):
        for k in self.eggs:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.eggs:
            k.update(dt)

    def delete(self, d):
        if len(d) == 0:
            return
        remain_eggs = []
        for k in self.eggs:  # Recorro todos los huevos
            if k not in d:  # Si no se elimina, lo añado a la lista de huevos que quedan
                remain_eggs.append(k)
        self.eggs = remain_eggs  # Actualizo la lista
