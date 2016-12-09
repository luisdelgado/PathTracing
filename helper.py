## leitura dos arquivos
from objetos import Objeto, Luz, ObjectQuadric
from pygame.math import Vector3

# Cada função trata um tipo diferente do arquivo de configuração
class Read():
    def __init__(self):
        pass

    def eye(self, values):
        return self.__get_float_list(values)

    def size(self, values):
        return  self.__get_float_list(values)

    def ortho(self, values):
        return  self.__get_float_list(values)

    def background(self, values):
        return  self.__get_float_list(values)

    def ambient(self, values):
        return self.__get_float(values)

    def tonemapping(self, values):
        return self.__get_float(values)

    def npaths(self, values):
        return self.__get_float(values)

    def seed(self,  values):
        return self.__get_float(values)

    def object(self, values):
        # Obtendo os vertices e faces que se encontram em arquivos separdos
        vertices = self.__get_vertices(values[0])
        faces = self.__get_faces(values[0])

        cor = (float(values[1]),
               float(values[2]),
               float(values[3]))

        # Demais propriedades do objeto
        ka = values[4]
        kd = values[5]
        ks = values[6]
        kt = values[7]
        n = values[8]

        obj = Objeto(vertices, faces, cor, ka, kd, ks, kt, n)

        return obj

    def light(self, values):
        # Obtendo os vertices e faces que se encontram em arquivos separdos
        vertices = self.__get_vertices(values[0])
        faces = self.__get_faces(values[0])

        # Cor e intensidade da luz
        cor = (values[1], values[2], values[3])
        lp = float(values[4])

        luz = Luz(vertices, faces, cor, lp)

        return luz

    def objectquadric(self, values):
        print(values)

    # Retorna a string contendo o nome do arquivo de saida
    def output(self,values):
        return values[0]

    # retorna uma lista contendo os vertices(Lista de int)
    def __get_faces(self, name):
        faces = []

        f = open ('.\src\\' + name, 'r')

        for line in f:
            # Pulando linhas em branco
            if len(line) < 2:
                continue

            words = line.split()
            line_type = words[0]  ## Tipo da linha
            values = words[1:]  ## Valores do objeto ou propriedade

            if line_type == 'f':
                vect3 = [int(values[0]),
                         int(values[1]),
                         int(values[2])]

                faces.append(vect3)

        return faces

    # Retorna des vertices(lista de Vector3)
    def __get_vertices(self, name):
        vertices = []
        faces = []

        f = open ('.\src\\' + name, 'r')

        for line in f:
            # Pulando linhas em branco
            if len(line) < 2:
                continue

            words = line.split()
            line_type = words[0]  ## Tipo da linha
            values = words[1:]  ## Valores do objeto ou propriedade

            if line_type == 'v':
                vect3 = Vector3(float(values[0]),
                                float(values[1]),
                                float(values[2]))

                vertices.append(vect3)


        return vertices

    # As funções abaixo apenas realizam conversão de tipos em uma lista
    def __get_float_list(self,values):
        return list(map(float, values))

    def __get_float(self, value):
        fst = value[0]

        return float(fst)

# Checa o time e designa a função para retornar o valor formatado
def read(t, values):
     read = Read()

    # Chamamos a função com nome read_ + tipo do valor a ser lido(object, light, eye...)
     func = getattr(read, t)
     result = func(values)
     return result