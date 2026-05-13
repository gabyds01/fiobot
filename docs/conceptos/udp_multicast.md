# UDP (User Datagram Protocol)

Es un protocolo de la capa de transporte (capa 4) del modelo OSI que envía datagramas independientes sin establecer una conexión previa, por lo que no hay handshakes, retransmisiones automáticas ni control de flujo.

## Ventajas

Baja latencia, menos overhead y simpleza; ideal para streaming, voice/video en tiempo real, DNS y casos donde perder paquetes es tolerable.

## Desventaja

No garantiza que los paquetes lleguen, ni que lleguen en orden, ni que no se dupliquen; si se necesita fiabilidad se debe implementar en la capa de aplicación.

# Multicast

Es un mecanismo de direccionamiento que permite enviar un único paquete a un grupo de receptores interesados (direcciones IP de multicast, p. ej. 224.0.0.0/4 para IPv4).

## Uso típico

Distribución de audio/video en red local, descubrimiento de servicios y algunos protocolos de sincronización donde muchos hosts deben recibir los mismos mensajes sin enviar copias separadas al emisor.

## Requisitos/limitaciones

Necesita soporte de red (routers/switches) para reenviar paquetes multicast entre subredes; en redes no configuradas, el multicast puede funcionar solo en la LAN local.

# Sockets en python

La librería estándar socket expone una API para crear sockets UDP (SOCK_DGRAM) y TCP (SOCK_STREAM). Ejemplos mínimos:

> Crear socket UDP y enviar:

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b"hola", ("192.0.2.1", 12345))
```

> Crear socket UDP y recibir:

```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 12345))
data, addr = s.recvfrom(4096)
```

### Diferencias clave con TCP

- Conexión: TCP es orientado a conexión (handshake); UDP es sin conexión.
- Fiabilidad: TCP garantiza entrega, orden y retransmisión; UDP no.
- Overhead y latencia: TCP añade control (más overhead) y puede introducir latencia por retransmisiones; UDP es más liviano y con menor latencia potencial.
- Uso: TCP para transferencias fiables (HTTP, bases de datos, ficheros), UDP para tiempo real o sencillez (DNS, VoIP, streaming, juegos donde se prioriza la frescura de la información).
