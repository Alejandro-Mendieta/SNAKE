# 🐍 Snake Game con Botones Interactivos

Un clásico juego de Snake desarrollado en Python con Pygame, que incluye una interfaz mejorada con botones interactivos, efectos visuales y compatibilidad optimizada para Linux.

## ✨ Características Principales

### 🎮 Jugabilidad
- **Controles intuitivos**: Usa las flechas direccionales o WASD para mover la serpiente
- **Sistema de puntuación**: Gana 10 puntos por cada fruta comida
- **Condición de victoria**: Alcanza 100 puntos para ganar el juego
- **Detección de colisiones**: Game over si chocas con los bordes o contigo mismo

### 🎨 Interfaz Mejorada
- **Botones interactivos**:
  - ⏸️ Botón de pausa en la esquina superior derecha
  - 🔄 Botón de reinicio para reiniciar rápidamente
  - 🎮 Botón de jugar en el menú principal
- **Efectos visuales**:
  - Sistema de partículas para celebraciones
  - Efectos al comer frutas (brillos, chispas, estrellas)
  - Animaciones suaves y transiciones
- **Diseño responsivo**: Interfaz adaptada para 900x600 píxeles

### 🔊 Sistema de Audio
- Música de fondo en loop
- Soporte para múltiples formatos (OGG, WAV, MP3)
- Control de volumen integrado
- Pausa automática de música al pausar el juego

## 🛠️ Instalación y Requisitos

### Prerrequisitos
```bash
# Para sistemas Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-pygame

# Para sistemas basados en Arch
sudo pacman -S python python-pip python-pygame
```

### Instalación
1. Clona o descarga el proyecto
2. Navega al directorio del juego
3. Ejecuta el juego:
```bash
python3 snake_game.py
```

## 🎯 Controles

| Acción | Teclas |
|--------|--------|
| Mover arriba | `Flecha arriba` o `W` |
| Mover abajo | `Flecha abajo` o `S` |
| Mover izquierda | `Flecha izquierda` o `A` |
| Mover derecha | `Flecha derecha` o `D` |
| Pausar/Reanudar | `ESC` o click en ⏸️ |
| Reiniciar | Click en 🔄 |

## 🏆 Objetivo del Juego

1. **Controla la serpiente** y recoge las frutas rojas
2. **Evita chocar** con los bordes y con tu propio cuerpo
3. **Cada fruta** te hace crecer y suma 10 puntos
4. **¡Alcanza 100 puntos** para ganar!

## 🎨 Características Técnicas

### Compatibilidad
- ✅ **Linux** (Ubuntu, Debian, Arch, etc.)
- ✅ Múltiples formatos de audio e imágenes
- ✅ Fuentes del sistema alternativas
- ✅ Manejo robusto de errores

### Estructura del Código
- **Programación orientada a objetos**
- **Sistema de partículas modular**
- **Manejo de estados del juego** (menú, jugando, pausa, game over)
- **Gestión eficiente de recursos**

### Efectos Visuales Incluidos
- `brillo`: Efecto al comer frutas
- `chispas`: Para puntuaciones medias
- `estrellas`: Para puntuaciones altas
- `humo`: Al game over
- `confeti`: Celebración al ganar

## 🐛 Solución de Problemas

### Error de audio
```bash
# Instalar dependencias adicionales de audio
sudo apt install libsdl2-mixer-2.0-0 libsdl2-image-2.0-0
```

### El juego no inicia
- Verifica que Python 3 esté instalado
- Asegúrate de tener Pygame instalado correctamente
- Ejecuta desde la terminal para ver mensajes de error

### Problemas de rendimiento
- Ajusta la variable `FPS` en el código
- Reduce la cantidad de partículas si es necesario

## 📁 Estructura de Archivos
```
snake_game/
├── snake_game.py          # Archivo principal del juego
├── assets/
│   ├── Musica/
│   │   ├── Musica-De-Fondo.ogg
│   │   └── Musica-De-Fondo.mp3
│   └── Fotos/
│       ├── icono.png
│       └── icono.xpm
└── README.md
```

## 🚀 Personalización

Puedes modificar fácilmente:
- **Velocidad**: Cambia la variable `FPS`
- **Tamaño del tablero**: Modifica `ANCHO` y `ALTO`
- **Colores**: Ajusta las constantes de color
- **Dificultad**: Cambia la velocidad inicial o el tamaño de la serpiente

## 👨‍💻 Desarrollo
Por ALEJANDRO MENDIETA 
Creado con ❤️ usando:
- **Python 3**
- **Pygame**
- **Sistema de partículas personalizado**
- **Compatibilidad multiplataforma**

¡Disfruta del juego! 🎮