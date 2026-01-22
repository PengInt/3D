import sys

import json
import math, pygame
import pathlib
import pygame as system
from termcolor import colored as c
import numpy as np

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @property
    def pos(self):
        return [self.x, self.y, self.z]
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    def __pow__(self, b):
        if isinstance(b, Vector3):
            return self.x*b.x + self.y*b.y + self.z*b.z
        else:
            return NotImplemented
    '''def __mod__(self, b):    # cross product
        if isinstance(b, Vector3):
            return Vector3(self.x*b.x, self.y*b.y, self.z*b.z)
        else:
            return NotImplemented'''
    def __add__(self, b):
        if isinstance(b, Vector3):
            return Vector3(self.x+b.x, self.y+b.y, self.z+b.z)
        else:
            return NotImplemented
    def __radd__(self, a):
        return self.__add__(a)
    def __mul__(self, b):
        if isinstance(b, int) or isinstance(b, float):
            return Vector3(self.x*b, self.y*b, self.z*b)
        elif isinstance(b, Vector3):
            return Vector3((self.y*b.z-self.z*b.y), (self.z*b.x-self.x*b.z), (self.x*b.y-self.y*b.x))
        else:
            return NotImplemented
    def __rmul__(self, a):
        return self.__mul__(a)
    def __sub__(self, b):
        return self.__add__(-b)
    def __rsub__(self, a):
        return -self.__sub__(a)
    def __truediv__(self, b):
        if isinstance(b, Vector3):
            return self.__mul__(Vector3(1/b.x, 1/b.y, 1/b.z))
        elif isinstance(b, float|int):
            return self.__mul__(1/b)
        else:
            return NotImplemented
    def __rtruediv__(self, a):
        temp = self.__truediv__(a)
        return Vector3(1/temp.x, 1/temp.y, 1/temp.z)
    def __eq__(self, b):
        if isinstance(b, Vector3):
            return self.x == b.x and self.y == b.y and self.z == b.z
        else:
            return NotImplemented
    def __str__(self):
        return f'({self.x:.2f}, {self.y:.2f}, {self.z:.2f})'
    def __irshift__(self, b):
        return NotImplemented
    def __abs__(self):
        return Vector3(math.fabs(self.x), math.fabs(self.y), math.fabs(self.z))
    @classmethod
    def dist(cls, a, b):
        dp = abs(Vector3(a.x - b.x, a.y - b.y, a.z - b.z))
        return (dp.x**2 + dp.y**2 + dp.z**2)**0.5
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    @classmethod
    def getLowest(cls, points):
        lp = None
        for p in points:
            if lp == None:
                lp = p
            else:
                if lp.y > p.y:
                    lp = p
        return lp

    @classmethod
    def getHighest(cls, points):
        hp = None
        for p in points:
            if hp == None:
                hp = p
            else:
                if hp.y < p.y:
                    hp = p
        return hp


class Quaternion:
    def __init__(self, a: float|int, v: Vector3):
        self.w = a
        self.a = a
        self.v = v
    @property
    def x(self):
        return self.v.x
    @property
    def y(self):
        return self.v.y
    @property
    def z(self):
        return self.v.z

# (a1, **v1**) * (a2, **v2**) = (a1a2 - **v1**•**v2**, a1**v2** + a2**v1** + **v1**×**v2**)
    def __mul__(self, b):
        if isinstance(b, Quaternion):
            return Quaternion(
                self.a*b.a - self.v ** b.v,
                self.a * b.v + b.a * self.v + self.v * b.v
            )
        else:
            return NotImplemented
    def __neg__(self):
        return Quaternion(-self.a, -self.v)
    @property
    def conjugate(self):
        return Quaternion(self.a, -self.v)
    def __str__(self):
        return f'{self.w:.2f} + {self.x:.2f}i + {self.y:.2f}j + {self.z:.2f}k'
    @property
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

def tempRot(self, b: tuple[Vector3, Quaternion]):
    if isinstance(b, tuple):
        referencePoint = b[0]
        rotationQuaternion = b[1]

        deltaX = self.x-referencePoint.x
        deltaY = self.y-referencePoint.y
        deltaZ = self.z-referencePoint.z
        deltaPoint = Vector3(deltaX, deltaY, deltaZ)
        quaternionDeltaPoint = Quaternion(0, deltaPoint)

        magnitude = rotationQuaternion.magnitude # magnitude

        unitQuaternionX = rotationQuaternion.x / magnitude
        unitQuaternionY = rotationQuaternion.y / magnitude
        unitQuaternionZ = rotationQuaternion.z / magnitude
        unitVector = Vector3(unitQuaternionX, unitQuaternionY, unitQuaternionZ)

        halfAngle = rotationQuaternion.a/2

        unitQuaternion = Quaternion(
            math.cos(halfAngle),
            math.sin(halfAngle) * unitVector
        )
        unitQuaternionConjugate = unitQuaternion.conjugate # inversing the unit quaternion

        #print('\nUnit Quaternion Conjugate (q-1)       ', unitQuaternionConjugate)
        #print('Unit Quaternion (q)                   ', unitQuaternion)
        #print('Quaternion Point to Rotate (p)        ', quaternionDeltaPoint)
        #print('Currently using formula (q-1)pq\n')

        newQuaternion = unitQuaternionConjugate * quaternionDeltaPoint * unitQuaternion # new quaternion

        #print(newQuaternion)

        self.x = newQuaternion.x + referencePoint.x
        self.y = newQuaternion.y + referencePoint.y
        self.z = newQuaternion.z + referencePoint.z
        self.x = round(self.x, 15)
        self.y = round(self.y, 15)
        self.z = round(self.z, 15)
        if int(self.x) == self.x:
            self.x = int(self.x)
        if int(self.y) == self.y:
            self.y = int(self.y)
        if int(self.z) == self.z:
            self.z = int(self.z)
        return self
    else:
        return NotImplemented
Vector3.__irshift__ = tempRot

class Line:
    def __init__(self, v1: Vector3, v2: Vector3):
        self.v = [v1, v2]
    @property
    def length(self):
        return Vector3.dist(self.v[0], self.v[1])
    @property
    def pos(self):
        return (self.v[0] + self.v[1])/2
    def __ge__(self, v: Vector3):
        self.v[0] += v
        self.v[1] += v
    def __irshift__(self, b: Quaternion|tuple[Quaternion, Vector3]):
        if isinstance(b, Quaternion):
            q = b
            r = self.pos
        elif isinstance(b, tuple):
            q = b[0]
            r = b[1]
        else:
            return NotImplemented

        for v in self.v:
            v >>= (r, q)
        return self
    
class Triangle:
    def __init__(self, v1, v2, v3):
        self.v = [v1, v2, v3]
    @property
    def pos(self):
        return (self.v[0] + self.v[1] + self.v[2])/3
    @property
    def surfaceArea(self):
        ab = self.v[0]-self.v[1]
        bc = self.v[1]-self.v[2]
        a = abs(ab * bc)
        return ((a.x**2 + a.y**2 + a.z**2)**0.5) / 2
    @property
    def verticalSurfaceArea(self):
        x = []
        z = []
        for v in self.v:
            x.append(v.x)
            z.append(v.z)
        return abs(x[0] * (z[1] - z[2]) + x[1] * (z[2] - z[0]) + x[2] * (z[0] - z[1])) / 2
    def lighting(self, camPos):
        up = True
        l = Vector3.getLowest(self.v)
        h = Vector3.getHighest(self.v)
        if Vector3.dist(h, camPos) > Vector3.dist(l, camPos):
            da = math.atan2(h.y, Vector3.dist(h, camPos)) - math.atan2(l.y, Vector3.dist(l, camPos))
            if da < 0 and l.y > 0 and h.y > 0:
                up = False
            else:
                up = True
        else:
            da = math.atan2(l.y, Vector3.dist(l, camPos)) - math.atan2(h.y, Vector3.dist(h, camPos))
            if da > 0 and l.y < 0 and h.y < 0:
                up = True
            else:
                up = False
        if up:
            return self.verticalSurfaceArea / self.surfaceArea
        return 0
    def __irshift__(self, b: Quaternion|tuple[Quaternion, Vector3]):
        if isinstance(b, Quaternion):
            q = b
            r = self.pos
        elif isinstance(b, tuple):
            q = b[0]
            r = b[1]
        else:
            return NotImplemented

        for v in self.v:
            v >>= (r, q)
        return self

class GameObject:
    heierarchy = {}
    def __init__(self, v: tuple[Vector3], l: tuple[tuple[int, int]]|list[tuple[int, int]|tuple[list[int]]|list[list[int]]], t: tuple[tuple[int, int, int]]|list[tuple[int, int, int]]|tuple[list[int]]|list[list[int]], pos=Vector3(0, 0, 0), **kwargs):
        self.pos = pos
        self.v = v
        self.l = []
        self.t = []
        for i in l:
            self.l.append(Line(self.v[i[0]], self.v[i[1]]))
        for i in t:
            self.t.append(Triangle(self.v[i[0]], self.v[i[1]], self.v[i[2]]))
        self.name = kwargs.pop('name', 0)
        print(self.name)
        if self.name == 0:
            self.name = 'GameObject'
            n = 0
            while self.name in Renderer.renderers:
                n += 1
                self.name = f'GameObject {n}'
            GameObject.heierarchy[self.name] = self
        else:
            startingName = self.name
            n = 0
            while self.name in GameObject.heierarchy:
                n += 1
                self.name = f'{startingName} {n}'
            GameObject.heierarchy[self.name] = self
    def getSortedTriangles(self, rPos: Vector3):
        sortedTriangles = []
        for t in self.t:
            sortedTriangles.append(t)
        sortedTriangles.sort(
            key=lambda t: Vector3.dist(rPos, t.pos),
            reverse=True
        )

        return sortedTriangles

    @classmethod
    def fromJSON(cls, file: pathlib.Path, name=0):
        JSON = json.load(open(file))
        if name == 0:
            name = JSON['object_name']
        vertices = []
        for v in JSON['vertices']:
            vertices.append(Vector3(v['position'][0], v['position'][1], v['position'][2]))
        lines = []
        for l in JSON['edges']:
            lines.append(l['vertices_indices'])
        triangles = []
        for f in JSON['faces']:
            if len(f['vertices_indices']) == 3:
                triangles.append(f['vertices_indices'])
            elif len(f['vertices_indices']) == 4:
                triangles.append(f['vertices_indices'][:3])
                triangles.append(f['vertices_indices'][1:])
        return GameObject(vertices, lines, triangles, Vector3(0, 0, 0), name=name)


    def __irshift__(self, b: Quaternion|tuple[Quaternion, Vector3]):
        if isinstance(b, Quaternion):
            q = b
            r = self.pos
        elif isinstance(b, tuple):
            q = b[0]
            r = b[1]
        else:
            return NotImplemented

        for v in self.v:
            v >>= (r, q)
        self.pos >>= (r, q)
        return self
    def __ge__(self, b: Vector3):
        if (isinstance(b, Vector3)):
            self.pos += b
            for v in range(len(self.v)):
                self.v[v] += b
            return True
        else:
            return NotImplemented

class Camera:
    def __init__(self, **kwargs):
        self.fov = kwargs.pop('fov', None)
        if self.fov is None:
            self.fov = 90
        self.pos = kwargs.pop('pos', None)
        if self.pos is None:
            self.pos = Vector3(0, 0, -5)
        self.rot = kwargs.pop('rot', None)
        if self.rot is None:
            self.rot = Quaternion(0, Vector3(0, 0, 0))

    def __str__(self):
        return 'Camera Object'

pygame.init()
print('\033c', end='')
class Renderer:
    renderers = {}
    def __init__(self, **kwargs):
        '''
        **kwargs (default):
         - fov (90)
         - camera (Camera())
         - surfaceSize ((400, 400))
         - vsync (1)
         - surface (pygame.display.set_mode(surfaceSize, vsync))
        '''
        self.fov = kwargs.pop('fov', None)
        if self.fov is None:
            self.fov = 90
        self.camera = kwargs.pop('camera', None)
        if self.camera is None:
            self.camera = Camera()
        self.surfaceSize = kwargs.pop('surfaceSize', None)
        if self.surfaceSize is None:
            self.surfaceSize = (400, 400)
        self.vsync = kwargs.pop('vsync', None)
        if self.vsync is None:
            self.vsync = 1
        self.surface = kwargs.pop('surface', None)
        if self.surface is None:
            self.surface = pygame.display.set_mode(self.surfaceSize, vsync=self.vsync)
            pygame.display.set_icon(pygame.image.load('Icon.png'))
            pygame.display.set_caption('Renderer')
        self.name = kwargs.pop('Name', 0)
        if self.name == 0:
            self.name = 'Renderer'
            n = 0
            while self.name in Renderer.renderers:
                n += 1
                self.name = f'Renderer {n}'
            Renderer.renderers[self.name] = self
        
        print(c('  -> New Renderer', (0, 255, 255)))
    def __str__(self):
        result = ''
        for attr in self.__dict__:
            if attr != 'zBuffer':
                result += f'    {c(attr, (0, 255, 0))} {" "*math.floor((7.5-len(attr))%2)}{". "*math.floor(7.5-len(attr)/2)}. . . {c(self.__dict__[attr], (0, 0, 255))}\n'
        return result
    def render(self):
        camPos = self.camera.pos
        self.surface.fill((0, 0, 0))
        for obj in GameObject.heierarchy:
            maxY = -1000000
            minY = 1000000
            for t in GameObject.heierarchy[obj].t:
                if t.pos.y > maxY: maxY = t.pos.y
                elif t.pos.y < minY: minY = t.pos.y
            for t in GameObject.heierarchy[obj].getSortedTriangles(self.camera.pos):
                dx1 = t.v[0].x-camPos.x
                dx2 = t.v[1].x-camPos.x
                dx3 = t.v[2].x-camPos.x

                dy1 = t.v[0].y-camPos.y
                dy2 = t.v[1].y-camPos.y
                dy3 = t.v[2].y-camPos.y

                dz1 = t.v[0].z-camPos.z
                dz2 = t.v[1].z-camPos.z
                dz3 = t.v[2].z-camPos.z

                y1 = dy1/dz1
                y2 = dy2/dz2
                y3 = dy3/dz3

                x1 = dx1 / dz1
                x2 = dx2 / dz2
                x3 = dx3 / dz3

                c = (t.lighting(self.camera.pos) * 3/4 + 0.25) * 255

                pygame.draw.polygon(self.surface, (c, c, c),
                                    ((x1*self.surface.get_height()+self.surface.get_height()*0.5, -y1*self.surface.get_height()+self.surface.get_height()*0.5),
                                            (x2*self.surface.get_height()+self.surface.get_height()*0.5, -y2*self.surface.get_height()+self.surface.get_height()*0.5),
                                            (x3*self.surface.get_height()+self.surface.get_height()*0.5, -y3*self.surface.get_height()+self.surface.get_height()*0.5)
                                           ))
        pygame.display.update()


print(c('Welcom from GameEngine!\n', (153, 255, 102)))


Renderer()
print(Renderer.renderers['Renderer'])
