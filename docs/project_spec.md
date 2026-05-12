# FioBot -- Especificacion del Proyecto

> **Estado**: En progreso -- Completar los campos marcados con `(?)` a medida que se definan.

---

## 1. Informacion General

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | FioBot |
| **Categoria** | LARC VSSS 2026 (IEEE Very Small Size Soccer) |
| **Equipo** | (?) _Nombre del equipo_ |
| **Universidad/Institucion** | (?) _Institucion_ |
| **Repositorio** | `gabyds01/fiobot` (monorepo) |
| **Lider tecnico** | gabrields |
| **Cantidad de integrantes** | (?) _Numero de personas_ |
| **Deadline competencia** | Sin deadline establecido |

---

## 2. Hardware de los Robots

| Componente | Especificacion | Notas |
|-----------|---------------|-------|
| **Microcontrolador** | ESP32-C3 | Uno por robot |
| **Cantidad de robots** | 6 (3 en cancha + 3 spare/practica) | Para partidos locales |
| **Dimensiones max** | 8.0 cm x 8.0 cm x 8.0 cm (con ArUco) | Reglamento LARC 2026 |
| **Motores** | (?) _Paso a paso con encoders -- confirmar modelo exacto_ | 2 motores (diferencial) |
| **Motor driver** | (?) _Modelo a confirmar (TB6612/DRV8833/etc)_ | |
| **Bateria** | (?) _Tipo, voltaje, capacidad (ej: LiPo 2S 7.4V 500mAh)_ | |
| **Sensores locales** | Encoders (en motores) | Sin IMU, sin IR |
| **Mecanismo de kick** | No tiene -- solo empuje con curva frontal | |
| **Marcadores** | ArUco Original 80mm x 80mm | IDs: Azul {256, 272, 273}, Amarillo {955, 771, 939} |
| **PCB** | (?) _Custom PCB o protoboard?_ | |
| **Peso** | (?) _Peso de cada robot_ | |

---

## 3. Hardware del Bridge

| Componente | Especificacion | Notas |
|-----------|---------------|-------|
| **Microcontrolador** | ESP32 (cualquier variante) | (?) _DevKit v1? S3? C3?_ |
| **Conexion al host** | USB Serial | |
| **Funcion** | Relay puro: Serial a ESP-NOW | |
| **Protocolo inalambrico** | ESP-NOW v1.0 | Max 250 bytes/paquete |

---

## 4. Sistema de Vision

| Aspecto | Detalle |
|---------|---------|
| **Simulador** | FIRASim (externo, no en monorepo) |
| **Software de vision real** | VSS Vision Software (ArUco detection) |
| **Camara** | Webcam 1080p | (?) _Modelo exacto_ |
| **Altura de camara** | >= 2m sobre el campo |
| **Publicacion de datos** | Multicast UDP (mismo formato que FIRASim) |
| **Frecuencia** | ~60 Hz |

---

## 5. Comunicacion y Protocolos

### 5.1 Flujo de datos completo

```
+---------------+   Multicast UDP    +---------------+   WebSocket    +--------------+
| FIRASim /     | -----------------> |  Backend      | <------------> |  Panel Web   |
| VSS Vision    |  (Environment)     |  Python       |   (cmds/data)  |  (Dashboard) |
+---------------+                    |  (FastAPI)    |                +--------------+
                                     |               |
                                     |  Estrategia   |
                                     |  activa       |
                                     |               |
                                     +-------+-------+
                                             |
                     +-----------------------+
                     |                       |
             Modo Simulador          Modo Real
             (UDP commands)          (USB Serial)
                     |                       |
                     v                       v
             +---------------+       +--------------+
             |  FIRASim      |       |  ESP32 Bridge|
             |  (recv cmds)  |       |  (Serial ->  |
             +---------------+       |   ESP-NOW)   |
                                     +-------+------+
                                             | ESP-NOW
                                     +-------+-------+
                                     v       v       v
                                  Robot 0  Robot 1  Robot 2
                                 (ESP32-C3)(ESP32-C3)(ESP32-C3)
```

### 5.2 Puertos y direcciones de red

| Canal | Direccion/Puerto | Protocolo | Sentido |
|-------|-----------------|-----------|---------|
| FIRASim -> Backend (vision) | `224.0.0.1:10002` | UDP Multicast + Protobuf | Sim -> Host |
| Backend -> FIRASim (commands) | `127.0.0.1:20011` | UDP + Protobuf | Host -> Sim |
| Referee -> Backend | (?) _Puerto del VSSReferee_ | UDP Multicast + Protobuf | Ref -> Host |
| Backend -> Referee (placement) | (?) _Puerto placement_ | UDP + Protobuf | Host -> Ref |
| Backend <-> Panel Web | `ws://localhost:8000/ws` | WebSocket + JSON | Bidireccional |
| Backend -> Bridge | `/dev/ttyUSB0` (o similar) | USB Serial 115200 baud | Host -> Bridge |
| Bridge -> Robots | Canal WiFi (?) | ESP-NOW | Bridge -> Robots |
| Robots -> Bridge | Canal WiFi (?) | ESP-NOW | Robots -> Bridge (futuro) |

**Nota sobre multicast local**: Si FIRASim corre en la misma PC que el backend, el trafico
multicast puede salir por la interfaz WiFi en vez de quedarse local. Para forzar que se
quede en loopback:

```bash
ip route add 224.0.0.0/4 dev lo
```

Esto no es necesario si FIRASim corre en otra PC dentro de la misma red.

### 5.3 Protobuf -- Mensajes del simulador (VSSSProto)

#### Simulacion (paquete `fira_message`)

| Mensaje | Campos | Uso |
|---------|--------|-----|
| `Ball` | x, y, z, vx, vy, vz | Estado de la pelota |
| `Robot` | robot_id, x, y, orientation, vx, vy, vorientation | Estado de un robot |
| `Field` | width, length, goal_width, goal_depth, center_radius, penalty_width/depth/point | Dimensiones del campo |
| `Frame` | ball, robots_yellow[], robots_blue[] | Frame completo del estado del juego |
| `Environment` | step, frame, field, goals_blue, goals_yellow | Respuesta del simulador |
| `Command` | id, yellowteam, wheel_left, wheel_right | Comando a un robot |
| `Commands` | robot_commands[] | Paquete de comandos |

#### Referee (paquete `VSSRef`)

| Mensaje / Enum | Valores | Uso |
|----------------|---------|-----|
| `Foul` | FREE_KICK, PENALTY_KICK, GOAL_KICK, FREE_BALL, KICKOFF, STOP, GAME_ON, HALT | Tipo de falta/evento |
| `Color` | BLUE, YELLOW, NONE | Color del equipo |
| `Quadrant` | NO_QUADRANT, Q1, Q2, Q3, Q4 | Cuadrante de la falta |
| `Half` | FIRST_HALF, SECOND_HALF, OVERTIME_*, PENALTY_SHOOTOUTS | Tiempo del partido |
| `VSSRef_Command` | foul, teamcolor, foulQuadrant, timestamp, gameHalf | Comando del arbitro |
| `VSSRef_Placement` | Frame (robots con posiciones) | Posicionamiento del equipo |

### 5.4 Protocolo serial Host -> Bridge (propuesta)

```
Formato: Binario compacto con header
+------+------+----------+-----------+-----------+-----+
| 0xAA | LEN  | ROBOT_ID | WHEEL_L   | WHEEL_R   | CRC |
| 1B   | 1B   | 1B       | 2B int16  | 2B int16  | 1B  |
+------+------+----------+-----------+-----------+-----+

Total: 8 bytes por robot, 24 bytes para 3 robots
```

Alternativa: JSON compacto `{"id":0,"l":100,"r":-50}` (mas legible para debug)

(?) _Preferencia: binario o JSON para serial?_

### 5.5 ESP-NOW Payload (Bridge -> Robot)

| Campo | Tipo | Bytes | Descripcion |
|-------|------|-------|-------------|
| robot_id | uint8 | 1 | ID del robot destino |
| wheel_left | int16 | 2 | Velocidad rueda izquierda |
| wheel_right | int16 | 2 | Velocidad rueda derecha |
| flags | uint8 | 1 | Bits: start/stop/config_mode |
| _reservado_ | -- | 2 | Para futuras extensiones (PID params, etc.) |

**Total: 8 bytes** (bien dentro del limite de 250B de ESP-NOW)

---

## 6. Software Stack

| Componente | Tecnologia | Version |
|-----------|------------|---------|
| **Python** | Python | 3.14 |
| **Gestor de paquetes Python** | uv | latest |
| **Backend web** | FastAPI + Uvicorn | latest |
| **Frontend** | Vanilla HTML/CSS/JS | -- |
| **Comunicacion web** | WebSocket nativo | -- |
| **Serializacion (sim)** | Protobuf (protobuf Python) | proto3 |
| **Firmware robots** | C/C++ (Arduino framework) | -- |
| **Firmware build** | PlatformIO | latest |
| **ESP-NOW** | ESP-IDF ESP-NOW (via Arduino) | -- |

---

## 7. Estructura del Monorepo

```
fiobot/
|-- web/                    # Panel web (HTML/CSS/JS)
|   |-- index.html
|   |-- css/
|   |-- js/
|   +-- assets/
|-- strategy/               # Backend Python + estrategias
|   |-- pyproject.toml      # Proyecto uv
|   |-- src/
|   |   |-- server/         # FastAPI app + WebSocket
|   |   |-- strategies/     # Modulos de estrategia
|   |   |-- comms/          # Comunicacion (UDP, serial)
|   |   +-- proto/          # Protobuf generados
|   +-- tests/
|-- firmware/
|   |-- bridge/             # PlatformIO project - ESP32 Bridge
|   |   |-- platformio.ini
|   |   |-- src/
|   |   +-- include/
|   +-- robot/              # PlatformIO project - ESP32-C3 Robot
|       |-- platformio.ini
|       |-- src/
|       +-- include/
|-- proto/                  # Archivos .proto originales (subtree de VSSSProto)
|   |-- simulation/
|   +-- referee/
|-- docs/                   # Documentacion del proyecto
|   |-- conceptos/          # Documentacion teorica
|   |-- implementation_plan.md
|   +-- project_spec.md
|-- scripts/                # Scripts de utilidad
|   +-- generate_proto.sh   # Generar codigo Python desde .proto
|-- .gitignore
|-- README.md
+-- Makefile                # Comandos globales (run, build, flash, etc.)
```

---

## 8. Estrategias Disponibles

| ID | Nombre | Descripcion | Estado |
|----|--------|-------------|--------|
| 0 | `stop` | Todos los robots se detienen | Por implementar |
| 1 | `go_to_position` | Robot va a coordenada (x,y) con control simple | Por implementar |
| 2 | `follow_ball` | Robot persigue la pelota | Por implementar |
| 3 | `basic_roles` | Portero fijo + atacante + defensor dinamicos | Por implementar |
| 4 | `rl_agent` | Agente RL entrenado (PPO/SB3) | Futuro |

---

## 9. Constantes del Campo (LARC VSSS 2026)

| Parametro | Valor |
|-----------|-------|
| Area de juego | 150 cm x 130 cm |
| Piso total (con laterales) | 170 cm + 2w x 130 cm + 2w |
| Altura laterales | 5 cm |
| Espesor laterales (w) | 1.2 cm -- 2.5 cm |
| Porterias | 10 cm profundidad x 40 cm ancho |
| Circulo central (radio) | 20 cm |
| Area portero | 70 cm x 15 cm + arco 12.5 cm radio |
| Esquinas (triangulos) | 7 cm x 7 cm |
| Grosor lineas | 3 mm |
| Puntos de referencia | 0.5 cm radio (1 cm diametro) |
| Pelota | ~42.7 mm diametro, ~46g, naranja |
| Robots por equipo en cancha | 3 |
| Duracion partido | 2 x 5 min |
| Medio tiempo | 10 min |
| Cobertura pelota por robot | max 30% diametro |
| Diferencia de goles para terminar | 10 goles |

---

## 10. Direcciones MAC de los dispositivos

> Completar cuando se tengan los ESP32 listos.

| Dispositivo | MAC Address | Rol | Notas |
|------------|-------------|-----|-------|
| Bridge | (?) `XX:XX:XX:XX:XX:XX` | Relay | |
| Robot 0 | (?) `XX:XX:XX:XX:XX:XX` | Jugador | |
| Robot 1 | (?) `XX:XX:XX:XX:XX:XX` | Jugador | |
| Robot 2 | (?) `XX:XX:XX:XX:XX:XX` | Jugador | |
| Robot 3 | (?) `XX:XX:XX:XX:XX:XX` | Spare | |
| Robot 4 | (?) `XX:XX:XX:XX:XX:XX` | Spare | |
| Robot 5 | (?) `XX:XX:XX:XX:XX:XX` | Spare | |

---

## 11. Parametros de control (PID)

> Completar durante calibracion.

| Parametro | Robot 0 | Robot 1 | Robot 2 | Notas |
|-----------|---------|---------|---------|-------|
| Kp | (?) | (?) | (?) | |
| Ki | (?) | (?) | (?) | |
| Kd | (?) | (?) | (?) | |
| Max RPM | (?) | (?) | (?) | |
| Encoder CPR | (?) | (?) | (?) | Counts per revolution |
| Wheel diameter | (?) | (?) | (?) | mm |
| Wheel base | (?) | (?) | (?) | mm (distancia entre ruedas) |

---

## 12. Checklist de Datos Pendientes

- [ ] (?) Nombre del equipo
- [ ] (?) Modelo exacto del motor driver
- [ ] (?) Modelo exacto del motor + encoder (CPR)
- [ ] (?) Tipo de bateria (LiPo? voltaje? capacidad?)
- [ ] (?) Diametro de ruedas y distancia entre ellas (wheel base)
- [ ] (?) PCB custom o protoboard?
- [ ] (?) Variante ESP32 para el bridge (DevKit v1, S3, C3?)
- [ ] (?) Modelo de webcam
- [ ] (?) Puerto del VSSReferee (si se usa)
- [ ] (?) Canal WiFi preferido para ESP-NOW
- [ ] (?) Protocolo serial: binario compacto o JSON?
- [ ] (?) Peso de cada robot
- [ ] (?) MACs de todos los ESP32
- [ ] (?) Parametros PID iniciales
