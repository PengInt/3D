import math, pygame


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @property
    def pos(self):
        return [self.x, self.y, self.z]

class Quaternion:
    def __init__(self, a, v: Vector3):
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
    @classmethod
    def mult(cls, a, b):
        return Quaternion(a.a*b.a)

class Camera:
    def __init__(self, **kwargs):
        fov = 90
        pos = Vector3(0, 2, 5)
        rot = ()

        for key, val in kwargs.items():
            locals()[key] = val

class Renderer:
    def __init__(self, **kwargs):
        fov = 90
        camera = Camera()

        for key, val in kwargs.items():
            locals()[key] = val

        self.fov = fov
        self.camera = camera