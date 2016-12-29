#########################################
# ----------------PyPath-----------------#
# Simple Path Tracer Programmed in Python#
# ----------By: Julian Villella----------#
# ------Start Date: August 17, 2011------#
#########################################

# Modules
from math import sqrt

# -------------------------------------------------Vector3D class
class Vector3D:
    # Initializer
    def __init__(self, x_element, y_element, z_element):
        self.x = x_element
        self.y = y_element
        self.z = z_element

    # Operator Overloading
    def __sub__(self, v):
        return Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __add__(self, v):
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __mul__(self, s):
        return Vector3D(self.x * s, self.y * s, self.z * s)

    def __truediv__(self, s):
        return Vector3D(self.x / s, self.y / s, self.z / s)

    def __repr__(self):
        return "Algebra.Vector3D ({}, {}, {})".format(self.x, self.y, self.z)


# Return dot product between two vectors
def Dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


# Return perpendicular vector
def Cross(a, b):
    return Vector3D(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


# Return length of vector
def Length(v):
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z)


# Return normalized vector (unit vector)
def Normalize(v):
    return v * (1.0 / Length(v))

# Return the normal vector from a triangule
def Normal(a, b, c):
    v = b - a
    s = c - a

    # Cross Product - Normal vector
    normal = Cross(v, s)

    # Normalize normal vector
    return Normalize(normal)


# Return normal that is pointing on the side as the passed direction
def orient_normal(normal, direction):
    if Dot(normal, direction) < 0.0:
        return normal * -1.0  # flip normal
    else:
        return normal

def Parallelogram_Area(A, B, P):
    v = B - A
    s = P - A

    cross = Cross(v, s)

    return Dot(v, s)

def local_color(obj, ray, ambient):
    # Iluminação do objeto
    color = obj.color

    # Iluminação ambiente
    ia = ambient * float(obj.ka)
    color = color + (RGBColour(ia, ia, ia))

    # Iluminação difusa
    p1 = Vector3D(0.0, -1.0, 0.0)
    p2 = obj.normal

    if (Length(p1) != 1):
        p1 = Normalize(p1)

    if (Length(obj.normal) != 1):
        p2 = Normalize(obj.normal)

    lv = 1.0 * float(obj.kd) * Dot(p1, p2)

    color = color + (RGBColour(lv, lv, lv))

    # Iluminação especular
    p1 = Vector3D(p1.x * (-1), p1.y, p1.z)
    p2 = ray.o

    if (Length(p1) != 1):
        p1 = Normalize(p1)

    if (Length(ray.o) != 1):
        p2 = Normalize(ray.o)

    lv = 1.0 * float(obj.ks) * pow(Dot(p1, p2), float(obj.n))

    color = color + (RGBColour(lv, lv, lv))

    return color

def tonemapping(pixel):
    pixel.r = pixel.r / (pixel.r + 1)
    pixel.g = pixel.g / (pixel.g + 1)
    pixel.b = pixel.b / (pixel.b + 1)

# -------------------------------------------------Ray class
class Ray:
    # Initializer
    def __init__(self, origin=Vector3D(0.0, 0.0, 0.0),
                 direction=Vector3D(0.0, 0.0, 0.0)):
        self.o = origin
        self.d = direction

    # Member Functions
    def get_hitpoint(self, t):
        return self.o + self.d * t

# -------------------------------------------------RGBColour class
class RGBColour:
    # Initializer
    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    # Operator Overloading
    def __add__(self, c):
        return RGBColour(self.r + c.r, self.g + c.g, self.b + c.b)

    def __sub__(self, c):
        return RGBColour(self.r - c.r, self.g - c.g, self.b - c.b)

    def __mul__(self, s):
        return RGBColour(self.r * s, self.g * s, self.b * s)

    def __truediv__(self, s):
        return RGBColour(self.r / s, self.g / s, self.b / s)

    # this alows us to multipy by another RGBColour
    def multiply(self, c):
        return RGBColour(self.r * c.r, self.g * c.g, self.b * c.b)

    # Member Functions
    def clamp(self, minimum, maximum):
        # red
        if (self.r > maximum): self.r = maximum
        if (self.r < minimum): self.r = minimum
        # green
        if (self.g > maximum): self.g = maximum
        if (self.g < minimum): self.g = minimum
        # blue
        if (self.b > maximum): self.b = maximum
        if (self.b < minimum): self.b = minimum

    def repr(self):
        return "RGBColour ({},{},{})".format(self.r, self.g, self.b)




# Constants
BLACK = RGBColour(0.0, 0.0, 0.0)
WHITE = RGBColour(1.0, 1.0, 1.0)
RED = RGBColour(1.0, 0.0, 0.0)  # for testing
