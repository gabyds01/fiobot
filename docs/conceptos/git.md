# Qué es Git?

Es un sistema de control de versiones que realiza un seguimiento de los cambios en los archivos.

## Flujo de trabajo básico adoptado

- **main / master solo para código estable:** la rama principal (sea main o master) solo recibe cambios que han pasado test automáticos y revisión de código (Pull Request / Merge Request).
- **No commitear directamente a main:** el día a día se hace en ramas auxiliares (por ejemplo `dev`, `feature/...`, `fix/...`).
- **Pull Request obligatorio:** para integrar una rama a `main` siempre se abre un PR, se revisa el código y se autoriza el merge.

> Filosofía: separar el `desarrollo` (ramas secundarias) de `producción` (main).

## Sobre el formato de commits y PRs

- **Commits:**
    - Mensaje breve y claro en la primera línea, luego si hace falta una explicación más larga.
    - Algunos equipos usan convenciones como: `feat: añade autenticación`, `fix: corrige leak de memoria`, etc. (siguen "conventional commits").
- **Pull Requests:**
    - Descripción clara de qué hace el cambio, por qué y, si hay, qué issue o ticket se está cerrando.
    - Que el título sea descriptivo: por ejemplo, `Add user login form` en vez de `fix`.

## Merge vs Rebase

### Qué hace Merge?

- Combina dos ramas creando un **commit de fusión** (merge commit) que tiene dos padres: el último commit de cada rama.
- **No modifica el historial previo:** se mantiene la historia original de ambas ramas, con forma de "árboles" que se unen.

> Ejemplo típico:

```
git checkout main
git merge feature/login
```

Git crea un commit extra que une `main` con los cambios de `feature/login`.

- Cuando usar `merge`:
    - Cuando se integra cambios en ramas públicas o compartidas (por ejemplo `main` o `develop`).
    - Cuando se quiere preservar todo el historial y dejar claro "cuándo" y "de qué rama" vinieron los cambios.

> Flujo de merge:

```
# antes de merge (feature/login se bifurcó de main en B)
          main
            |
A---B---C---D
     \
      F---G---H   <-- feature/login

# después de git checkout main && git merge feature/login
# M es el merge commit, tiene dos padres: D y H
A---B---C---D-------M   <-- main
     \             /
      F---G---H---     <-- feature/login
```


### Qué hace Rebase?

- "Traslada" los commits de una rama para que se apliquen por encima del final de otra rama, reescribiendo el historial.
- El resultado es una **historia lineal y limpia**, sin commits de fusión, pero los commits originales dejan de existir (cambian de hash).

> Ejemplo típico:

```
git checkout feature/login
git rebase main
```

Git toma los commits de `feature/login` y los reaplica sobre el último commit de `main`, como si se hubieran hecho más tarde.

- Cuando usar `rebase`:
    - En ramas **privadas** (por ejemplo una rama de feature) para "limpiar" antes de hacer un merge.
    - Para actualizar la rama local con los últimos cambios de `main`, manteniendo una historia lineal.
    - **Nunca (o casi nunca) en `main` o ramas públicas o ya compartidas**, porque reescribir el historial complica la vida del resto del equipo.

> Flujo de rebase:

```
# antes de rebase (feature/login se bifurcó de main en C)
              main
                |
A---B---C---D---E
         \
          F---G   <-- feature/login

# después de git checkout feature/login && git rebase main
# main sigue apuntando a E, feature/login se "reubicó" encima de E
              main
                |
A---B---C---D---E---F'---G'   <-- feature/login

# Los commits F y G originales ya no existen,
# fueron reescritos como F' y G' (distinto hash)
```

## Pull Request (PR)

Es una petición para incorporar los cambios de una rama en otra; incluye diffs, descripción y discusión.

### Función

Facilita la revisión de código, ejecución de CI/CD, y aprobación antes del merge.

### Buenas prácticas

Escribir un título claro y una descripción que explique el qué y el por qué, enlazar issues/tickets, incluir pruebas o capturas si es útil, y mantener el PR enfocado en un único objetivo.

## Resolución de conflictos

Ocurre cuando dos cambios distintos editan las mismas líneas o el mismo área del código y Git no puede decidir automáticamente cuál conservar; Git marca las zonas en conflicto en los archivos.

### Cómo se resuelve?

Abrir los archivos conflictivos, revisar las secciones marcadas (`<<<<<<<`, `=======`, `>>>>>>>`), decidir la versión final (mantener una, combinar o reescribir), quitar las marcas, `git add` y completar el commit que resuelve el conflicto.

## Tag (etiqueta)

Es un puntero fijo a un commit concreto que marca un punto significativo (por ejemplo una release v1.0.0); es similar a una branch que no cambia.

### Tipos

- Tag ligeros (simple referencia).
- Tag anotados (incluyen metadata: autor, fecha, mensaje y pueden firmarse).

### Uso

- Marcar releases
- Facilitar rollbacks a una versión específica.
- Enlazar artefactos (builds) o changelogs a un commit exacto.

## Git stash

Es un **almacen temporal** local donde Git guarda una "captura" de los cambios (staged y no staged) sin crear commits permanentes.

### Función principal

Poder cambiar de rama o atender una urgencia sin perder el trabajo en progreso (WIP).

- Comandos útiles:
    - `git stash` o `git stash save "mensaje"` guarda los cambios y deja el working tree limpio.
    - `git stash list` muestra las entradas guardadas.
    - `git stash pop` aplica y elimina la entrada más reciente (recupera los cambios).
    - `git stash apply stash@{n}` aplica sin eliminar, `git stash drop stash@{n}` borra una entrada; `git stash clear` borra todas las entradas.

## .gitignore

Es un archivo de texto (normalmente en la raíz del repo) que le dice a Git qué archivos o carpetas debe ignorar (no hacer add ni track).

### Función principal

Mantener el repositorio limpio evitando subir archivos generados, secretos o dependencias que no deben versionarse.

## Cherry pick

Toma un cambio introducido por un commit (o una serie de commits) y lo aplica como un nuevo commit en la rama actual.

### Función típica

Extraer un `fix` o una mejora puntual de otra rama sin traer todo el historial ni hacer merge de esa rama completa.

## Git reset

Mueve el puntero de **HEAD** a otro commit y (según la opción) cambia el índice y/o el working tree; en la práctica "borra" commits posteriores en el historial local.

- Modos comunes:
    - `--soft <commit>`: mueve HEAD pero mantiene los cambios en staging (index).
    - `--mixed <commit>` (por defecto): mueve HEAD y deja los cambios en el working tree (no staged).
    - `--hard <commit>`: mueve HEAD y reestablece índice y working tree a ese commit (se pierden cambios no guardados).

### Cuándo usarlo?

Para corregir commits recientes en la copia local (reordenar, combinar o descartar commits) antes de compartirlos; útil durante limpieza local.

## Git revert

Crea un nuevo commit que aplica la inversa de un commit objetivo, de modo que el efecto de un commit original queda deshecho, pero el historial permanece intacto.

