# Herencia

Es una forma de reutilizar código en la que una clase nueva (hija / subclase) hereda atributos y métodos de otra clase existente (padre / superclase).

- Qué se gana:
    - No se tiene que copiar y pegar el código del padre (reutilización)
    - Se puede ampliar el comportamiento en la clase hija (polimorfismo)

```python
class Animal:
    def hacer_sonido(self):
        print("Sonido genérico")

class Perro(Animal):
    def hacer_sonido(self):
        print("Guau")

p = Perro()
p.hacer_sonido()  # "Guau" (método sobrescrito)
```

# Clases abstractas y el módulo abc

- Qué es una **clase abstracta**: una clase base que no está pensada para instanciarse directamente, sino para:
    - definir un "contrato" (qué métodos debe tener cualquiera que la herede), y
    - forzar a las subclases a implementar ciertos métodos.

- En Python se hace con el módulo `abc` ("Abstract Base Class"):

- `ABC`: clase base para declarar una clase abstracta.
- `abstractmethod`: decorador que marca un método como obligatorio en las subclases.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def hacer_sonido(self):
        pass

class Perro(Animal):
    def hacer_sonido(self):
        print("Guau")

p = Perro()
p.hacer_sonido()  # "Guau" (método sobrescrito)
```

## Por qué usar clases abstractas?

- Aseguran que todas las subclases tengan el mismo conjunto de métodos (interfaz común).
- Son útiles en frameworks y librerías donde diferentes implementaciones deben cumplir el mismo contrato.

# Patrón Strategy (por qué y para qué)

- **Qué hace**: encapsula distintos "algoritmos" o formas de hacer algo en clases separadas, y permite cambiar fácilmente el comportamiento de un objeto en tiempo de ejecución.

- Estructura típica:
    - Una **clase de contexto** que usa una estrategia (por ejemplo, un método que llama a `strategy.execute()`).
    - Varias **clases de estrategia** (cada una con su propia lógica).

```python
from abc import ABC, abstractmethod

# Clase abstracta para la estrategia
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class BubbleSort(SortingStrategy):
    def sort(self, data: list) -> list:
        # ordenamiento burbuja (muy lento, solo para el ejemplo)
        return sorted(data)  # simplificado

class QuickSort(SortingStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, reverse=True)  # solo para el ejemplo

# Contexto que usa una estrategia
class DataProcessor:
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy

    def process(self, data: list) -> list:
        return self._strategy.sort(data)

# Uso (fácil de cambiar el comportamiento)
proc = DataProcessor(BubbleSort())
print(proc.process([3, 1, 2]))

proc = DataProcessor(QuickSort())  # solo cambias el objeto estrategia
print(proc.process([3, 1, 2]))
```

## Por qué usar el patrón Strategy + clases abstractas?

- Separa cómo se hace algo (estrategia) de quién lo usa (contexto).
- Se pueden agregar nuevas estrategias sin tocar el código del contexto.
- Es muy útil cuando:
    - Se tiene varios algoritmos para lo mismo (por ejemplo, distintas formas de pago, de ordenamiento, de validación, etc.).
    - Se quiere elegir el comportamiento en tiempo de ejecución (configuración, feature flags, etc.).

## Cómo se relaciona todo?

- La **herencia** permite tener una clase base y varias subclases con comportamientos diferentes.
- Las **clases abstractas** con `ABC` imponen un contrato: "todas las subclases deben implementar estos métodos".
- El **patrón Strategy** usa esa relación de herencia/abstracta para definir familias de algoritmos intercambiables (una estrategia = una clase que hereda de una clase base abstracta).
