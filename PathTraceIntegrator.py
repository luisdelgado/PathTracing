from Algebra import RGBColour
from Algebra import BLACK, Vector3D, Cross, Normalize, Length, Dot, local_color, Ray, flip_direction, random_direction, WHITE
from objetos import Objeto, Light, ObjectQuadric
import random
from math import sqrt
from math import pow

class PathTraceIntegrator:
    background = BLACK # Cor do Background
    ambient = 0.5

    #Initializer - creates object list
    def __init__(self):
        self.obj_list = []


    #trace light path
    def trace_ray(self, ray, depth, nRefractedInitial):
        difuso = BLACK
        especular = BLACK
        refletido = BLACK
        transmitido = BLACK
        self.nRefractedInitial = nRefractedInitial
        temLuz = 0

        # Checando interseções com cada objeto
        dist = 100
        dist2 = 100
        hit = False
        hit2 = False
        objeto = 1
        hit_point = Vector3D(0.0, 0.0, 0.0)
        hit_point2 = Vector3D(0.0, 0.0, 0.0)
        normal = Vector3D(0.0, 0.0, 0.0)
        normal2 = Vector3D(0.0, 0.0, 0.0)
        objeto2 = 0.0

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
                #dir2 = Normalize(dir)

                # shadow ray
                shadow_ray = Ray(Vector3D(dir.x, dir.y, dir.z), Normalize(Vector3D(0.0000, 3.8360, -24.9060)))
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2 and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        hit_point2 = inter2[2]
                        normal2 = inter2[3]
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz==0:
                    if objeto2.kt == 0.0:
                        difuso = BLACK
                    else:
                        new_ray = Ray(hit_point, Normalize(dir))
                        difuso = self.trace_ray(new_ray, depth - 1, objeto.kt)
                        #difuso = difuso * objeto2.kt
                else:
                    new_ray = Ray(hit_point, Normalize(dir))
                    difuso = self.trace_ray(new_ray, depth - 1, objeto.kt)
            elif aleatorio < obj.kd + obj.ks:        #         ## Raio especular
                L = Normalize(flip_direction(ray.d))
                N = objeto.normal
                R = (N * (Dot(N, L)) - L) * 2.0
                #R2 = Normalize(R)

                # shadow ray
                shadow_ray = Ray(Vector3D(R.x, R.y, R.z), Normalize(Vector3D(0.0000, 3.8360, -24.9060)))
                for obj2 in self.obj_list:
                    inter2 = obj2.intersect(shadow_ray)
                    tmp_hit2 = inter2[0]
                    distance2 = inter2[1]

                    if tmp_hit2  and distance2 < dist2:
                        dist2 = distance2
                        objeto2 = obj2
                        hit2 = tmp_hit2
                        hit_point2 = inter2[2]
                        normal2 = inter2[3]
                        temLuz = 0
                        if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                            if isinstance(objeto2, Light):
                                temLuz = 1

                if temLuz == 0.0:
                    if objeto2.kt == 0:
                        especular = BLACK
                    else:
                        new_ray = Ray(hit_point, Normalize(R))
                        especular = self.trace_ray(new_ray, depth - 1, objeto.kt)
                        #especular = especular * objeto2.kt
                else:
                    new_ray = Ray(hit_point, Normalize(R))
                    especular = self.trace_ray(new_ray, depth - 1, objeto.kt)
            else:                                               ## Raio Transmitido
                if (objeto.kt > 0):
                    L = Normalize(ray.d)
                    N = objeto.normal
                    if Length(N) != 1:
                        N = Normalize(N)
                    cos1 = Dot(N, flip_direction(L))
                    refletido = L + (N * (2 * cos1))
                    #refletido2 = Normalize(refletido)

                    # shadow ray
                    shadow_ray = Ray(Vector3D(refletido.x, refletido.y, refletido.z), Normalize(Vector3D(0.0000, 3.8360, -24.9060)))
                    for obj2 in self.obj_list:
                        inter2 = obj2.intersect(shadow_ray)
                        tmp_hit2 = inter2[0]
                        distance2 = inter2[1]

                        if tmp_hit2 and distance2 < dist2:
                            dist2 = distance2
                            objeto2 = obj2
                            hit2 = tmp_hit2
                            hit_point2 = inter2[2]
                            normal2 = inter2[3]
                            temLuz = 0
                            if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                if isinstance(objeto2, Light):
                                    temLuz = 1

                    if temLuz == 0:
                        if objeto2.kt == 0.0:
                            refletido = BLACK
                        else:
                            new_rayReflected = Ray(hit_point, Normalize(refletido))
                            refletido = self.trace_ray(new_rayReflected, depth - 1, objeto.kt)
                            #refletido = refletido * objeto2.kt
                    else:
                        new_rayReflected = Ray(hit_point, Normalize(refletido))
                        refletido = self.trace_ray(new_rayReflected, depth - 1, objeto.kt)

                    delta = 1-((pow(1.33/objeto.kt,2))*(1-(pow(cos1,2))))
                    if (delta >= 0):
                        cos2 = sqrt(delta)
                        divisao = nRefractedInitial / objeto.kt
                        nRefractedInitial = objeto.kt
                        if (cos1 > 0) :
                            transmitido = (L * divisao) + (N * ((divisao * cos1) - cos2))
                            #transmitido2 = Normalize(transmitido)
                        else:
                            transmitido = (L * divisao) + (N * ((divisao * cos1) + cos2))
                            #transmitido2 = Normalize(transmitido)

                        # shadow ray
                        shadow_ray = Ray(Vector3D(transmitido.x, transmitido.y, transmitido.z), Normalize(Vector3D(0.0000, 3.8360, -24.9060)))
                        for obj2 in self.obj_list:
                            inter2 = obj2.intersect(shadow_ray)
                            tmp_hit2 = inter2[0]
                            distance2 = inter2[1]

                            if tmp_hit2 and distance2 < dist2:
                                dist2 = distance2
                                objeto2 = obj2
                                hit2 = tmp_hit2
                                hit_point2 = inter2[2]
                                normal2 = inter2[3]
                                temLuz = 0
                                if hit2:  ## Se o raio bateu no objeto calculamos a cor do ponto
                                    if isinstance(objeto2, Light):
                                        temLuz = 1

                        if temLuz == 0:
                            if objeto2.kt == 0.0:
                                transmitido = BLACK
                            else:
                                new_ray = Ray(hit_point, Normalize(transmitido))
                                transmitido = self.trace_ray(new_ray, depth - 1, objeto.kt)
                                #transmitido = transmitido * objeto2.kt
                        else:
                            new_ray = Ray(hit_point, Normalize(transmitido))
                            transmitido = self.trace_ray(new_ray, depth-1, objeto.kt)

        return result + difuso * objeto.kd + especular * objeto.ks + refletido + transmitido * objeto.kt
