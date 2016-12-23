"""
Responsavel por controlar o aplicativo
"""
from helper import read
from random import random, gauss, randrange

print("Lendo Arquivos de configuração e Objetos")

file = "./src/cornellroom.sdl"

obj_types_list = ['object','quad', 'light']
prop_types_list = ['eye', 'size', 'ortho', 'background', 'ambient', 'tonemapping', 'npaths', 'seed', 'output']

obj_list = []  # Lista de objetos a serem redenrizados
prop_dict = {} # dicionario com propriedades da cena

# Lendo os arquivos de configurações e objetos
f = open(file, 'r')

for line in f:
    # Pulando linhas em branco
    if len(line) < 2:
        continue

    words = line.split()
    line_type = words[0] ## Tipo da linha
    values = words[1:]   ## Valores do objeto ou propriedade

    if line_type == '#':
        pass
    elif line_type in obj_types_list:
        obj_list.append(read(line_type, values))
    elif line_type in prop_types_list:
        prop_dict[line_type] = (read(line_type, values))
    else:
        print ("Tipo não encontrado")
        print(line_type)

print("Lista de objetos: ", obj_list)
print("Lista de propriedades: ", prop_dict)
print(obj_list[5].vertices)
i = 0
a = 0.0
b = 0.0
c = 0.0
ve = []
p = []
q = []
for x in obj_list[5].faces:
    print((obj_list[5].faces[i]))
    ve = (obj_list[5].faces[i])
    d = 0
    i = i+1
    for j in ve:
        print(ve[d])
        if d == 0:
            a = (obj_list[5].vertices[ve[d]-1])
        if d == 1:
            b = (obj_list[5].vertices[ve[d]-1])
        if d == 2:
            c = (obj_list[5].vertices[ve[d]-1])
        d = d+1
    p = a - b
    q = a - c
    print(p)
    print(q)
    a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x
    n = p[1]*q[2] - p[2]*q[1], p[2]*q[0] - p[0]*q[2], p[0]*q[1] - p[1]*q[0]
    print(n)
    b = randrange(3)
    print(b)
#print(str (obj_types_list['light'][0]))
# Inicializando objetos da cena
