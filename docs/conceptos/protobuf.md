# Qué es Protocol Buffers (protobuf)

Es un sistema creado por Google para definir esquemas de datos y serializarlos en un formato binario compacto y rápido, pensado para comunicación RPC y almacenamiento eficiente.

> La comunicación RPC (Llamada a Procedimiento Remoto, por sus siglas en inglés) es un protocolo que permite a un programa de computadora ejecutar código, funciones o procesos en otra máquina o servidor remoto, sin que el programador tenga que preocuparse por los detalles técnicos de la red.

## Ventajas principales

Mensajes compactos (menos tamaño que JSON/XML), generación de código para múltiples lenguajes y compatibilidad hacia adelante/atrás si se siguen reglas sencillas de diseño.

## Archivos .proto --- qué contienen?

Un archivo .proto es texto con una sintaxis propia donde se definen paquetes, mensajes (structs) y servicios (para gRPC).

## Reglas importantes para mantener compatibilidad

No reasignar números de campo, usar campos opcionales o repeated según convenga, y preferir añadir nuevos campos con nuevos números en lugar de modificar existentes.

## Serializar y deserializar (qué significan y cómo se usan)

- Serializar: convertir un objeto (instancia de un mensaje generado) en una secuencia de bytes compacta para enviar por red o guardar en disco.
- Deserializar: tomar esos bytes y reconstruir el objeto con sus campos.
