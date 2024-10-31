import pygame
import sys
from boton import Button

# Inicializar Pygame
pygame.init()

# Definir los colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

FONT = 'font/minecraft_font.ttf'

# Dimensiones de la ventana
ANCHO_VENTANA = 600
ALTO_VENTANA = 600
TAMANO_CELDA = 100  # Cada celda será de 100x100 píxeles
FILAS = 6
COLUMNAS = 6

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Pacman Univalle - LUCHITO Y VARGAS")

# Reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Cargar imágenes de personajes
imagen_rene = pygame.image.load("imagenes/rana.jpeg")
imagen_piggy = pygame.image.load("imagenes/piggy.jpeg")
imagen_elmo = pygame.image.load("imagenes/elmo.jpeg")
imagen_galleta = pygame.image.load("imagenes/galleta.jpeg")
imagen_rana_elmo = pygame.image.load("imagenes/ranayelmo.jpeg")
imagen_rana_galleta = pygame.image.load("imagenes/rene_come_galleta.jpeg")

# Escalar las imágenes al tamaño adecuado
imagen_rene = pygame.transform.scale(imagen_rene, (TAMANO_CELDA, TAMANO_CELDA))
imagen_piggy = pygame.transform.scale(imagen_piggy, (TAMANO_CELDA, TAMANO_CELDA))
imagen_elmo = pygame.transform.scale(imagen_elmo, (TAMANO_CELDA, TAMANO_CELDA))
imagen_galleta = pygame.transform.scale(imagen_galleta, (TAMANO_CELDA, TAMANO_CELDA))
imagen_rana_elmo = pygame.transform.scale(imagen_rana_elmo, (TAMANO_CELDA, TAMANO_CELDA))  
imagen_rana_galleta = pygame.transform.scale(imagen_rana_galleta, (TAMANO_CELDA, TAMANO_CELDA))

# MAPAS
mapa1 = [
    [' ', ' ', ' ', '#', ' ', 'E'],
    ['#', '#', ' ', '#', ' ', '#'],
    [' ', ' ', 'G', ' ', ' ', ' '],
    [' ', '#', '#', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['R', ' ', '#', ' ', 'P', ' ']
]

mapa2 = [
    ['#', ' ', ' ', ' ', ' ', 'E'],
    ['#', '#', '#', '#', ' ', '#'],
    [' ', ' ', 'G', '#', ' ', ' '],
    [' ', '#', ' ', ' ', ' ', ' '],
    ['#', ' ', '#', '#', '#', ' '],
    ['R', ' ', ' ', ' ', 'P', ' ']
]

mapa3 = [
    [' ', '#', ' ', '#', ' ', 'E'],
    [' ', ' ', ' ', '#', ' ', '#'],
    ['#', 'G', ' ', ' ', ' ', ' '],
    [' ', '#', '#', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['R', ' ', '#', ' ', 'P', ' ']
]

# Lista de mapas
mapas = [mapa1, mapa2, mapa3]
laberinto = mapas[0]  # Inicializa el laberinto con el primer mapa
en_seleccion_mapa = False  # Agrega esta línea para inicializar la variable


def seleccionar_mapa():
    print("Selecciona un mapa:")
    for i, mapa in enumerate(mapas, start=1):
        print(f"{i}. Mapa {i}")

    seleccion = int(input("Introduce el número del mapa que deseas: ")) - 1
    if 0 <= seleccion < len(mapas):
        return mapas[seleccion]
    else:
        print("Selección no válida. Se seleccionará el Mapa 1 por defecto.")
        return mapas[0]


# Posiciones de René y Elmo
posicion_rene = (5, 0)  # Posición inicial de René
posicion_elmo = (0, 5)  # Posición de Elmo
posicion_piggy = (5, 4)
posicion_galleta = (2, 1)

# Movimientos posibles: arriba, abajo, izquierda, derecha
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Función para comprobar si una posición está dentro de los límites del laberinto
def es_valida(fila, columna, laberinto):
    return 0 <= fila < len(laberinto) and 0 <= columna < len(laberinto[0]) and laberinto[fila][columna] != '#'

# Función para dibujar el laberinto
def dibujar_laberinto(ventana, laberinto):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            celda = laberinto[fila][columna]
            if celda == '#':  # Obstáculo
                pygame.draw.rect(ventana, NEGRO, 
                                 (columna * TAMANO_CELDA, fila * TAMANO_CELDA, 
                                  TAMANO_CELDA, TAMANO_CELDA))
            elif celda == 'R':  # René
                ventana.blit(imagen_rene, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            elif celda == 'P':  # Piggy
                ventana.blit(imagen_piggy, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            elif celda == 'E':  # Elmo
                ventana.blit(imagen_elmo, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            elif celda == 'G':  # Galleta
                ventana.blit(imagen_galleta, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            else:  # Espacio vacío
                pygame.draw.rect(ventana, BLANCO, 
                                 (columna * TAMANO_CELDA, fila * TAMANO_CELDA, 
                                  TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.rect(ventana, NEGRO, 
                             (columna * TAMANO_CELDA, fila * TAMANO_CELDA, 
                              TAMANO_CELDA, TAMANO_CELDA), 1)

def busqueda_profundidad_limitada(laberinto, inicio, objetivo, max_profundidad):
    # Algoritmo de DFS Limitado usando una lista para almacenar las posiciones visitadas
    def dls(posicion_actual, objetivo, profundidad_actual, visitados, arbol):
        # Si alcanzamos el límite de profundidad, no buscamos más
        if profundidad_actual >= limite_profundidad:
            return None
        
        # Si encontramos el objetivo, devolvemos el camino
        if posicion_actual == objetivo:
            return [posicion_actual]
        
        # Agregar la posición actual a los visitados
        visitados.append(posicion_actual)

        # Inicializar el nodo en el árbol
        if posicion_actual not in arbol:
            arbol[posicion_actual] = []

        # Explorando movimientos posibles
        for movimiento in movimientos:
            nueva_fila = posicion_actual[0] + movimiento[0]
            nueva_columna = posicion_actual[1] + movimiento[1]
            nuevo_estado = (nueva_fila, nueva_columna)

            # Verifica que la nueva posición sea válida y no sea un estado ya visitado
            if es_valida(nueva_fila, nueva_columna, laberinto) and nuevo_estado not in visitados:
                # Agregar el nuevo estado al árbol de búsqueda
                arbol[posicion_actual].append(nuevo_estado)

                # Llamada recursiva con el nuevo estado
                resultado = dls(nuevo_estado, objetivo, profundidad_actual + 1, visitados, arbol)

                # Si encontramos un resultado, lo retornamos
                if resultado:
                    return [posicion_actual] + resultado
        
        # Eliminar la posición actual de visitados después de explorar
        visitados.pop()
        return None

    for limite_profundidad in range(1, max_profundidad + 1):
        visitados = []  # Reiniciar la lista de visitados para cada profundidad
        arbol = {}
        resultado = dls(inicio, objetivo, 0, visitados, arbol)

        # Imprimir el árbol completo
        print(f"Árbol completo para profundidad {limite_profundidad}:")
        for nodo, hijos in arbol.items():
            print(f"{nodo}: {hijos}")

        # Si se encuentra un resultado, retornarlo y podar el árbol
        if resultado:
            arbol_podado = podar_arbol(arbol, resultado)
            return resultado, arbol_podado

    return None, {}  # Si no se encontró camino dentro del límite de profundidad

def podar_arbol(arbol, camino_valido):
    arbol_podado = {}
    for i in range(len(camino_valido) - 1):
        nodo = camino_valido[i]
        siguiente_nodo = camino_valido[i + 1]
        arbol_podado[nodo] = [siguiente_nodo]
    return arbol_podado

# Función para mover a René
comio_galleta = False  
def mover_rene(laberinto, camino):
    global comio_galleta
    for paso in camino:
        fila, columna = paso
        for fila_laberinto in range(len(laberinto)):
            for columna_laberinto in range(len(laberinto[0])): 
                if laberinto[fila_laberinto][columna_laberinto] == 'R':
                    laberinto[fila_laberinto][columna_laberinto] = ' '

        laberinto[fila][columna] = 'R'
        if (fila, columna) == tuple(posicion_galleta):
            comio_galleta = True

        dibujar_laberinto(ventana, laberinto)
        if comio_galleta:
            ventana.blit(imagen_rana_galleta, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
        else:
            ventana.blit(imagen_rene, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))

        ventana.blit(imagen_piggy, (posicion_piggy[1] * TAMANO_CELDA, posicion_piggy[0] * TAMANO_CELDA))
        ventana.blit(imagen_galleta, (posicion_galleta[1] * TAMANO_CELDA, posicion_galleta[0] * TAMANO_CELDA))
        
        pygame.display.flip()
        pygame.time.delay(500)

        if (fila, columna) == posicion_elmo:
            ventana.blit(imagen_rana_elmo, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            pygame.display.flip()
            pygame.time.delay(500)
            break

    if comio_galleta:
        comio_galleta = False
        dibujar_laberinto(ventana, laberinto)
        ventana.blit(imagen_rene, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
        pygame.display.flip()

# Función para mostrar mensaje de éxito
def mostrar_mensaje_exito():
    fuente = pygame.font.Font(FONT, 20)
    ventana.fill(BLANCO)
    mensaje = fuente.render("¡René encontró a Elmo!", True, VERDE)
    ventana.blit(mensaje, (50, 50))
    boton_rect = pygame.Rect(150, 200, 300, 100)
    pygame.draw.rect(ventana, AZUL, boton_rect)
    boton_texto = fuente.render("Volver a jugar", True, BLANCO)
    ventana.blit(boton_texto, (200, 230))
    pygame.display.flip()
    
    esperando_click = True
    while esperando_click:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    esperando_click = False

# Función para limpiar el laberinto
def limpiar_laberinto():
    laberinto[5][0] = 'R'  
    laberinto[0][5] = 'E'  
    laberinto[5][4] = "P"
    laberinto[2][1] = "G"

# Función para reiniciar posiciones
def reiniciar_posiciones():
    ventana.blit(imagen_piggy, (posicion_piggy[1] * TAMANO_CELDA, posicion_piggy[0] * TAMANO_CELDA))
    ventana.blit(imagen_galleta, (posicion_galleta[1] * TAMANO_CELDA, posicion_galleta[0] * TAMANO_CELDA))
    ventana.blit(imagen_rana_elmo, (posicion_elmo[1] * TAMANO_CELDA, posicion_elmo[0] * TAMANO_CELDA)) 
    pygame.display.flip()

# Función principal del juego
def jugar():
    global en_menu
    global en_nosotros
    
    # Configuración inicial del juego
    posicion_rene = (5, 0)  # Posición inicial de René
    posicion_elmo = (0, 5)  # Posición de Elmo
    max_profundidad = 20  # Establece el límite máximo de profundidad
    
    # Realiza la búsqueda de profundidad limitada
    camino, arbol_podado = busqueda_profundidad_limitada(laberinto, posicion_rene, posicion_elmo, max_profundidad)

    if camino:
        print("Camino encontrado:", camino)
        mover_rene(laberinto, camino)  # Mueve a René por el laberinto
        mostrar_mensaje_exito()  # Muestra el mensaje de éxito
    else:
        print("No se encontró un camino dentro del límite de profundidad.")

    limpiar_laberinto()  # Limpia el laberinto para el próximo juego
    reiniciar_posiciones()  # Reinicia las posiciones de los personajes
    en_menu = True  # Regresar al menú principal

# Interfaz gráfica
boton_jugar = Button(200, 100, "Jugar")
boton_nosotros = Button(200, 175, "Creditos")
boton_salir = Button(200, 250, "Salir")
boton_volver = Button(200, 500, "Volver")

# Variable para controlar el estado del juego
en_menu = True
en_nosotros = False

# Función para actualizar el estado del juego
def update(events):
    if en_menu:
        boton_jugar.update()
        boton_nosotros.update()
        boton_salir.update()
    elif en_nosotros:
        boton_volver.update()
    elif en_seleccion_mapa:
        pass  # No necesitas botones en la selección de mapa

# Función para dibujar en la ventana
def draw():
    if en_menu:
        ventana.fill(BLANCO)
        boton_jugar.draw(ventana)
        boton_nosotros.draw(ventana)
        boton_salir.draw(ventana)
    elif en_nosotros:
        nosotros()
    elif en_seleccion_mapa:
        mostrar_seleccion_mapa()  # Mostrar la selección de mapa
    pygame.display.flip()

def nosotros():
    ventana.fill(BLANCO)
    fuente = pygame.font.Font(FONT, 24)
    creditos = [
        "Desarrollado por:",
        "Luis F. Hernandez - 2160189",
        "Juan E. Vargas - 2160191",
        "Universidad del Valle",
    ]
    y = 50
    for linea in creditos:
        texto = fuente.render(linea, True, NEGRO)
        ventana.blit(texto, (50, y))
        y += 50
    boton_volver.draw(ventana)
    pygame.display.flip()
    
# Función para manejar eventos

# Modificación en la función manejar_eventos para manejar los botones de selección de mapa correctamente
def manejar_eventos(events):
    global en_menu
    global en_nosotros
    global en_seleccion_mapa
    global laberinto

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if en_menu:
            if boton_jugar.clicked:
                en_menu = False
                en_seleccion_mapa = True  # Cambia al estado de selección de mapa
            if boton_nosotros.clicked:
                en_menu = False
                en_nosotros = True
            if boton_salir.clicked:
                pygame.quit()
                sys.exit()

        elif en_seleccion_mapa:
            # Aquí verifica cada botón de mapa
            for i in range(len(mapas)):
                boton_mapa = Button(200, 100 + i * 75, f"Mapa {i + 1}")
                boton_mapa.update()  # Actualiza el estado del botón
                if boton_mapa.clicked:
                    laberinto = mapas[i]  # Selecciona el mapa
                    jugar()  # Inicia el juego con el mapa seleccionado

            # Botón de volver al menú
            boton_volver_menu = Button(200, 100 + len(mapas) * 75, "Volver al menú")
            boton_volver_menu.update()  # Asegúrate de que se actualice
            if boton_volver_menu.clicked:
                en_seleccion_mapa = False
                en_menu = True  # Regresar al menú principal

        elif en_nosotros:
            if boton_volver.clicked:
                en_nosotros = False
                en_menu = True  # Regresar al menú principal


# Función para mostrar la selección de mapa
def mostrar_seleccion_mapa():
    ventana.fill(BLANCO)
    fuente = pygame.font.Font(FONT, 24)

    # Títulos
    titulo = fuente.render("Selecciona un mapa:", True, NEGRO)
    ventana.blit(titulo, (150, 50))

    # Dibujar botones para cada mapa
    for i, mapa in enumerate(mapas):
        boton_mapa = Button(200, 100 + i * 75, f"Mapa {i + 1}")
        boton_mapa.draw(ventana)

    # Botón de volver al menú
    boton_volver_menu = Button(200, 100 + len(mapas) * 75, "Volver al menú")
    boton_volver_menu.draw(ventana)

    pygame.display.flip()

# Bucle principal
while True:
    events = pygame.event.get()
    manejar_eventos(events)
    update(events)
    draw()
    reloj.tick(60)

# Salir del juego
pygame.quit()