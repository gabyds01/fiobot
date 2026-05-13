# FioBot -- Plan de Implementacion

## Resumen

Este documento define los objetivos a cumplir para construir el proyecto FioBot.
Esta organizado en fases incrementales. Cada fase tiene objetivos concretos con
criterios de verificacion.

El MVP prioriza la integracion con el simulador FIRASim antes de pasar a robots reales.

Ver `project_spec.md` para las especificaciones tecnicas completas.

---

## Arquitectura del Sistema

```
+---------------+   Multicast UDP    +---------------+   WebSocket    +--------------+
| FIRASim /     | -----------------> |  Backend      | <------------> |  Panel Web   |
| VSS Vision    |  (Environment)     |  Python       |   (cmds/data)  |  (Dashboard) |
+---------------+  224.0.0.1:10002   |  (FastAPI)    |                +--------------+
                                     |               |
                                     |  Estrategia   |
                                     |  activa       |
                                     +-------+-------+
                                             |
                     +-----------------------+
                     |                       |
             Modo Simulador          Modo Real
          (UDP 127.0.0.1:20011)    (USB Serial)
                     |                       |
                     v                       v
             +---------------+       +--------------+
             |  FIRASim      |       |  ESP32 Bridge|
             +---------------+       +------+-------+
                                            | ESP-NOW
                                     +------+------+
                                     v      v      v
                                    R0     R1     R2
                                  (ESP32-C3 cada uno)
```

---

## Fase 1: Fundacion del Monorepo

### Objetivo 1.1 -- Crear la estructura de directorios

Crear la estructura completa del monorepo segun la seccion 7 del `project_spec.md`.
No hace falta que tengan contenido real todavia, pero si que existan los directorios
y archivos placeholder donde corresponda.

**Verificacion**: La estructura del repositorio coincide con el diagrama del spec.

### Objetivo 1.2 -- Agregar VSSSProto como subtree

Agregar los archivos `.proto` del repositorio VSSSLeague/VSSSProto al directorio `proto/`.
Se puede usar `git subtree` o simplemente copiar los archivos necesarios.

Los archivos necesarios estan en:
- `simulation/`: command.proto, common.proto, packet.proto, replacement.proto
- `referee/`: vssref_command.proto, vssref_common.proto, vssref_placement.proto

**Verificacion**: Los archivos `.proto` existen en `proto/simulation/` y `proto/referee/`.

### Objetivo 1.3 -- Inicializar el proyecto Python con uv

Crear `strategy/pyproject.toml` con las dependencias:
- `fastapi`
- `uvicorn[standard]`
- `websockets`
- `pyserial`
- `protobuf`

Inicializar el entorno con `uv sync`.

**Conceptos teoricos necesarios**: Ver `docs/conceptos/python_projects.md`

**Verificacion**: `uv sync` instala las dependencias sin errores.

### Objetivo 1.4 -- Script de generacion de protobuf

Crear `scripts/generate_proto.sh` que ejecute `protoc` para generar los bindings
Python desde los archivos `.proto` y los coloque en `strategy/src/proto/`.

**Verificacion**: `bash scripts/generate_proto.sh` genera archivos `_pb2.py` en
`strategy/src/proto/`.

### Objetivo 1.5 -- Makefile con comandos globales

Crear un `Makefile` en la raiz con al menos:
- `make dev` -> Inicia el backend FastAPI
- `make proto` -> Genera protobuf Python

Mas adelante se agregaran targets para firmware.

**Verificacion**: `make dev` levanta el servidor, `make proto` genera los protobuf.

### Objetivo 1.6 -- Actualizar .gitignore y README

- Actualizar `.gitignore` para cubrir Python (__pycache__, .venv, etc.), PlatformIO
  (.pio, .vscode), protobuf generados, y archivos del sistema.
- Actualizar `README.md` con una descripcion basica del proyecto y como empezar.

**Verificacion**: Los archivos generados y temporales no se trackean en git.

---

## Fase 2: Backend + Integracion con Simulador

### Objetivo 2.1 -- Receptor UDP (leer del simulador)

Crear `strategy/src/comms/udp_receiver.py`:
- Una clase que se suscriba al multicast `224.0.0.1:10002`
- Decodifique los mensajes protobuf `Environment`
- Extraiga el `Frame` con posiciones de robots y pelota
- Publique el estado en una estructura accesible por el resto del programa

**Conceptos teoricos necesarios**: Ver `docs/conceptos/udp_multicast.md`,
`docs/conceptos/protobuf.md`

**Verificacion**: Con FIRASim corriendo, el receptor imprime las posiciones de los
robots y la pelota en consola.

### Objetivo 2.2 -- Emisor UDP (enviar al simulador)

Crear `strategy/src/comms/udp_sender.py`:
- Una clase que envie mensajes protobuf `Commands` a `127.0.0.1:20011`
- Recibe una lista de comandos `(robot_id, wheel_left, wheel_right)` y los serializa

**Verificacion**: Enviando un comando con wheel_left=10, wheel_right=10, el robot
avanza en linea recta en FIRASim.

### Objetivo 2.3 -- Estado del juego

Crear `strategy/src/engine/game_state.py`:
- Una clase `GameState` que represente el estado actual del juego
- Posiciones y velocidades de todos los robots (ambos equipos)
- Posicion y velocidad de la pelota
- Score, dimensiones del campo

**Conceptos teoricos necesarios**: Ver `docs/conceptos/dataclasses.md`

**Verificacion**: El GameState se actualiza correctamente con cada frame del simulador.

### Objetivo 2.4 -- Clase base de estrategia

Crear `strategy/src/strategies/base.py`:
- Una clase abstracta `BaseStrategy` con:
  - Atributos: `name`, `description`, `parameters` (dict de parametros ajustables)
  - Metodo abstracto: `compute(state: GameState) -> list[RobotCommand]`
  - Metodos opcionales: `on_activate()`, `on_deactivate()`

Todas las estrategias futuras heredaran de esta clase.

**Conceptos teoricos necesarios**: Ver `docs/conceptos/clases_abstractas.md`

**Verificacion**: No se puede instanciar `BaseStrategy` directamente (da error).

### Objetivo 2.5 -- Estrategia "stop"

Crear `strategy/src/strategies/stop.py`:
- Hereda de `BaseStrategy`
- `compute()` retorna velocidad (0, 0) para todos los robots

**Verificacion**: Al activar esta estrategia, todos los robots se detienen en FIRASim.

### Objetivo 2.6 -- Estrategia "go_to_position"

Crear `strategy/src/strategies/go_to_position.py`:
- Hereda de `BaseStrategy`
- Dado un target (x, y), calcula el angulo hacia el target
- Genera velocidades diferenciales para llegar al punto
- Parametros ajustables: `target_x`, `target_y`, `max_speed`, `Kp_angular`

**Verificacion**: Un robot se mueve hacia la posicion objetivo en FIRASim.

### Objetivo 2.7 -- Estrategia "follow_ball"

Crear `strategy/src/strategies/follow_ball.py`:
- Hereda de `BaseStrategy`
- Cada robot persigue la posicion actual de la pelota
- Usa la misma logica de go_to_position pero con target = posicion de la pelota

**Verificacion**: Los robots persiguen la pelota en FIRASim.

### Objetivo 2.8 -- Motor de estrategias

Crear `strategy/src/engine/strategy_engine.py`:
- Clase `StrategyEngine` que:
  - Recibe el `GameState` del receptor UDP
  - Ejecuta la estrategia activa
  - Envia los comandos resultantes al emisor correspondiente (UDP para sim)
  - Permite cambiar la estrategia activa en caliente
  - Registra las estrategias disponibles automaticamente

**Verificacion**: Se puede cambiar de estrategia sin reiniciar el backend.

### Objetivo 2.9 -- Servidor FastAPI basico

Crear `strategy/src/server/app.py`:
- App FastAPI que:
  - Levanta el StrategyEngine al iniciar
  - Endpoint `GET /api/strategies` -> lista de estrategias disponibles
  - Endpoint `GET /api/status` -> estado actual (estrategia activa, modo, conexion)
  - Sirve archivos estaticos de `web/` en la raiz `/`

**Conceptos teoricos necesarios**: Ver `docs/conceptos/fastapi_basics.md`

**Verificacion**: `make dev` levanta el servidor, las APIs responden correctamente.

### Objetivo 2.10 -- WebSocket endpoint

Agregar a la app FastAPI:
- Endpoint WebSocket `ws://localhost:8000/ws`
- Envia el game state al panel cada frame (~60Hz, o throttled a 30Hz)
- Recibe comandos del panel (start, stop, cambiar estrategia, actualizar parametros)
- Formato de mensajes: JSON

**Conceptos teoricos necesarios**: Ver `docs/conceptos/websockets.md`

**Verificacion**: Un cliente WebSocket (puede ser desde el navegador con la consola JS)
recibe datos del juego y puede enviar comandos.

---

## Fase 3: Panel Web (Dashboard)

### Objetivo 3.1 -- Estructura HTML base

Crear `web/index.html`:
- Layout con sidebar (controles) y area principal (canvas del campo)
- Cargar fuentes (Google Fonts - Inter o similar)
- Dark theme

**Verificacion**: La pagina carga correctamente desde `http://localhost:8000/`.

### Objetivo 3.2 -- Estilos CSS

Crear `web/css/index.css`:
- Design system con variables CSS (colores, spacing, tipografia)
- Dark theme por defecto
- Estilos para botones, cards, dropdowns, indicadores de estado

**Verificacion**: La interfaz se ve limpia y profesional.

### Objetivo 3.3 -- Conexion WebSocket desde JS

Crear `web/js/websocket.js`:
- Clase `FioBotSocket` que:
  - Se conecta al backend WebSocket
  - Reconecta automaticamente si se cae la conexion
  - Expone metodos para enviar comandos
  - Dispara callbacks cuando llegan datos

**Verificacion**: El indicador de conexion muestra "conectado" y se actualiza el estado.

### Objetivo 3.4 -- Visualizacion del campo

Crear `web/js/field_renderer.js`:
- Clase `FieldRenderer` que usa un Canvas 2D para:
  - Dibujar el campo a escala (con lineas, areas, circulo central)
  - Renderizar robots como flechas/circulos con orientacion
  - Renderizar la pelota
  - Actualizar a ~30fps

**Verificacion**: Se ven los robots y la pelota moviendose en tiempo real en el canvas.

### Objetivo 3.5 -- Controles basicos

Crear `web/js/controls.js`:
- Boton Start/Stop
- Dropdown para seleccionar estrategia
- Formulario dinamico que muestra los parametros de la estrategia activa y permite
  modificarlos

**Verificacion**: Cambiar estrategia y modificar parametros desde el panel afecta el
comportamiento de los robots en FIRASim.

### Objetivo 3.6 -- Inicializacion de la app

Crear `web/js/app.js`:
- Conecta todos los modulos: WebSocket, FieldRenderer, Controls
- Maneja el ciclo de vida de la aplicacion

**Verificacion**: Todo funciona integrado: ver campo, cambiar estrategia, start/stop.

---

## Fase 4: Comunicacion Fisica (Bridge + Robots)

### Objetivo 4.1 -- Emisor serial (Python)

Crear `strategy/src/comms/serial_sender.py`:
- Clase `SerialSender` que:
  - Abre un puerto serial configurable
  - Serializa comandos de robot en el formato binario definido en el spec
  - Detecta desconexion y reconecta automaticamente

**Verificacion**: Se pueden enviar bytes al puerto serial y verificar con un monitor.

### Objetivo 4.2 -- Firmware del bridge

Crear proyecto PlatformIO en `firmware/bridge/`:
- `platformio.ini` con la configuracion del ESP32 elegido
- `src/main.cpp` que:
  - Lee bytes del Serial
  - Parsea los paquetes (header, payload, CRC)
  - Reenvia el payload correspondiente a cada robot por ESP-NOW
  - Reporta estado via Serial (opcional)

**Verificacion**: El bridge recibe paquetes por Serial y los reenvia por ESP-NOW
(verificable con un segundo ESP32 en modo monitor).

### Objetivo 4.3 -- Firmware del robot

Crear proyecto PlatformIO en `firmware/robot/`:
- `platformio.ini` con ESP32-C3
- Modulos:
  - Recepcion ESP-NOW
  - Control de motores (PWM + direccion)
  - Lectura de encoders (interrupciones)
  - PID controller por motor
  - Safety timeout (para motores si no recibe mensajes en >500ms)

**Verificacion**: El robot recibe comandos y mueve los motores con PID. Se detiene
automaticamente si pierde comunicacion.

---

## Fase 5: Integracion Modo Dual (Sim/Real)

### Objetivo 5.1 -- Switch de modo desde panel web

Modificar el backend y el panel para:
- Toggle Sim/Real que cambia el canal de salida de comandos
- En modo simulador: enviar por UDP a FIRASim
- En modo real: enviar por Serial al bridge
- Indicador visual del modo actual

**Verificacion**: Cambiar el toggle redirige los comandos al canal correcto.

### Objetivo 5.2 -- Tuning de PID via OTA

- Desde el panel web se pueden modificar los valores de PID
- El backend envia un paquete especial (flag CONFIG_MODE) al bridge
- El bridge lo reenvia al robot correspondiente
- El robot actualiza sus PID controllers en runtime

**Verificacion**: Modificar PID desde el panel cambia el comportamiento del motor.

---

## Fase 6: Avanzado (Post-MVP)

### Objetivo 6.1 -- Estrategia con roles

Estrategia `basic_roles` con portero fijo, atacante que persigue pelota, defensor
que cubre el arco. Posicionamiento automatico para jugadas.

### Objetivo 6.2 -- Integracion con VSSReferee

Recibir y reaccionar a comandos del arbitro automatico (STOP, GAME_ON, KICKOFF, etc.).

### Objetivo 6.3 -- Agente RL

Importar modelos entrenados con Stable Baselines3 como estrategia seleccionable.

### Objetivo 6.4 -- Match state manager

Tracking de score, tiempo, faltas, historial, y grabacion de replay.

---

## Documentacion Teorica

A medida que se avance en los objetivos, se creara documentacion teorica en
`docs/conceptos/`. Estos documentos explican los conceptos de programacion
utilizados, pensados para que cualquier integrante del equipo pueda entenderlos.

Algunos conceptos son transversales a todas las fases (como git) y se deben
dominar desde el inicio. Otros son especificos de cada fase y se pueden aprender
a medida que se necesiten.

Documentos planificados:

| Documento | Se necesita en | Temas |
|-----------|---------------|-------|
| `git.md` | Todas | Commits convencionales, ramas (branching model), merge vs rebase, pull requests, resolusion de conflictos, tags, .gitignore, stash, cherry-pick, reset vs revert, buenas practicas para trabajo en equipo |
| `python_projects.md` | Fase 1 | Que es pyproject.toml, que es uv, como instalar dependencias, entornos virtuales |
| `protobuf.md` | Fase 1-2 | Que es protobuf, archivos .proto, como generar codigo, serializar/deserializar |
| `udp_multicast.md` | Fase 2 | Que es UDP, que es multicast, sockets en Python, diferencia con TCP |
| `dataclasses.md` | Fase 2 | Que es una clase, atributos, metodos, dataclasses en Python |
| `clases_abstractas.md` | Fase 2 | Herencia, clases abstractas, ABC, por que usarlas (Strategy Pattern) |
| `fastapi_basics.md` | Fase 2 | Que es una API REST, endpoints, que es ASGI, async/await basico |
| `websockets.md` | Fase 2-3 | Que es WebSocket, diferencia con HTTP, como usarlo en JS y Python |
| `esp_now.md` | Fase 4 | Que es ESP-NOW, como funciona, MACs, peers, callbacks |
| `pid_control.md` | Fase 4 | Que es PID, Kp/Ki/Kd, anti-windup, tuning basico |
| `platformio.md` | Fase 4 | Que es PlatformIO, platformio.ini, como compilar y flashear |
