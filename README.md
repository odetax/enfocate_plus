# 🧠 ENFÓCATE+

> Plataforma de minijuegos cognitivos diseñada para personas con TDAH.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Justificación](#-justificación)
- [Objetivos](#-objetivos)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Juegos Incluidos](#-juegos-incluidos)
- [Guía para Equipos: Contrato de Integración](#-guía-para-equipos-contrato-de-integración)
- [Convenciones de Código](#-convenciones-de-código)
- [Gestión de Recursos (Assets)](#-gestión-de-recursos-assets)
- [Patrón de Diseño: Facade](#-patrón-de-diseño-facade)
- [Estándares de Diseño](#-estándares-de-diseño)
- [Contribución](#-contribución)
- [Equipo de Integración](#-equipo-de-integración)
- [Créditos](#-créditos)

---

## 📖 Descripción

**ENFÓCATE+** es una plataforma unificada de minijuegos diseñada específicamente para estimular las capacidades cognitivas de personas con TDAH (Trastorno por Déficit de Atención e Hiperactividad). Ofrece un entorno digital libre de distracciones y altamente intuitivo para entrenar la concentración y la memoria.

---

## 💡 Justificación

Las personas con TDAH a menudo enfrentan desafíos con la función ejecutiva y la atención sostenida. El software educativo tradicional suele ser aburrido o, por el contrario, los videojuegos comerciales suelen ser demasiado caóticos y sobreestimulantes.

Este proyecto busca un equilibrio al utilizar Python para crear una herramienta que sea **entretenida pero estructurada**, convirtiendo el tiempo de pantalla en tiempo de entrenamiento cognitivo útil.

---

## 🎯 Objetivos

**Objetivo General:**
* Diseñar, desarrollar e integrar 11 juegos adaptados a las necesidades de personas con TDAH en una aplicación de escritorio programada en Python.

**Objetivos Específicos:**
- **Accesibilidad Cognitiva:** Interfaces limpias, sin sobreestimulación (evitar parpadeos excesivos o sonidos estridentes).
- **Consistencia Técnica:** Lograr que los 11 juegos funcionen bajo un mismo menú sin errores.
- **Modularidad:** Cada juego es una pieza independiente que se integra al sistema central.

---

## 💻 Requisitos del Sistema

| Requisito | Detalle |
|-----------|---------|
| Python | 3.11 – 3.13 |
| Biblioteca gráfica | Pygame |
| FPS Objetivo | 60 FPS |

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio principal
git clone <URL_DEL_REPOSITORIO>
cd proyecto_enfocate_plus

# 2. Inicializar y actualizar los submódulos (juegos)
git submodule update --init --recursive

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python main.py
```

> ⚠️ Si agregas un nuevo submódulo de juego, asegúrate de correr `git submodule update --init` para que los demás puedan descargarlo.

---

## 📁 Estructura del Proyecto

```
proyecto_enfocate_plus/
│
├── .gitignore
├── .gitmodules               # Registro de todos los submódulos (juegos)
├── requirements.txt          # Librerías necesarias
├── README.md                 # Este archivo
├── main.py                   # Punto de entrada: menú principal
├── engine.py                 # Configuraciones globales (colores, fuentes, rutas)
├── assets/                   # Recursos compartidos (logo, fuentes, UI común)
│
│
├── ui/
│   ├── base.py
│   ├── components.py
│   └── screen.py
│
├── core/
│   ├── managers/
│   │   ├── asset_manager.py
│   │   └── sound_player.py
│   │
│   └── settings.py
│   
└── games/                    # Carpeta contenedora de todos los juegos
    ├── __init__.py
    │
    ├── equipo_01_nombre/     # Submódulo: Juego del Equipo 1
    │   ├── main.py           # Punto de entrada del juego (Facade)
    │   └── assets/           # Recursos exclusivos de este juego
    │
    ├── equipo_02_nombre/     # Submódulo: Juego del Equipo 2
    │   ├── main.py
    │   └── assets/
    │
    └── ...                   # Hasta el equipo 11
```

---

## 🎮 Juegos Incluidos

| # Equipo | Juego |
|---|-------|
| 01 | Maze: Light Trace |
| 02 | Crash |
| 03 | Encontrar las Diferencias |
| 04 | Keep The Cadence |
| 05 | Purely Place |
| 06 | Sokoban |
| 07 | Osu Legacy |
| 08 | ColorFusion |
| 09 | Memoria |
| 10 | Pescar Al Salmón |
| 11 | Pomodo Tower Defense |
| 12 | Disk Sort Puzzle |

---

## 📜 Guía para Equipos: Contrato de Integración

Estas reglas son **obligatorias** para que todos los juegos funcionen correctamente dentro de la plataforma.

### ✅ El archivo principal debe llamarse `main.py`

Cada equipo debe tener un archivo `main.py` en la raíz de su carpeta. Este archivo es la **única puerta de entrada** al juego.

```python
# games/equipo_01_nombre/main.py

def run(screen, clock):
    """
    Función principal del juego.
    Recibe la pantalla y el reloj del menú principal.
    Debe hacer return al terminar (NO sys.exit).
    """
    # ... lógica del juego ...
    return  # Vuelve al menú principal
```

### ❌ Prohibido: `sys.exit()` o `quit()`

Estas funciones cierran **toda la aplicación**. Cuando el juego termine, siempre usar `return`.

```python
# ❌ MAL
pygame.quit()
sys.exit()

# ✅ BIEN
return  # Regresa al menú principal
```

### ❌ Prohibido: Crear una nueva ventana

La ventana (`pygame.display.set_mode`) la crea el menú principal. Los juegos **reciben** la pantalla como parámetro, no crean una nueva.

```python
# ❌ MAL
screen = pygame.display.set_mode((800, 600))

# ✅ BIEN
def run(screen, clock):  # La pantalla llega como parámetro
    ...
```

### ❌ Prohibido: Variables globales

Todo debe estar encapsulado en funciones o clases para evitar conflictos entre equipos.

```python
# ❌ MAL
global puntos
puntos = 0

# ✅ BIEN
class Game:
    def __init__(self):
        self.puntos = 0
```

---

## 🖊️ Convenciones de Código

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Idioma (código) | Inglés | `calculate_score`, `user_list` |
| Idioma (comentarios/docs) | Español | `# Calcula el puntaje del jugador` |
| Clases | CamelCase | `GameManager`, `MemoryGame` |
| Variables y Métodos | snake_case | `calcular_puntaje`, `lista_usuarios` |
| Constantes | MAYÚSCULAS | `COLOR_FONDO`, `MAX_LIVES` |

---

## 🗂️ Gestión de Recursos (Assets)

### Rutas: Siempre relativas

```python
# ❌ MAL — ruta absoluta, no funciona en otra computadora
image = pygame.image.load("C:/Users/Jose/Proyecto/imagen.png")

# ✅ BIEN — ruta relativa con pathlib
from pathlib import Path
BASE_DIR = Path(__file__).parent
image = pygame.image.load(BASE_DIR / "assets" / "imagen.png")
```

### Formatos estándar

**Imágenes:**
- `.png` → todos los elementos del juego (personajes, UI, ítems). Conserva transparencia.
- `.jpg` → solo para fondos estáticos grandes.
- Nombres en `minusculas_y_guiones_bajos.png`

**Audio:**
- `.wav` / `.ogg` → efectos sonoros cortos.
- `.ogg` → música de fondo larga.

---

## 🏛️ Patrón de Diseño: Facade

Cada juego implementa el patrón **Facade**: el archivo `main.py` actúa como interfaz simplificada hacia toda la lógica interna del juego.

```
menú principal
      │
      ▼
games/equipo_01/main.py   ← Facade (interfaz simple)
      │
      ├── game_logic.py
      ├── renderer.py
      ├── entities.py
      └── ...             ← Complejidad interna oculta
```

El `main.py` del equipo **solo** importa e inicia el juego. No contiene lógica de juego directamente.

---

## 🎨 Estándares de Diseño

- **Tecla ESC:** Siempre debe pausar o volver al menú principal.
- **Textos:** Evitar textos largos; preferir íconos visuales.
- **Estimulación:** Sin parpadeos excesivos ni sonidos estridentes.
- **Paleta de colores:** Usar colores del `config.py` global para mantener consistencia visual.

---

## 🤝 Contribución

### Flujo de trabajo con submódulos Git

Cada equipo trabaja en su propio repositorio (submódulo). El repositorio principal solo registra a qué commit apunta cada juego.

```bash
# Dentro de tu carpeta de juego (submódulo):
git add .
git commit -m "feat: descripción del cambio"
git push origin main

# Desde el repositorio principal, actualizar la referencia del submódulo:
cd ../..  # volver a la raíz del proyecto
git add games/equipo_01_nombre
git commit -m "chore: actualizar submódulo equipo 01"
git push
```

### Checklist antes de hacer push

- [ ] El archivo principal se llama `main.py` y tiene la función `run(screen, clock)`
- [ ] No se usa `sys.exit()`, `quit()`, ni `pygame.display.set_mode()`
- [ ] No hay variables globales
- [ ] Todos los assets usan rutas relativas con `pathlib` o `os`
- [ ] Los archivos de imagen son `.png` o `.jpg`
- [ ] Los archivos de audio son `.wav` u `.ogg`
- [ ] La tecla ESC regresa al menú o pausa el juego
- [ ] El código sigue las convenciones de nombres

---

## 👥 Equipo de Integración

* Alejandro Capriles

* Alexandro Núñez

* Anelissa Espín

* Gabriel Garantón

* José Aguilera

* Leonardo Di Giorgio

* Luis Lameda

* Odett Sayegh

---

## 🏫 Créditos

Este proyecto fue desarrollado como **trabajo final** de la materia **Objetos y Abstracción de Datos**.

| | |
|---|---|
| 🎓 **Institución** | Universidad de Oriente — Núcleo Anzoátegui |
| 📚 **Materia** | Objetos y Abstracción de Datos |
| 👨‍🏫 **Profesor** | Ing. Plácido Malavé |

---
<p align="center">Hecho con 💙 para apoyar a personas con TDAH</p>
