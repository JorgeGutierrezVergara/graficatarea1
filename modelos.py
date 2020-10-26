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
        gpu_wing_quad = es.toGPUShape(bs.createColorQuad(1, 0.5, 0.5))  # gris oscuro
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
        mono.transform = tr.matmul([tr.scale(0.1, 0.2, 0), tr.translate(-8, -1.6, 0)])
        mono.childs += [body, window_1, window_2, window_3, tail_back, nose, wing]

        transform_mono = sg.SceneGraphNode('chanseyTR')
        transform_mono.childs += [mono]

        self.model = transform_mono
        self.pos = 0 #posicion de la tecla, 1=> acelerando, -1=> desacelerando, 0=>cayendo
        self.a =  0 #indica la aceleración del avión
        self.y =  0 #indica la pos visual del avion (-0.3, 0.9)
        self.vy = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
    
    def modifymodel(self):
        self.model.transform = tr.translate(0, self.y, 0)

    def update(self, dt):
        if self.pos == 1:
            self.a += dt
            if self.a > 0:
                self.a = min(1.6, self.a) 
                self.vy = (abs(self.a)**1.8) * 0.5
                self.y = self.vy

        
        elif self.pos == 0:
            if self.a < 0:
                self.a += dt
                self.y = (abs(self.a)**1.8) * 0.5
            elif self.a > 0:
                self.a -= dt
                self.y = (abs(self.a)**1.8) * 0.5

        elif self.pos ==-1:
            self.a -= dt
            if self.a > 0:
                self.a = min(1.6, self.a)
                self.vy = (abs(self.a)**1.8) * 0.5
                self.y = self.vy
        
        self.modifymodel()
        print(self.y)

    def move_down(self):
        self.pos = -1

    def move_up(self):
        self.pos = 1

    def move_center(self):
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



class HUD_y_vel(object):
    def __init__(self):
        # Figuras básicas
        gpu_tablero_quad   = es.toGPUShape(bs.createColorQuad(0.3, 0.3, 0.3))      # gris
        gpu_quarter_circle = es.toGPUShape(bs.createQuarterCircle())
        gpu_indicator_line = es.toGPUShape(bs.createColorQuad(1.0, 1.0, 1.0))
        gpu_center         = es.toGPUShape(bs.createColorQuad(1,1,1))
        #creamos el tablero
        tablero = sg.SceneGraphNode('tablero')
        tablero.transform = tr.scale(6,0.6,1)
        tablero.childs += [gpu_tablero_quad]
        #creamos un velocimetro uwu
        qvel = sg.SceneGraphNode('qvel')  # cuarto de circulo generico
        qvel.transform = tr.scale(0.25, 0.25, 1)
        qvel.childs += [gpu_quarter_circle]
        q1vel = sg.SceneGraphNode('q1vel')
        q1vel.childs += [qvel]
        q2vel = sg.SceneGraphNode('q2vel')
        q2vel.transform = tr.rotationZ(1.57)
        q2vel.childs += [qvel] 
        q3vel = sg.SceneGraphNode('q3vel')
        q3vel.transform = tr.rotationZ(3.14)
        q3vel.childs += [qvel] 
        q4vel = sg.SceneGraphNode('q4vel')
        q4vel.transform = tr.rotationZ(-1.57)
        q4vel.childs += [qvel]
        #un centro
        centro = sg.SceneGraphNode('centro')
        centro.transform = tr.uniformScale(0.02)
        centro.childs += [gpu_center]
        #hacemos los grados
        raya =  sg.SceneGraphNode('raya')
        raya.childs += [gpu_indicator_line]
        raya1 = sg.SceneGraphNode('raya1')
        raya1.transform = tr.matmul([tr.translate(0,0.21,0), tr.scale(0.005,0.08,1)])
        raya1.childs += [raya]
        raya2 = sg.SceneGraphNode('raya2')
        raya2.transform = tr.matmul([tr.translate(0.206,0,0),tr.rotationZ(1.58), tr.scale(0.005,0.08,1)])
        raya2.childs += [raya]
        raya3 = sg.SceneGraphNode('raya3')
        raya3.transform = tr.matmul([tr.translate(-0.206,0,0),tr.rotationZ(1.58), tr.scale(0.005,0.08,1)])
        raya3.childs += [raya]
        raya4 = sg.SceneGraphNode('raya4')
        raya4.transform = tr.matmul([tr.translate(-0.15,0.15,0),tr.rotationZ(0.5), tr.scale(0.005,0.08,1)])
        raya4.childs += [raya]
        raya5 = sg.SceneGraphNode('raya5')
        raya5.transform = tr.matmul([tr.translate(0.15,0.15,0),tr.rotationZ(-0.5), tr.scale(0.005,0.08,1)])
        raya5.childs += [raya]
        raya6 = sg.SceneGraphNode('raya6')
        raya6.transform = tr.matmul([tr.translate(0.15,-0.15,0),tr.rotationZ(0.5), tr.scale(0.005,0.08,1)])
        raya6.childs += [raya]
        raya7 = sg.SceneGraphNode('raya7')
        raya7.transform = tr.matmul([tr.translate(-0.15,-0.15,0),tr.rotationZ(-0.5), tr.scale(0.005,0.08,1)])
        raya7.childs += [raya]
        # Ensamblamos el mono
        vel = sg.SceneGraphNode('vel')
        vel.transform = tr.matmul([tr.translate(-0.8, -0.7, 0), tr.scale(0.7,1,1)])
        vel.childs += [tablero, q1vel, q2vel, q3vel, q4vel,centro, raya1, raya2, raya3, raya4, raya5,raya6, raya7]
        translate_vel = sg.SceneGraphNode('velTR')
        translate_vel.childs += [vel]

        self.model = vel
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

class Alt(object):
    def __init__(self):
        # Figuras básicas
        gpu_black_back = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpu_blue_mid   = es.toGPUShape(bs.createColorQuad(0, 1, 0.9))
        gpu_white_sq   = es.toGPUShape(bs.createColorQuad(1,1,1))
        #creamos un medidor de revoluciones
        back = sg.SceneGraphNode('back')  # cuarto de circulo generico
        back.transform = tr.scale(0.25, 1, 1)
        back.childs += [gpu_black_back]

        blue = sg.SceneGraphNode('blue')
        blue.transform = tr.scale(0.23,0.98,0)
        blue.childs += [gpu_blue_mid]

        white = sg.SceneGraphNode('white')
        white.transform = tr.scale(0.23,0.18,1)
        white.childs += [gpu_white_sq]

        white1 = sg.SceneGraphNode('white1')
        white1.transform = tr.translate(0,0.4,0)
        white1.childs += [white]

        white2 = sg.SceneGraphNode('white2')
        white2.transform = tr.translate(0,0.2,0)
        white2.childs += [white]

        white3 = sg.SceneGraphNode('white3')
        white3.transform = tr.translate(0,0,0)
        white3.childs += [white]

        white4 = sg.SceneGraphNode('white4')
        white4.transform = tr.translate(0,-0.2,0)
        white4.childs += [white]

        white5 = sg.SceneGraphNode('white5')
        white5.transform = tr.translate(0,-0.4,0)
        white5.childs += [white]
        # Ensamblamos el mono
        alt = sg.SceneGraphNode('alt')
        alt.transform = tr.matmul([tr.translate(-0.53, -0.7, 0),tr.scale(0.35,0.5,1)])
        alt.childs += [back, blue, white1, white2, white3, white4, white5]

        translate_alt = sg.SceneGraphNode('altTR')
        translate_alt.childs += [alt]

        self.model = alt
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

class Cab(object):
    def __init__(self):
        # Figuras básicas
        gpu_black_back = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpu_white_mid   = es.toGPUShape(bs.createColorQuad(1, 1, 1))
        gpu_black_line   = es.toGPUShape(bs.createColorQuad(0,0,0))
        #creamos un medidor de revoluciones
        back = sg.SceneGraphNode('back')  # cuarto de circulo generico
        back.transform = tr.scale(1.25, 1, 1)
        back.childs += [gpu_black_back]

        white = sg.SceneGraphNode('white')
        white.transform = tr.scale(1.23,0.98,0)
        white.childs += [gpu_white_mid]

        line = sg.SceneGraphNode('line')
        line.transform = tr.scale(1.,0.02,0)
        line.childs += [gpu_black_line]

        line1 = sg.SceneGraphNode('line1')
        line1.childs += [line]

        line2 = sg.SceneGraphNode('line2')
        line2.transform = tr.translate(0,0.26,0)
        line2.childs += [line]

        line3 = sg.SceneGraphNode('line3')
        line3.transform = tr.translate(0,-0.26,0)
        line3.childs += [line]

        # Ensamblamos el mono
        cab = sg.SceneGraphNode('cab')
        cab.transform = tr.matmul([tr.translate(0.2, -0.7, 0), tr.uniformScale(0.34)])
        cab.childs += [back, white, line1, line2, line3]

        translate_cab = sg.SceneGraphNode('cabTR')
        translate_cab.childs += [cab]

        self.model = cab
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

class Rev(object):
    def __init__(self):
        # Figuras básicas
        gpu_quarter_circle = es.toGPUShape(bs.createQuarterCircle())
        gpu_indicator_line = es.toGPUShape(bs.createColorQuad(1.0, 1.0, 1.0))
        gpu_center         = es.toGPUShape(bs.createColorQuad(1,1,1))
        #creamos un medidor de revoluciones
        qvel = sg.SceneGraphNode('qvel')  # cuarto de circulo generico
        qvel.transform = tr.scale(0.25, 0.25, 1)
        qvel.childs += [gpu_quarter_circle]
        q1vel = sg.SceneGraphNode('q1vel')
        q1vel.childs += [qvel]
        q2vel = sg.SceneGraphNode('q2vel')
        q2vel.transform = tr.rotationZ(1.57)
        q2vel.childs += [qvel] 
        q3vel = sg.SceneGraphNode('q3vel')
        q3vel.transform = tr.rotationZ(3.14)
        q3vel.childs += [qvel] 
        q4vel = sg.SceneGraphNode('q4vel')
        q4vel.transform = tr.rotationZ(-1.57)
        q4vel.childs += [qvel] 
        #un centro
        centro = sg.SceneGraphNode('centro')
        centro.transform = tr.uniformScale(0.02)
        centro.childs += [gpu_center]
        #hacemos los grados
        raya =  sg.SceneGraphNode('raya')
        raya.childs += [gpu_indicator_line]
        raya1 = sg.SceneGraphNode('raya1')
        raya1.transform = tr.matmul([tr.translate(0,0.21,0), tr.scale(0.005,0.08,1)])
        raya1.childs += [raya]
        raya2 = sg.SceneGraphNode('raya2')
        raya2.transform = tr.matmul([tr.translate(0.206,0,0),tr.rotationZ(1.58), tr.scale(0.005,0.08,1)])
        raya2.childs += [raya]
        raya3 = sg.SceneGraphNode('raya3')
        raya3.transform = tr.matmul([tr.translate(-0.206,0,0),tr.rotationZ(1.58), tr.scale(0.005,0.08,1)])
        raya3.childs += [raya]
        raya4 = sg.SceneGraphNode('raya4')
        raya4.transform = tr.matmul([tr.translate(-0.15,0.15,0),tr.rotationZ(0.5), tr.scale(0.005,0.08,1)])
        raya4.childs += [raya]
        raya5 = sg.SceneGraphNode('raya5')
        raya5.transform = tr.matmul([tr.translate(0.15,0.15,0),tr.rotationZ(-0.5), tr.scale(0.005,0.08,1)])
        raya5.childs += [raya]
        raya6 = sg.SceneGraphNode('raya6')
        raya6.transform = tr.matmul([tr.translate(0.15,-0.15,0),tr.rotationZ(0.5), tr.scale(0.005,0.08,1)])
        raya6.childs += [raya]
        raya7 = sg.SceneGraphNode('raya7')
        raya7.transform = tr.matmul([tr.translate(-0.15,-0.15,0),tr.rotationZ(-0.5), tr.scale(0.005,0.08,1)])
        raya7.childs += [raya]
        # Ensamblamos el mono
        rev = sg.SceneGraphNode('rev')
        rev.transform = tr.matmul([tr.translate(-0.25, -0.7, 0),tr.scale(0.7,1,1)])
        rev.childs += [q1vel, q2vel, q3vel, q4vel,centro, raya1, raya2, raya3, raya4, raya5,raya6, raya7]
        translate_rev = sg.SceneGraphNode('revTR')
        translate_rev.childs += [rev]

        self.model = rev
        self.pos = 0

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')



class Egg(object):
    #creamos una montaña
    def __init__(self):
        gpu_egg = es.toGPUShape(bs.createColorTriangle(0.47, .19, .0))

        #creamos una base y altura aleatoria para las montañas
        base = random.uniform(0.5,3)
        altura = random.uniform(0.5,2)

        egg = sg.SceneGraphNode('egg')
        egg.transform = tr.scale(base, altura, 1)
        egg.childs += [gpu_egg]

        egg_tr = sg.SceneGraphNode('eggTR')
        egg_tr.childs += [egg]

        self.pos_x = 2 # LOGICA
        self.pos_y = -0.2
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
