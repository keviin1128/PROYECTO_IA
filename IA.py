import pygame

# Inicializar Pygame
pygame.init()

# Definir los colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

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

# Función para dibujar el laberinto
def dibujar_laberinto(ventana, laberinto):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Obtener el contenido de la celda
            celda = laberinto[fila][columna]

            # Dibujar el contenido de la celda
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
            # Dibujar el borde de la celda
            pygame.draw.rect(ventana, NEGRO, 
                             (columna * TAMANO_CELDA, fila * TAMANO_CELDA, 
                              TAMANO_CELDA, TAMANO_CELDA), 1)

# Posiciones de René y Elmo
posicion_rene = (5, 0)  # Posición inicial de René
posicion_elmo = (0, 5)  # Posición de Elmo
posicion_piggy = (5, 4)
posicion_galleta = (2 , 1)


# Movimientos posibles: arriba, abajo, izquierda, derecha
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Función para comprobar si una posición está dentro de los límites del laberinto
def es_valida(fila, columna, laberinto):
    return 0 <= fila < len(laberinto) and 0 <= columna < len(laberinto[0]) and laberinto[fila][columna] != '#'

def solicitar_limite_profundidad(ventana):
    fuente = pygame.font.SysFont(None, 48)
    entrada = ""
    limite_ingresado = False

    while not limite_ingresado:
        ventana.fill(BLANCO)  # Limpiar la pantalla
        texto = fuente.render("Ingrese el límite de profundidad (1-20):", True, NEGRO)
        ventana.blit(texto, (50, 50))

        # Mostrar el límite ingresado hasta ahora
        limite_texto = fuente.render(entrada, True, NEGRO)
        ventana.blit(limite_texto, (50, 150))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Si se presiona Enter
                    if entrada.isdigit():
                        limite = int(entrada)
                        if 1 <= limite <= 20:  # Verificar el rango
                            return limite
                    entrada = ""  # Reiniciar la entrada
                elif evento.key == pygame.K_BACKSPACE:  # Manejar Backspace
                    entrada = entrada[:-1]  # Eliminar último carácter
                elif len(entrada) < 2:  # Limitar la longitud de la entrada
                    entrada += evento.unicode  # Agregar carácter a la entrada

        # Redibujar la ventana
        pygame.display.flip()

# Implementación de la búsqueda limitada por profundidad (DLS)
def busqueda_profundidad_limitada(laberinto, inicio, objetivo, limite_profundidad):
    def dls(posicion_actual, objetivo, profundidad_actual, visitados):
        # Si hemos alcanzado el límite de profundidad, no podemos continuar
        if profundidad_actual == limite_profundidad:
            return None

        # Si encontramos al objetivo, devolvemos el camino
        if posicion_actual == objetivo:
            return [posicion_actual]

        fila_actual, columna_actual = posicion_actual
        visitados.add(posicion_actual)  # Marcamos la posición como visitada
        caminos = []  # Para almacenar todos los caminos encontrados

        for movimiento in movimientos:
            nueva_fila = fila_actual + movimiento[0]
            nueva_columna = columna_actual + movimiento[1]

            # Verificamos si la nueva posición es válida y no ha sido visitada
            if es_valida(nueva_fila, nueva_columna, laberinto) and (nueva_fila, nueva_columna) not in visitados:
                nuevo_estado = (nueva_fila, nueva_columna)

                # Llamamos recursivamente a DLS incrementando el número de pasos
                resultado = dls(nuevo_estado, objetivo, profundidad_actual + 1, visitados)

                # Si se encuentra un camino válido, se agrega a la lista de caminos
                if resultado:
                    caminos.append([posicion_actual] + resultado)

        visitados.remove(posicion_actual)  # Desmarcar la posición después de explorar

        # Devolvemos el camino más largo encontrado (si existe) dentro del límite de profundidad
        if caminos:
            return max(caminos, key=len)  # Elegir el camino más largo
        return None  # No se encontró un camino dentro del límite de profundidad

    # Inicializamos el conjunto de posiciones visitadas
    visitados = set()
    return dls(inicio, objetivo, 0, visitados)

# Solicitar el límite de profundidad al inicio
limite_profundidad = solicitar_limite_profundidad(ventana)

# Lógica del juego después de obtener el límite de profundidad
camino = busqueda_profundidad_limitada(laberinto, posicion_rene, posicion_elmo, limite_profundidad)

if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino dentro del límite de profundidad.")

comio_galleta = False  
def mover_rene(laberinto, camino):
    global comio_galleta  # Usar la bandera global
    for paso in camino:
        fila, columna = paso

        # Limpiar la posición anterior de René
        for fila_laberinto in range(len(laberinto)):
            for columna_laberinto in range(len(laberinto[0])):
                if laberinto[fila_laberinto][columna_laberinto] == 'R':
                    laberinto[fila_laberinto][columna_laberinto] = ' '  # Limpiar la posición anterior

        # Actualizar la posición de René en el laberinto
        laberinto[fila][columna] = 'R'

        # Verificar si René ha llegado a la galleta
        if (fila, columna) == tuple(posicion_galleta):
            comio_galleta = True  # Cambiar el estado si se encuentra con la galleta

        # Redibujar el laberinto y los objetos en él
        dibujar_laberinto(ventana, laberinto)

        # Seleccionar la imagen de René según si ha comido galleta o no
        if comio_galleta:
            ventana.blit(imagen_rana_galleta, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
        else:
            ventana.blit(imagen_rene, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))

        # Redibujar Piggy y la galleta
        ventana.blit(imagen_piggy, (posicion_piggy[1] * TAMANO_CELDA, posicion_piggy[0] * TAMANO_CELDA))
        ventana.blit(imagen_galleta, (posicion_galleta[1] * TAMANO_CELDA, posicion_galleta[0] * TAMANO_CELDA))
        
        pygame.display.flip()
        pygame.time.delay(500)  # Pausa para que el movimiento sea visible

        # Verificar si René ha llegado a Elmo
        if (fila, columna) == posicion_elmo:  # Si René está en la posición de Elmo
            ventana.blit(imagen_rana_elmo, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))
            pygame.display.flip()
            pygame.time.delay(500)
            break  # Detener el bucle porque René ha llegado a Elmo

    # Al final del movimiento, si ha comido la galleta, reiniciar la bandera
    if comio_galleta:
        # Reiniciar la bandera para la próxima iteración
        comio_galleta = False  # Reiniciar la bandera para la próxima iteración
        # Redibujar el laberinto para mostrar la imagen original en la siguiente iteración
        dibujar_laberinto(ventana, laberinto)
        ventana.blit(imagen_rene, (columna * TAMANO_CELDA, fila * TAMANO_CELDA))  # Asegurarse de que se dibuje la imagen original
        pygame.display.flip()  # Actualizar la pantalla


# Bucle para ejecutar el juego
ejecutando = True

# Mover a René por el camino encontrado
if camino:
    mover_rene(laberinto, camino)

def mostrar_mensaje_exito():
    fuente = pygame.font.SysFont(None, 48)
    ventana.fill(BLANCO)
    
    # Mensaje de éxito
    mensaje = fuente.render("¡René encontró a Elmo!", True, VERDE)
    ventana.blit(mensaje, (50, 50))
    
    # Botón para reiniciar
    boton_rect = pygame.Rect(150, 200, 300, 100)
    pygame.draw.rect(ventana, AZUL, boton_rect)
    boton_texto = fuente.render("Volver a jugar", True, BLANCO)
    ventana.blit(boton_texto, (200, 230))

    # Actualizar la pantalla
    pygame.display.flip()
    
    # Esperar a que se haga clic en el botón
    esperando_click = True
    while esperando_click:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):  # Si se hace clic en el botón
                    esperando_click = False

while ejecutando:
    # Solicitar el límite de profundidad al inicio
    limite_profundidad = solicitar_limite_profundidad(ventana)

    # Lógica del juego después de obtener el límite de profundidad
    camino = busqueda_profundidad_limitada(laberinto, posicion_rene, posicion_elmo, limite_profundidad)

    if camino:
        print("Camino encontrado:", camino)
        mover_rene(laberinto, camino)  # Mover a René por el camino encontrado
        mostrar_mensaje_exito()  # Mostrar mensaje de éxito
    else:
        print("No se encontró un camino dentro del límite de profundidad.")

    # Esperar un momento antes de reiniciar
    pygame.time.delay(2500)  

    # Limpiar el laberinto y volver a la posición inicial
    laberinto[5][0] = 'R'  
    laberinto[0][5] = 'E'  
    laberinto[5][4] = "P"
    laberinto[2][1] = "G"

    # Limpiar la ventana y volver a dibujar el laberinto
    ventana.fill(BLANCO)
    dibujar_laberinto(ventana, laberinto)
    pygame.display.flip()

    # Redibujar las imágenes de Piggy y la galleta en sus posiciones
    ventana.blit(imagen_piggy, (posicion_piggy[1] * TAMANO_CELDA, posicion_piggy[0] * TAMANO_CELDA))
    ventana.blit(imagen_galleta, (posicion_galleta[1] * TAMANO_CELDA, posicion_galleta[0] * TAMANO_CELDA))
    ventana.blit(imagen_rana_elmo, (posicion_elmo[1] * TAMANO_CELDA, posicion_elmo[0] * TAMANO_CELDA)) 
    
    pygame.display.flip() 

    # Comprobar eventos para salir
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

# Salir del juego
pygame.quit()
