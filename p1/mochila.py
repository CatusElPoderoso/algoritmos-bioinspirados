import random
import time
random.seed(time.time())

# lista de individuos
individuos = []
# aptitudes y costos de cada individuo
aptitudes = []
costos = []
# probabilidad de seleccion y acumulada
probabilidades = []
probabilidades_ac = []
# padres e hijos
padre1 = []
padre2 = []
hijo1 = []
hijo2 = []
# lista de cruza y auxiliar
cruza = []
auxiliar = []

# CREAMOS individuos con genes aleatorios
def genera_individuo():
    return [random.randint(0, 10) for _ in range(7)]

# EVALUAMOS la aptitud (costo) de un individuo
def aptitud(individuo):
    return sum([individuo[0]*10, 
                individuo[1]*8, 
                individuo[2]*12, 
                individuo[3]*6, 
                individuo[4]*3, 
                individuo[5]*2, 
                individuo[6]*2])

# EVALUAMOS las restricciones (peso) de un individuo
def restriccion(individuo):
    return sum([individuo[0]*4,
                individuo[1]*2,
                individuo[2]*5,
                individuo[3]*5,
                individuo[4]*2,
                individuo[5]*1.5,
                individuo[6]*1])

# CREAMOS la lista de individuos considerando las restricciones
def genera_lista_individuos(individuos):
    numero_deseado_i = 10
    while len(individuos) < numero_deseado_i:
        individuo = genera_individuo()
        if individuo[1] >= 3 and individuo[3] >= 2 and restriccion(individuo) <= 30:
            individuos.append(individuo)
            # print(f"{individuo}\ncuesta: {aptitud(individuo)} y pesa: {restriccion(individuo)}")
    print("\nGeneracion inicial: \n" + str(individuos))

def vector_aptitud(aptitudes, individuos):
    for individuo in individuos:
        apt = aptitud(individuo)
        aptitudes.append(apt)

def vector_costos(costos, individuos):
    for individuo in individuos:
        cst = restriccion(individuo)
        costos.append(cst)

# probabilidad de seleccion
def probabilidad(probabilidades, probabilidades_ac, aptitudes):
    siu = sum(aptitudes)
    for apt in aptitudes:
        probabilidades.append(apt / siu)
    probabilidad_ac = 0
    for apt in aptitudes:
        probabilidad_ac += apt / siu
        probabilidades_ac.append(probabilidad_ac)

genera_lista_individuos(individuos)
vector_aptitud(aptitudes, individuos)
vector_costos(costos, individuos)

probabilidad(probabilidades, probabilidades_ac, aptitudes)

# Descomenta si deseas ver las probabilidades
# print(probabilidades)
# print(probabilidades_ac)

# ALGORITMO GENETICOOOOOOOO

def genera_elemento_cruza():
    return [random.uniform(0,1) for _ in range(7)]

def ruleta(probabilidades_ac, individuos):
    global padre1, padre2  
    # crear dos números al azar
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)

    # recorrer probabilidad acumulada para decidir los dos papás
    for i in range(len(probabilidades_ac)): 
        if probabilidades_ac[i] > r1:
            padre1 = individuos[i]
            no_repetir = probabilidades_ac[i]
            break
    
    encontrado = False
    while not encontrado:
        for i in range(len(probabilidades_ac)):
            if probabilidades_ac[i] > r2:
                if probabilidades_ac[i] == no_repetir:
                    r2 = random.uniform(0,1)
                    # print("Reasigno r2 para evitar cruza del mismo individuo")
                    break  # Salir del ciclo for y volver a empezar
                else:
                    padre2 = individuos[i]
                    encontrado = True  # Hemos encontrado un padre diferente, salir del while
                    break 
    return padre1, padre2

def cruzar(cruza, hijo1, hijo2):
    hijo1.clear()  # Limpiar antes de cada cruce
    hijo2.clear()

    for i in range(7):  # Ajustar para que el índice empiece en 0
        if cruza[i] <= .5:
            hijo1.append(padre1[i])
        else:
            hijo1.append(padre2[i])

    for i in range(7):  # Ajustar para que el índice empiece en 0
        if cruza[i] <= .5:
            hijo2.append(padre2[i])
        else:
            hijo2.append(padre1[i])

def mutar(hijo):
    for i in range(7):  # Ajustar para que el índice empiece en 0
        r1 = random.uniform(0,1)
        if r1 <= .1:
            if (i == 1):
                r2 = random.randint(3, 10)
                hijo[i] = r2
            elif(i==3):
                r2 = random.randint(2, 10)
                hijo[i] = r2
            else:
                r2 = random.randint(1, 10)
                hijo[i] = r2

for i in range(50):
    #def generacion(padre1, padre2)
    for i in range(5):  
        # generar padres
        padre1, padre2 = ruleta(probabilidades_ac, individuos)
        # calcular probabilidad de cruza
        r1 = random.uniform(0,1)
        if r1 <= .85:
            # realizar cruza y mutación
            cruza = genera_elemento_cruza()
            cruzar(cruza, hijo1, hijo2)
            mutar(hijo1)
            mutar(hijo2)
            while(restriccion(hijo1)>30 or restriccion(hijo2)>30):
                cruza = genera_elemento_cruza()
                cruzar(cruza, hijo1, hijo2)
                mutar(hijo1)
                mutar(hijo2)
            
            if (aptitud(hijo1) >= aptitud(padre1) ):
                auxiliar.append(hijo1[:])  # Usar append para agregar copias de las listas
            else:
                auxiliar.append(padre1[:])
            if (aptitud(hijo2)>= aptitud(padre2) ):
                auxiliar.append(hijo2[:]) 
            else:
                auxiliar.append(padre2[:])              
        else:
            auxiliar.append(padre1[:])
            auxiliar.append(padre2[:])

    individuos.clear()
    individuos.extend([individuo[:] for individuo in auxiliar])
    auxiliar.clear()

    probabilidades.clear()
    probabilidades_ac.clear()
    aptitudes.clear()
    costos.clear()
    
    vector_aptitud(aptitudes, individuos)
    vector_costos(costos, individuos)
    probabilidad(probabilidades, probabilidades_ac, aptitudes)

    # print(individuos)
    # print("fin de la generación")

print("\nGeneracion final: \n" + str(individuos) + "\n")
mejora = 0
for i in range (10):
    m = aptitud(individuos[i])
    if(m > mejora):
        mejora = aptitud(individuos[i])
        mejor  = individuos[i]

print("La mejor forma para que los hermanos lleven sus productos dentro de la mochila es: \n")
print("Decoy Detonators:\t" + str(mejor[0]) + "\nLove Potion:\t\t" + str(mejor[1]) + "\nExtendable Ears:\t" + str(mejor[2]) + "\nSkiving Snackbox:\t" + str(mejor[3]) + "\nFever Fudge:\t\t" + str(mejor[4]) + "\nPuking Pastilles:\t" + str(mejor[5]) + "\nNosebleed Nougat:\t" + str(mejor[6]))
print("\nCon un valor total de " + str(aptitud(mejor)) + " y un peso de " + str(restriccion(mejor)))