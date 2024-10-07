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

# Definir el laberinto
laberinto = [
    [' ', ' ', ' ', '#', ' ', 'E'],  # E = Elmo
    ['#', '#', ' ', '#', ' ', '#'],
    [' ', ' ', 'G', ' ', ' ', ' '],  # G = Galleta
    [' ', '#', '#', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['R', ' ', '#', ' ', 'P', ' ']   # R = René, P = Piggy
]

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

# Función para solicitar el límite de profundidad
def solicitar_limite_profundidad(ventana):
    fuente = pygame.font.Font(FONT, 20)
    entrada = ""
    limite_ingresado = False

    while not limite_ingresado:
        ventana.fill(BLANCO)
        texto = fuente.render("Ingrese el limite de profundidad (1-20):", True, NEGRO)
        ventana.blit(texto, (50, 50))
        limite_texto = fuente.render(entrada, True, NEGRO)
        ventana.blit(limite_texto, (50, 150))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if entrada.isdigit():
                        limite = int(entrada)
                        if 1 <= limite <= 20:
                            return limite
                    entrada = ""
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                elif len(entrada) < 2:
                    entrada += evento.unicode

        pygame.display.flip()

# Implementación de la búsqueda limitada por profundidad (DLS)
def busqueda_profundidad_limitada(laberinto, inicio, objetivo, limite_profundidad):
    def dls(posicion_actual, objetivo, profundidad_actual, visitados):
        if profundidad_actual == limite_profundidad:
            return None
        if posicion_actual == objetivo:
            return [posicion_actual]

        fila_actual, columna_actual = posicion_actual
        visitados.add(posicion_actual)
        caminos = []

        for movimiento in movimientos:
            nueva_fila = fila_actual + movimiento[0]
            nueva_columna = columna_actual + movimiento[1]

            if es_valida(nueva_fila, nueva_columna, laberinto) and (nueva_fila, nueva_columna) not in visitados:
                nuevo_estado = (nueva_fila, nueva_columna)
                resultado = dls(nuevo_estado, objetivo, profundidad_actual + 1, visitados)
                if resultado:
                    caminos.append([posicion_actual] + resultado)

        visitados.remove(posicion_actual)
        if caminos:
            return max(caminos, key=len)
        return None

    visitados = set()
    return dls(inicio, objetivo, 0, visitados)

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
    limite_profundidad = solicitar_limite_profundidad(ventana)
    camino = busqueda_profundidad_limitada(laberinto, posicion_rene, posicion_elmo, limite_profundidad)

    if camino:
        print("Camino encontrado:", camino)
        mover_rene(laberinto, camino)
        mostrar_mensaje_exito()
    else:
        print("No se encontró un camino dentro del límite de profundidad.")
    
    limpiar_laberinto()
    reiniciar_posiciones()
    en_menu = True

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

# Función para dibujar en la ventana
def draw():
    if en_menu:
        ventana.fill(BLANCO)
        boton_jugar.draw(ventana)
        boton_nosotros.draw(ventana)
        boton_salir.draw(ventana)
    elif en_nosotros:
        nosotros()
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
def manejar_eventos(events):
    global en_menu
    global en_nosotros
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if en_menu:
            if boton_jugar.clicked:
                jugar()
            if boton_nosotros.clicked:
                en_menu = False
                en_nosotros = True
            if boton_salir.clicked:
                pygame.quit()
                sys.exit()
        elif en_nosotros:
            if boton_volver.clicked:
                en_nosotros = False
                en_menu = True
                boton_nosotros.reset()
                
        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                en_menu = True

# Bucle principal
while True:
    events = pygame.event.get()
    manejar_eventos(events)
    update(events)
    draw()
    reloj.tick(60)

# Salir del juego
pygame.quit()