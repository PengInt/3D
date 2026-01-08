import math, pygame
import pygame as system
from termcolor import colored as c


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
    def __gt__(self, b):
        return NotImplemented
    def __abs__(self):
        return Vector3(math.fabs(self.x), math.fabs(self.y), math.fabs(self.z))
    @classmethod
    def dist(cls, a, b):
        dp = abs(Vector3(a.x - b.x, a.y - b.y, a.z - b.z))
        return (dp.x**2 + dp.y**2 + dp.z**2)**0.5


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

            print('\nUnit Quaternion Conjugate (q-1)       ', unitQuaternionConjugate)
            print('Unit Quaternion (q)                   ', unitQuaternion)
            print('Quaternion Point to Rotate (p)        ', quaternionDeltaPoint)
            print('Currently using formula (q-1)pq\n')
            
            newQuaternion = unitQuaternionConjugate * quaternionDeltaPoint * unitQuaternion # new quaternion

            print(newQuaternion)
            
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
            return True
        else:
            return NotImplemented
Vector3.__gt__ = tempRot

class Line:
    def __init__(self, v1: Vector3, v2: Vector3):
        self.v = [v1, v2]
    @property
    def length(self):
        return Vector3.dist(self.v[0], self.v[1])
    def __ge__(self, v: Vector3):
        self.v[0] += v
        self.v[1] += v
    def __gt__(self, b: Quaternion|tuple[Quaternion, Vector3]):
       if isinstance(b, Quaternion):
           q = b
           r = (self.v[0] + self.v[1])/2
       elif isinstance(b, tuple):
           q = b[0]
           r = b[1]
       else:
           return NotImplemented

       for v in self.v:
           v > (r, q)
       return True
    

class GameObject:
    heierarchy = {}
    def __init__(self, v: tuple[Vector3], l: tuple[tuple[int, int]], pos=Vector3(0, 0, 0), **kwargs):
        self.pos = pos
        self.v = v
        self.l = []
        for i in l:
            self.l.append(Line(self.v[i[0]], self.v[i[1]]))
        self.name = kwargs.pop('Name', 0)
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

    def __gt__(self, b: Quaternion|tuple[Quaternion, Vector3]):
        if isinstance(b, Quaternion):
            q = b
            r = self.pos
        elif isinstance(b, tuple):
            q = b[0]
            r = b[1]
        else:
            return NotImplemented

        for v in self.v:
            v > (r, q)
        self.pos > (r, q)
        return True

class Camera:
    def __init__(self, **kwargs):
        self.fov = kwargs.pop('fov', None)
        if self.fov is None:
            self.fov = 90
        self.pos = kwargs.pop('pos', None)
        if self.pos is None:
            self.pos = Vector3(0, 0, 5)
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
            result += f'    {c(attr, (0, 255, 0))} {" "*math.floor((7.5-len(attr))%2)}{". "*math.floor(7.5-len(attr)/2)}. . . {c(self.__dict__[attr], (0, 0, 255))}\n'
        return result
    def render(self):
        camPos = self.camera.pos
        self.surface.fill((0, 0, 0))
        for obj in GameObject.heierarchy:
            for l in GameObject.heierarchy[obj].l:
                dx1 = l.v[0].x-camPos.x
                dx2 = l.v[1].x-camPos.x

                dy1 = l.v[0].y-camPos.y
                dy2 = l.v[1].y-camPos.y

                dz1 = l.v[0].z-camPos.z
                dz2 = l.v[1].z-camPos.z

                y1 = dy1/dz1
                y2 = dy2/dz2

                x1 = dx1 / dz1
                x2 = dx2 / dz2

                pygame.draw.line(self.surface, (255, 255, 255), (x1*self.surface.get_height()+self.surface.get_height()*0.5, -y1*self.surface.get_height()+self.surface.get_height()*0.5), (x2*self.surface.get_height()+self.surface.get_height()*0.5, -y2*self.surface.get_height()+self.surface.get_height()*0.5), 3)
        pygame.display.update()


print(c('Welcom from GameEngine!\n', (153, 255, 102)))


Renderer()
print(Renderer.renderers['Renderer'])

point = Vector3(2, 3, 1)
print(point)
point > (Vector3(0, 0, 0), Quaternion(math.pi/4, Vector3(0, 1, 0)))
print(point)
