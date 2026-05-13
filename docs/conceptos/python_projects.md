# pyproject.toml

Es un archivo en formato TOML que vive en la raíz del proyecto y centraliza metadata del proyecto, dependencias, requisitos del sistema de build y la configuración de herramientas (linters, formatters, test runners).

## Por qué usarlo?

Reemplaza y unifica lo que antes se repartía entre setup.py, setup.cfg, requirements.txt y varios archivos de configuración, y es el formato recomendado por las PEPs (PEP 518/621).

## Contenido típico

Una tabla [project] con nombre, versión y dependencias; una sección [build-system] para declarar la herramienta de build (por ejemplo setuptools o poetry); y secciones para configuraciones de herramientas (black, pytest, etc.).

# uv

Es una herramienta moderna que agrupa gestión de entornos virtuales y de dependencias (sustituyendo o complementando pip, virtualenv/venv y algunos flujos de pip-tools), diseñada para ser muy rápida.

## Qué hace en la práctica?

Crea entornos virtuales, instala y quita paquetes, actualiza pyproject.toml y genera/actualiza un lockfile (por ejemplo uv.lock) para reproducibilidad, y facilita tareas comunes de gestión de proyectos Python.

### Cómo instalar dependencias?

- Crear/usar entorno: `uv venv` crea un entorno virtual para el proyecto.
- Añadir dependencia de ejecución: `uv add <paquete>` (actualiza pyproject.toml y uv.lock).
- Añadir dependencia de desarrollo: `uv add --dev <paquete>` para herramientas como linters, formatters o test runners.
- Instalar desde lockfile o requirements: `uv sync` instala todo lo que figura en pyproject.toml y uv.lock.

# Entornos virtuales

Son entornos aislados que contienen una instalación de Python y paquetes separados del sistema global, para que cada proyecto tenga sus propias dependencias y versiones sin interferir entre sí.

## Por qué utilizarlos?

Por que evitan conflictos entre proyectos, facilitan reproducibilidad y permiten controlar versiones exactas de bibliotecas.

# Makefile

Es un archivo de texto llamado `Makefile` con reglas en la forma `target: deps` seguido de líneas de shell que se ejecutan si se quiere ese target.

Para ejecutar, en la terminal se pone `make target` (por ejemplo `make dev`).

Los targets pueden ser "falsos" (phony) si no crean archivos con ese nombre; se marca con `.PHONY` para evitar conflictos con archivos del mismo nombre.
