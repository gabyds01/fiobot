# Clase

Una clase define un tipo de objeto: en ella se describen los atributos que puede tener y los métodos (funciones) que puede hacer.

## Atributos

Son las variables que guardan el estado de ese objeto. Pueden definirse en el `__init__` (constructor) o en cualquier método.

```python
class Personaje:
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre   # atributo
        self.edad = edad     # atributo

p = Personaje("Ana", 20)
print(p.nombre)  # -> "Ana"
```
> Aquí `nombre` y `edad` son atributos de la instancia `p`.

## Métodos

Son funciones definidas dentro de la clase y que "saben" trabajar con el estado de ese objeto.

```python
class Personaje:
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, me llamo {self.nombre} y tengo {self.edad} años.")


p = Personaje("Ana", 20)
p.saludar()  # -> "Hola, me llamo Ana y tengo 20 años."
```

## Dataclasses

Una **dataclass** es una clase pensada sobre todo para almacenar datos (registro de campos) y que genera automáticamente parte del código "repetitivo" (`__init__`, `__repr__`, `__eq__`, etc.).

Se usa el decorador `@dataclass` del módulo estándar `dataclasses` (disponible desde Python 3.7).

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: float
    y: float
    z: float

p = Punto(1.0, 2.0, 3.0)
print(p)  # -> Punto(x=1.0, y=2.0, z=3.0)
```

Aquí Punto es una dataclass: ya tiene __init__, __repr__ y __eq__ definidos por el decorador, así que no se escriben a mano.

### Ventajas de los dataclasses

- Ahorra escribir `__init__` y `__repr__` cuando el objetivo principal de la clase es almacenar valores (estructuras de datos, DTOs, mensajes de configuración, etc.).
- Se pueden añadir: comparación automática (`order=True`), valores por defecto, campos que no se usan en `__init__` (`init=False`), campos calculados con `default_factory`, etc.