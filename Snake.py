import random 
import pygame 
from pygame import mixer
import os 
import sys
import math

def resource_path(relative_path):
    """Función mejorada para rutas en Linux"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        pygame.init()
        mixer.init()
        return True
    except Exception as e:
        print(f"Error inicializando Pygame: {e}")
        return False

# Inicializar Pygame con verificación
if not verificar_dependencias():
    print("Error: Pygame no está instalado correctamente.")
    print("Instala con: sudo apt install python3-pygame")
    sys.exit(1)

# Constantes del juego
ANCHO, ALTO = 900, 600  
TAMANIO_CELDA = 20
FILAS, COLUMNAS = ALTO // TAMANIO_CELDA, ANCHO // TAMANIO_CELDA
FPS = 7

# Colores   
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 180, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 100, 255)
GRIS = (40, 40, 40)
BORDE_COLOR = (100, 100, 100)
COLOR_FONDO = (211, 211, 211)  # Fondo gris claro
COLOR_BOTON = (50, 50, 50)
COLOR_BOTON_HOVER = (100, 150, 100)
COLOR_TEXTO = (255, 255, 255)

# Direcciones
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Snake Game")

# Configuración de audio mejorada para Linux
def cargar_audio():
    """Cargar recursos de audio con mejor manejo de errores"""
    formatos_audio = [
        "assets/Musica/Musica-De-Fondo.ogg",
        "assets/Musica/Musica-De-Fondo.wav", 
        "assets/Musica/Musica-De-Fondo.mp3",
        # Rutas alternativas
        "Musica-De-Fondo.ogg",
        "Musica-De-Fondo.wav",
        "Musica-De-Fondo.mp3"
    ]
    
    for formato in formatos_audio:
        try:
            ruta_audio = resource_path(formato)
            print(f"Intentando cargar: {ruta_audio}")
            
            if os.path.exists(ruta_audio):
                print(f"Archivo encontrado: {ruta_audio}")
                mixer.music.load(ruta_audio)
                mixer.music.play(-1)  # -1 para loop infinito
                mixer.music.set_volume(0.5)
                print("¡Música cargada y reproduciendo!")
                return True
            else:
                print(f"Archivo no encontrado: {ruta_audio}")
                
        except Exception as e:
            print(f"Error cargando {formato}: {e}")
    
    print("Advertencia: No se pudo cargar ningún archivo de audio")
    return False

# Cargar audio
cargar_audio()

# Cargar icono con múltiples formatos
def cargar_icono():
    """Cargar icono con formatos compatibles con Linux"""
    formatos_icono = [
        "assets/Fotos/icono.png",
        "assets/Fotos/icono.xpm",
        "assets/Fotos/icono.bmp"
    ]
    
    for formato in formatos_icono:
        try:
            ruta_icono = resource_path(formato)
            if os.path.exists(ruta_icono):
                icono = pygame.image.load(ruta_icono)
                pygame.display.set_icon(icono)
                print(f"Icono cargado: {formato}")
                return True
        except Exception as e:
            print(f"No se pudo cargar {formato}: {e}")
    
    print("Advertencia: No se pudo cargar ningún icono")
    return False

cargar_icono()

# Sistema de partículas
particulas = []

class Particula:
    def __init__(self, x, y, tipo="brillo"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(60, 120)
        self.size = random.randint(2, 6)
        
        # Configurar propiedades según el tipo de efecto
        if tipo == "brillo":
            self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.gravity = 0.05
        elif tipo == "humo":
            self.color = (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150))
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-2, -1)
            self.gravity = -0.02
            self.size = random.randint(3, 8)
        elif tipo == "chispas":
            self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-5, -2)
            self.gravity = 0.3
        elif tipo == "estrellas":
            self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.gravity = 0.1
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-5, 5)
        else:  # confeti por defecto
            self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)])
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-8, -2)
            self.gravity = 0.2
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        if self.tipo == "estrellas":
            self.rotation += self.rotation_speed
            
        self.life -= 1
        return self.life > 0
        
    def draw(self, pantalla):
        if self.tipo == "estrellas":
            # Dibujar estrella giratoria
            points = []
            for i in range(5):
                angle = self.rotation + i * 72
                rad = math.radians(angle)
                x = self.x + math.cos(rad) * self.size
                y = self.y + math.sin(rad) * self.size
                points.append((x, y))
                
                inner_angle = angle + 36
                inner_rad = math.radians(inner_angle)
                inner_x = self.x + math.cos(inner_rad) * (self.size / 2)
                inner_y = self.y + math.sin(inner_rad) * (self.size / 2)
                points.append((inner_x, inner_y))
                
            pygame.draw.polygon(pantalla, self.color, points)
            
        elif self.tipo in ["brillo", "humo"]:
            # Efecto de desvanecimiento para brillos y humo
            alpha = min(255, int(self.life * 2))
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            if self.tipo == "brillo":
                pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
            else:  # humo
                pygame.draw.circle(surf, (*self.color, alpha // 2), (self.size, self.size), self.size)
            pantalla.blit(surf, (self.x - self.size, self.y - self.size))
            
        elif self.tipo == "chispas":
            # Chispas con cola
            tail_length = 5
            for i in range(tail_length):
                alpha = 255 - (i * 50)
                if alpha > 0:
                    pos_x = self.x - (self.vx * i * 0.5)
                    pos_y = self.y - (self.vy * i * 0.5)
                    size = max(1, self.size - i)
                    pygame.draw.circle(pantalla, (*self.color, alpha), (int(pos_x), int(pos_y)), size)
        else:
            # Confeti normal
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.size, self.size))

def crear_particulas(x, y, cantidad=50, tipo="confeti"):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo))

# Botones - DEFINIDOS GLOBALMENTE
boton_pausa_rect = pygame.Rect(ANCHO - 80, 10, 32, 32)
boton_reiniciar_rect = pygame.Rect(ANCHO - 120, 10, 32, 32)

class Serpiente:
    def __init__(self):
        self.cuerpo = [(COLUMNAS // 2, FILAS // 2)]
        self.direccion = DERECHA
        self.crecer = False
        self.color_cabeza = (0, 200, 0)
        self.color_cuerpo = (0, 150, 0)
        self.ojos_color = (255, 255, 255)
    
    def mover(self):
        cabeza_x, cabeza_y = self.cuerpo[0]
        dir_x, dir_y = self.direccion
        nueva_cabeza = (cabeza_x + dir_x, cabeza_y + dir_y)
        
        # Game over si choca con bordes
        if (nueva_cabeza[0] < 0 or nueva_cabeza[0] >= COLUMNAS or 
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= FILAS):
            return False
        
        # Game over si choca consigo misma
        if nueva_cabeza in self.cuerpo:
            return False
        
        self.cuerpo.insert(0, nueva_cabeza)
        
        if not self.crecer:
            self.cuerpo.pop()
        else:
            self.crecer = False
            
        return True
    
    def cambiar_direccion(self, nueva_direccion):
        # Evitar que se mueva en dirección opuesta
        if (nueva_direccion[0] * -1, nueva_direccion[1] * -1) != self.direccion:
            self.direccion = nueva_direccion
    
    def comer(self, puntuacion):
        self.crecer = True
        # Efecto de brillos al comer
        crear_particulas(
            self.cuerpo[0][0] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
            self.cuerpo[0][1] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
            20, "brillo"
        )
        
        # Efectos especiales según puntuación
        if puntuacion >= 100:
            crear_particulas(
                self.cuerpo[0][0] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                self.cuerpo[0][1] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                30, "estrellas"
            )
        elif puntuacion >= 50:
            crear_particulas(
                self.cuerpo[0][0] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                self.cuerpo[0][1] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                25, "chispas"
            )
        
        return True
    
    def dibujar(self, pantalla):
        for i, (x, y) in enumerate(self.cuerpo):
            rect = pygame.Rect(x * TAMANIO_CELDA, y * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA)
            
            if i == 0:  # Cabeza
                pygame.draw.rect(pantalla, self.color_cabeza, rect)
                pygame.draw.rect(pantalla, VERDE_OSCURO, rect, 2)
                
                ojo_tam = TAMANIO_CELDA // 4
                if self.direccion == DERECHA:
                    ojo1 = (rect.right - ojo_tam - 2, rect.top + ojo_tam)
                    ojo2 = (rect.right - ojo_tam - 2, rect.bottom - ojo_tam * 2)
                elif self.direccion == IZQUIERDA:
                    ojo1 = (rect.left + 2, rect.top + ojo_tam)
                    ojo2 = (rect.left + 2, rect.bottom - ojo_tam * 2)
                elif self.direccion == ARRIBA:
                    ojo1 = (rect.left + ojo_tam, rect.top + 2)
                    ojo2 = (rect.right - ojo_tam * 2, rect.top + 2)
                else:  # ABAJO
                    ojo1 = (rect.left + ojo_tam, rect.bottom - ojo_tam - 2)
                    ojo2 = (rect.right - ojo_tam * 2, rect.bottom - ojo_tam - 2)
                
                pygame.draw.circle(pantalla, self.ojos_color, ojo1, ojo_tam)
                pygame.draw.circle(pantalla, self.ojos_color, ojo2, ojo_tam)
                pygame.draw.circle(pantalla, NEGRO, ojo1, ojo_tam // 2)
                pygame.draw.circle(pantalla, NEGRO, ojo2, ojo_tam // 2)
                
            else:  # Cuerpo
                margen = 2
                cuerpo_rect = pygame.Rect(
                    x * TAMANIO_CELDA + margen, 
                    y * TAMANIO_CELDA + margen, 
                    TAMANIO_CELDA - margen * 2, 
                    TAMANIO_CELDA - margen * 2
                )
                pygame.draw.rect(pantalla, self.color_cuerpo, cuerpo_rect)
                pygame.draw.rect(pantalla, VERDE_OSCURO, cuerpo_rect, 1)

class Comida:
    def __init__(self):
        self.posiciones = []  # Cambiado a lista para múltiples manzanas
        self.color = ROJO
        self.generar_multiples_posiciones(3)  # Generar 3 manzanas iniciales
    
    def generar_nueva_posicion(self, posiciones_evitar=None):
        """Genera una sola posición válida"""
        if posiciones_evitar is None:
            posiciones_evitar = []
        
        while True:
            nueva_pos = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
            if nueva_pos not in posiciones_evitar:
                return nueva_pos
    
    def generar_multiples_posiciones(self, cantidad, posiciones_evitar=None):
        """Genera múltiples posiciones de comida"""
        if posiciones_evitar is None:
            posiciones_evitar = []
        
        nuevas_posiciones = []
        for _ in range(cantidad):
            nueva_pos = self.generar_nueva_posicion(posiciones_evitar + nuevas_posiciones)
            nuevas_posiciones.append(nueva_pos)
        
        self.posiciones = nuevas_posiciones
    
    def reemplazar_posicion(self, posicion_a_reemplazar, cuerpo_serpiente=None):
        """Reemplaza solo la manzana comida, manteniendo las otras"""
        if cuerpo_serpiente is None:
            cuerpo_serpiente = []
        
        if posicion_a_reemplazar in self.posiciones:
            # Remover la manzana comida
            self.posiciones.remove(posicion_a_reemplazar)
            
            # Generar una nueva posición que no esté en el cuerpo de la serpiente ni en las otras manzanas
            nueva_pos = self.generar_nueva_posicion(cuerpo_serpiente + self.posiciones)
            self.posiciones.append(nueva_pos)
            
            print(f"Manzana reemplazada: {posicion_a_reemplazar} -> {nueva_pos}")
    
    def dibujar(self, pantalla):
        """Dibuja todas las manzanas en sus posiciones"""
        for posicion in self.posiciones:
            x, y = posicion
            rect = pygame.Rect(x * TAMANIO_CELDA, y * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA)
            
            pygame.draw.circle(pantalla, self.color, rect.center, TAMANIO_CELDA // 2 - 2)
            
            tallo_rect = pygame.Rect(
                rect.centerx - 2, 
                rect.top + 2, 
                4, 
                6
            )
            pygame.draw.rect(pantalla, VERDE, tallo_rect)
            
            hoja_points = [
                (rect.centerx + 2, rect.top + 4),
                (rect.centerx + 6, rect.top + 2),
                (rect.centerx + 4, rect.top + 6)
            ]
            pygame.draw.polygon(pantalla, VERDE_OSCURO, hoja_points)

def dibujar_boton_reiniciar():
    color_boton = COLOR_BOTON_HOVER if boton_reiniciar_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
    color_icono = (200, 200, 200) if boton_reiniciar_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_reiniciar_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_reiniciar_rect, 2, border_radius=6)
    
    centro_x = boton_reiniciar_rect.centerx
    centro_y = boton_reiniciar_rect.centery
    radio = 8
    
    pygame.draw.circle(pantalla, color_icono, (centro_x, centro_y), radio, 2)
    
    inicio_x = centro_x + 4
    inicio_y = centro_y - 4
    
    puntos_flecha = [
        (inicio_x, inicio_y),
        (inicio_x - 3, inicio_y - 3),
        (inicio_x - 6, inicio_y)
    ]
    pygame.draw.polygon(pantalla, color_icono, puntos_flecha)

def dibujar_boton_pausa():
    color_boton = COLOR_BOTON_HOVER if boton_pausa_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
    color_icono = (200, 200, 200) if boton_pausa_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_pausa_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_pausa_rect, 2, border_radius=6)
    
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 8, boton_pausa_rect.y + 6, 4, 20))
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 20, boton_pausa_rect.y + 6, 4, 20))

def dibujar_menu_principal():
    pantalla.fill(COLOR_FONDO)
    
    # Título animado
    tiempo = pygame.time.get_ticks() / 1000
    titulo = fuente_game_over.render("SNAKE GAME", True, NEGRO)
    titulo_rect = titulo.get_rect(center=(ANCHO//2, 100))
    
    surf_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    surf_temp.blit(titulo, (0, 0))
    surf_temp.set_alpha(200 + int(math.sin(tiempo * 3) * 55))
    pantalla.blit(surf_temp, titulo_rect)
    
    # Botón jugar
    boton_jugar = pygame.Rect(ANCHO//2 - 100, 300, 200, 60)
    color_boton = (0, 200, 0) if boton_jugar.collidepoint(pygame.mouse.get_pos()) else (0, 150, 0)
    
    pygame.draw.rect(pantalla, color_boton, boton_jugar, border_radius=12)
    pygame.draw.rect(pantalla, VERDE, boton_jugar, 3, border_radius=12)
    
    texto_jugar = fuente.render("JUGAR", True, BLANCO)
    texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
    pantalla.blit(texto_jugar, texto_rect)
    
    # Instrucciones
    instrucciones = [
        "EVITA CHOCAR CON LOS BORDES Y CONTIGO MISMO",
        "USA LAS FLECHAS O WASD PARA MOVERTE",
        "COME LAS FRUTAS ROJAS PARA CRECER",
        "¡CONSIGUE LA MAYOR PUNTUACIÓN!"
    ]
    
    for i, linea in enumerate(instrucciones):
        texto = fuente_pista.render(linea, True, NEGRO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 400 + i * 25))
    
    # Efecto de partículas ocasionales
    if random.random() < 0.02:
        crear_particulas(ANCHO//2, 150, 5, "confeti")
    
    return boton_jugar

def mostrar_pausa():
    s = pygame.Surface((ANCHO, ALTO))
    s.set_alpha(200)
    s.fill((0, 0, 0))  # Fondo negro semitransparente para mejor contraste
    pantalla.blit(s, (0, 0))

    texto_pausa = fuente_game_over.render("PAUSA", True, BLANCO)
    texto_rect = texto_pausa.get_rect(center=(ANCHO//2, ALTO//2 - 50))
    pantalla.blit(texto_pausa, texto_rect)
    
    # Triángulo de play
    pygame.draw.polygon(pantalla, BLANCO, [
        (ANCHO//2 - 25, ALTO//2 + 20),
        (ANCHO//2 - 25, ALTO//2 + 60),
        (ANCHO//2 + 25, ALTO//2 + 40)
    ], 0)
    
    texto_continuar = fuente.render("Click para continuar", True, BLANCO)
    texto_rect = texto_continuar.get_rect(center=(ANCHO//2, ALTO//2 + 100))
    pantalla.blit(texto_continuar, texto_rect)

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Snake Game")
        self.reloj = pygame.time.Clock()
        
        # Fuentes compatibles con Linux
        self.fuente = self.obtener_fuente(25)
        self.fuente_grande = self.obtener_fuente(50)
        self.fuente_mediana = self.obtener_fuente(24)
        self.fuente_pista = self.obtener_fuente(20)
        
        self.reiniciar_juego()
    
    def obtener_fuente(self, tamaño):
        """Obtener fuentes compatibles con Linux"""
        fuentes_linux = [
            'dejavusans',
            'liberationsans',
            'freesans',
            None
        ]
        
        for fuente_nombre in fuentes_linux:
            try:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño)
                texto_prueba = fuente.render('Test', True, BLANCO)
                if texto_prueba.get_width() > 0:
                    return fuente
            except:
                continue
        
        return pygame.font.Font(None, tamaño)
    
    def reiniciar_juego(self):
        self.serpiente = Serpiente()
        self.comida = Comida()
        self.puntuacion = 0
        self.juego_activo = True
        self.pausa = False
        self.estado_juego = "menu"
    
    def manejar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado_juego == "menu":
                    boton_jugar = pygame.Rect(ANCHO//2 - 100, 300, 200, 60)
                    if boton_jugar.collidepoint(mouse_pos):
                        self.estado_juego = "jugando"
                        print("Iniciando juego...")
                
                elif self.estado_juego == "jugando":
                    # CORRECCIÓN: Verificar botón de pausa PRIMERO
                    if boton_pausa_rect.collidepoint(mouse_pos):
                        self.pausa = not self.pausa
                        print(f"Pausa: {self.pausa}")
                        if self.pausa:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                        # IMPORTANTE: No procesar más eventos de click aquí
                        continue
                    
                    # Luego verificar botón de reiniciar
                    elif boton_reiniciar_rect.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        print("Juego reiniciado")
                    
                    # CORRECCIÓN: Si está en pausa y hace click en cualquier lugar, quitar pausa
                    elif self.pausa:
                        self.pausa = False
                        mixer.music.unpause()
                        print("Pausa desactivada")
                
                elif self.estado_juego in ["game_over", "ganador"]:
                    boton_reiniciar = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 80, 250, 60)
                    if boton_reiniciar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        print("Reiniciando desde pantalla final")
            
            if evento.type == pygame.KEYDOWN:
                if self.estado_juego == "jugando":
                    if evento.key == pygame.K_ESCAPE:
                        self.pausa = not self.pausa
                        print(f"Pausa con ESC: {self.pausa}")
                        if self.pausa:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                    
                    elif not self.pausa:
                        if evento.key in [pygame.K_UP, pygame.K_w]:
                            self.serpiente.cambiar_direccion(ARRIBA)
                        elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                            self.serpiente.cambiar_direccion(ABAJO)
                        elif evento.key in [pygame.K_LEFT, pygame.K_a]:
                            self.serpiente.cambiar_direccion(IZQUIERDA)
                        elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                            self.serpiente.cambiar_direccion(DERECHA)
                
                # NUEVO: Reiniciar con ENTER cuando se pierde
                elif self.estado_juego == "game_over":
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        print("Reiniciando con ENTER desde Game Over")
        
        return True
    
    def actualizar(self):
        if self.estado_juego == "jugando" and not self.pausa:
            if not self.serpiente.mover():
                # Efecto de humo al perder
                crear_particulas(
                    self.serpiente.cuerpo[0][0] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                    self.serpiente.cuerpo[0][1] * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                    50, "humo"
                )
                self.estado_juego = "game_over"
                print("Game Over!")
            
            # Verificar colisión con cualquier manzana
            cabeza_serpiente = self.serpiente.cuerpo[0]
            for posicion_comida in self.comida.posiciones[:]:  # Copia de la lista para iterar
                if cabeza_serpiente == posicion_comida:
                    # La serpiente come una manzana
                    self.serpiente.comer(self.puntuacion)
                    self.puntuacion += 10
                    
                    # NUEVO: Reemplazar solo la manzana comida, mantener las otras
                    self.comida.reemplazar_posicion(posicion_comida, self.serpiente.cuerpo)
                    print(f"Puntuación: {self.puntuacion}")
                    print(f"Manzanas en pantalla: {len(self.comida.posiciones)}")
                    
                    # Ganador al llegar a 10000 puntos
                    if self.puntuacion >= 10000:
                        self.estado_juego = "ganador"
                        crear_particulas(ANCHO//2, ALTO//2, 200, "confeti")
                        print("¡Ganador!")
                    break
    
    def dibujar_bordes(self):
        borde_rect = pygame.Rect(0, 0, ANCHO, ALTO)
        pygame.draw.rect(self.pantalla, BORDE_COLOR, borde_rect, 2)
    
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        
        if self.estado_juego == "menu":
            dibujar_menu_principal()
            
        elif self.estado_juego == "jugando":
            self.serpiente.dibujar(self.pantalla)
            self.comida.dibujar(self.pantalla)
            self.dibujar_bordes()
            
            # Mostrar puntuación con fondo para mejor legibilidad
            texto_puntuacion = self.fuente.render(f'Puntuación: {self.puntuacion}', True, NEGRO)
            # Fondo semitransparente para el texto
            fondo_texto = pygame.Surface((texto_puntuacion.get_width() + 10, texto_puntuacion.get_height() + 5), pygame.SRCALPHA)
            self.pantalla.blit(fondo_texto, (5, 5))
            self.pantalla.blit(texto_puntuacion, (10, 10))
            
            # Mostrar cantidad de manzanas
            texto_manzanas = self.fuente.render(f'Manzanas: {len(self.comida.posiciones)}', True, NEGRO)
            fondo_manzanas = pygame.Surface((texto_manzanas.get_width() + 10, texto_manzanas.get_height() + 5), pygame.SRCALPHA)
            self.pantalla.blit(fondo_manzanas, (5, 40))
            self.pantalla.blit(texto_manzanas, (10, 45))
            
            # Dibujar botones
            dibujar_boton_reiniciar()
            dibujar_boton_pausa()
            
            if self.pausa:
                mostrar_pausa()
                
        elif self.estado_juego == "game_over":
            self.dibujar_pantalla_final("GAME OVER", ROJO)
            
        elif self.estado_juego == "ganador":
            self.dibujar_pantalla_final("¡GANASTE!", VERDE)
        
        # Dibujar partículas
        for particula in particulas:
            particula.draw(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_pantalla_final(self, mensaje, color):
        self.pantalla.fill(COLOR_FONDO)
        
        texto_resultado = self.fuente_grande.render(mensaje, True, color)
        texto_rect = texto_resultado.get_rect(center=(ANCHO//2, ALTO//2 - 60))
        self.pantalla.blit(texto_resultado, texto_rect)
        
        texto_puntuacion = self.fuente.render(f'Puntuación final: {self.puntuacion}', True, NEGRO)
        texto_rect = texto_puntuacion.get_rect(center=(ANCHO//2, ALTO//2))
        self.pantalla.blit(texto_puntuacion, texto_rect)
        
        # Botón reiniciar
        boton_reiniciar = pygame.Rect(ANCHO//2 - 125, ALTO//2 + 80, 250, 60)
        color_boton = (0, 200, 0) if boton_reiniciar.collidepoint(pygame.mouse.get_pos()) else (0, 150, 0)
        
        pygame.draw.rect(self.pantalla, color_boton, boton_reiniciar, border_radius=12)
        pygame.draw.rect(self.pantalla, VERDE, boton_reiniciar, 3, border_radius=12)
        
        texto_reiniciar = self.fuente.render("JUGAR DE NUEVO", True, BLANCO)
        texto_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, texto_rect)
        
        # NUEVO: Instrucción para reiniciar con ENTER
        texto_enter = self.fuente_pista.render("", True, NEGRO)
        texto_rect = texto_enter.get_rect(center=(ANCHO//2, ALTO//2 + 150))
        self.pantalla.blit(texto_enter, texto_rect)
    
    def correr(self):
        global particulas
        
        corriendo = True
        while corriendo:
            # Actualizar partículas
            particulas = [p for p in particulas if p.update()]
            
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

# Variables globales para fuentes (se inicializarán en el juego)
fuente = None
fuente_game_over = None
fuente_pista = None

def main():
    """Función principal con manejo de errores"""
    try:
        print("Iniciando Snake Game con Manzanas Persistentes")
        juego = Juego()
        
        # Hacer las fuentes globales disponibles
        global fuente, fuente_game_over, fuente_pista
        fuente = juego.fuente
        fuente_game_over = juego.fuente_grande
        fuente_pista = juego.fuente_pista
        
        juego.correr()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("Juego terminado correctamente")

if __name__ == "__main__":
    main()