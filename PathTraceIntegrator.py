from Algebra import RGBColour
from Algebra import BLACK, Vector3D, Cross, Normalize, Length, Dot, local_color, Ray, flip_direction, random_direction, WHITE
from objetos import Objeto, Light, ObjectQuadric
import random
from math import sqrt
from math import pow

nRefractedInitial = 1.33

class PathTraceIntegrator:
    background = BLACK # Cor do Background
    ambient = 0.5

    #Initializer - creates object list
    def __init__(self):
        self.obj_list = []


    #trace light path
    def trace_ray(self, ray, depth):
        difuso = BLACK
        especular = BLACK
        refletido = BLACK
        transmitido = BLACK

        # Checando interseções com cada objeto
        dist = 100
        hit = False
        objeto = 1
        hit_point = Vector3D(0.0, 0.0, 0.0)
        normal = Vector3D(0.0, 0.0, 0.0)

        for obj in self.obj_list:
            inter = obj.intersect(ray)
            tmp_hit = inter[0]
            distance = inter[1]

            if tmp_hit and distance < dist:
                dist = distance
                objeto = obj
                hit = tmp_hit
                hit_point = inter[2]
                normal = inter[3]

        if hit: ## Se o raio bateu no objeto calculamos a cor do ponto
            if isinstance(objeto, Light):
                return objeto.color
            else:
                result = local_color(objeto, normal, ray, self.ambient)
        else:
            return self.background


        # Calculando os Raios Secúndarios
        ktot = obj.kd + obj.ks + obj.kt
        aleatorio = random.random()*ktot


        if depth > 0:
            if aleatorio < obj.kd:                            ## Raio Difuso
                x = random.random()
                y = random.random()
                dir = random_direction(x, y, normal)

                new_ray = Ray(hit_point, Normalize(dir))
                difuso = self.trace_ray(new_ray, depth - 1)
            elif aleatorio < obj.kd + obj.ks:        #         ## Raio especular
                L = Normalize(flip_direction(ray.d))
                N = objeto.normal
                R = (N * (Dot(N, L)) - L) * 2.0

                new_ray = Ray(hit_point, Normalize(R))
                especular = self.trace_ray(new_ray, depth - 1)
            else:                                               ## Raio Transmitido
                L = Normalize(flip_direction(ray.d))
                N = objeto.normal
                if Length(N) != 1:
                    N = Normalize(N)
                cos1 = Dot(N, L)
                refletido = L + (N * (2 * cos1))
                new_rayReflected = Ray(hit_point, Normalize(refletido))
                refletido = self.trace_ray(new_rayReflected, depth - 1)
                if (objeto.kt > 0):
                    delta = 1-((pow(1.33/objeto.kt,2))*(1-(pow(cos1,2))))
                    if (delta >= 0):
                        cos2 = sqrt(delta)

                        divisao = self.nRefractedInitial / objeto.kt
                        self.nRefractedInitial = objeto.kt
                        if (cos1 > 0) :
                            transmitido = (divisao * L) + (((divisao * cos1) - cos2) * N)
                        else:
                            transmitido = (divisao * L) + (((divisao * cos1) + cos2) * N)
                        new_ray = Ray(hit_point, Normalize(transmitido))
                        transmitido = self.trace_ray(new_ray, depth-1)

        return result + difuso * objeto.kd + especular * objeto.ks + refletido + transmitido * objeto.kt
