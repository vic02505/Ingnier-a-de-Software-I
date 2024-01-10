# **Cómo contribuir**

Para este proyecto, en su mayoría se tratan de seguir las convenciones del lenguaje Python
([PEP8](https://peps.python.org/pep-0008/)) en la medida de lo posible. Algunos casos quedan aquí
explícitos, así como también excepciones a los mismos acordadas en el grupo.

<u>Dichas convenciones deberían seguirse y pueden ser motivo de
rechazar un *Pull Request*.</u>

<hr width="30%" align="left" />

# Índice

- [Definiciones](#definiciones)

- [Código Fuente](#código-fuente)

    * [*Type Hints*](#type-hints)

    * [Funciones](#funciones)

        - [Nombres](#nombres)
        - [Parámetros](#parámetros)
        - [*docstrings*](#docstrings)

    * [Constantes](#constantes)

    * [Clases](#clases)

    * [Imports](#imports)

    * [Archivos](#archivos)

    * [Espaciado](#espaciado)

        - [*Type Hints*](#espaciado-con-respecto-a-type-hints)
        - [Declaración de Variables](#espaciado-en-declaración-de-variables)
        - [Funciones](#espaciado-en-funciones)
            * [Parámetros en Funciones](#espaciado-de-parámetros-en-funciones)
            * [Después de *docstrings*](#espaciado-después-de-docstrings-en-funciones)
        - [*imports*/Constantes](#espaciado-de-imports-y-constantes-globales)
        - [Final de Archivos](#espaciado-al-final-de-archivos)

    * [Estructura de Tests](#estructura-de-tests)

- [*Pull Requests*](#pull-requests)
    * [Motivación](#motivación)
    * [Cambios Hechos](#cambios-hechos)
    * [Lista de cambios](#lista-de-cambios)
    * [*Checklist*](#checklist)

- [*Commits*](#commits)

- [*Issues*](#issues)

<hr width="30%" align="left" />

# Definiciones

Pequeñas definiciones, tal que puedan ser referidas más tarde en el documento.

## snake_case
Convención para nombrar variables, funciones, *etc.* que consta de escribir
todo en minúsculas, separando potenciales espacios entre palabras con
barras bajas (`"_"`). **Ejemplo:**
```py
numero_chulo = 69
cadenaNoTanChula = "#MalNombradoPapu"
```

## SNAKE_CASE
Una variante del [snake_case](#snake_case), también llamada *"screaming snake_case"*. Es idéntico
salvo que las palabras van en mayúsculas en vez de minúsculas. **Ejemplo:**
```py
CONSTANTE_CHULA = 297
```

## camelCase
Convención para nombrar cosas que consiste en borrar los potenciales espacios entre palabras, y la
primera letra a partir de la segunda palabra se pone en mayúscula. **Ejemplo:**
```py
camelloFeliz = "https://shorturl.at/esyAM"
```

## PascalCase
Similar a [camelCase](#camelcase), con la diferencia de que la primera
palabra también tiene la primera letra en mayúsculas. **Ejemplo:**
```py
class CirculoMuyGrande(FiguraABC):
    ...
```

<hr/>

# Código Fuente

Acá van todas las cosas referidas a escribir código fuente, los archivos en los que está conetnido
dicho código, así como tests, etc.

## *Type Hints*

Se deben usar *type hints* donde sea posible. Esto, incluyendo (pero no necesariamente
limitándose) a:

* Firmas de funciones
    - Parámetros

* Atributos de clase
    - Con esto me refiero a que dentro del `__init__(self)` todo atributo que se inicialice:
        ```py
        self.att = "Algo"
        ```
        Debe tener el tipo declarado también (así en otras partes del código el IDE puede
        identificar orígenes de métodos y tal):
        ```py
        self.att: str = "Algo"
        ```

* Aliases de tipos personalizados (son en sí del tipo `typing.TypeAlias`)

Esto se extiende incluso de modo que se importen los tipos y constantes correspondientes del módulo
`typing` de ser necesario (`typing.Union`, `typing.Optional`, `typing.TYPE_CHECKING`, _etc..._).

## Funciones

### Nombres

Los nombres de funciones deberán seguir la convención
[snake_case](#snake_case), al momento de ser definida la misma.
```py
def producto_cruz(x1: float, y1: float, z1: float,
                  x2: float, y2: float, z2: float
) -> tuple[float, float, float]:
    ...
```

### Parámetros
Los mismos también deberán respetar la convención [snake_case](#snake_case),
además de tener en lo posible *type hints*. <br/>
Es perdonable que la firma de una función larga ocupe varias líneas. Lo que sí, se deben
poner sangrías para que quede prolijo.
```py
def posicion(pos_x: float, pos_y: float, /,
             *,
             vel_x: float=0.0,
             vel_y: float=0.0,
             acc_x: float=0.0,
             acc_y: float=0.0) -> tuple[float, float]:
    ...
```
**Nota:** Es posible que si se usa un *linter* les diga que no le gustan parámetros de una sola
palabra (ergo `x` o `y1` no valen), pero acá lo permitimos. Si se baja el puntaje por eso, hay
formas como `# pylint: disable=invalid-name` para esos casos.

### *DocStrings*
Las cadenas destinadas a documentar el propósito de una función o método deben seguir el siguiente
patrón:
* Una descripción breve de lo que hace el cuerpo de la función.
* En caso de haber parámetros, poner un guión (`"-"`) en una nueva línea, y en la siguiente línea
empezar a describir cada parámetro con el estilo
    ```py
    """
    La función hace algo. No sé el qué, pero estoy seguro de que es muy bonito. No mires abajo al
    cuerpo de la función, confía: está todo bien.
    -
    'param1': Esto es lo que hace el parámetro número 1 (uno). Es muy posible que si la
              descripción ocupe más de una línea, dejar sangría a partir de la segunda así
              queda bonito.

    'param2': El parámetro 2 es para dejar en claro que entre parámetros hay una línea vacía
              de separación.

    'param3/param4': Si consideran que dos parámetros tienen diferencias superfluas, pueden unir
                     sus descripciones y referirlas de esta manera.

    'param5': ...
    """
    ```
* Con respecto a lo que devuelve la función, no hace falta repetirlo en el docstring, pero si se
quiere incluirlo debería ir brevemente en la primera parte que es la descripción. <br/>
Además, al expandirse en muchas líneas, las comillas triples (`"""`) que abren y cierran la cadena
deben ir en su propia línea, aisladas:
    ```py
    def producto_cruz(x1: float, y1: float, z1: float,
                      x2: float, y2: float, z2: float
    ) -> tuple[float, float, float]:
        """
        Dadas las coordenadas de dos vectores en R3, calcula un nuevo vector que es el
        "producto cruz" del primero por el segundo.
        -
        'x1/y1/z1': Las coordenadas del primer vector.

        'x2/y2/z2': Las coordenadas del segundo vector.
        """

        x = (y1 * z2) - (y2 * z1)
        y = -((x1 * z2) - (x2 * z1))
        z = (x1 * y2) - (x2 * y1)
        return x, y, z
    ```
Salvo que por cualquier razón el *docstring* termine con una sola línea (normalmente porque no hay
parámetros). En cuyo caso pueden cerrarse con comillas simples (`"`) todo en una línea, o bien
seguir igual el modelo de las comillas triples (`"""`):
```py
def comillas_simples() -> str:
    "Esta función devuelve el símbolo de la comilla (\")."

    return "\""

def comillas_triples() -> str:
    """
    Esta función devuelve el símbolo de la comilla (\").
    """

    return "\""
```
Son ambos modelos válidos.

## Constantes

Las constantes deben seguir la convención del [SNAKE_CASE](#snake_case-1) en mayúsculas. <br/>
Además, han de ir justo después de los *imports* (y de haber, también de los aliases de tipos
personalizados), **pero no antes** que la primera declaración de función, clase, o variable
global que prosiga en el cuerpo del programa.
```py
from math import pi
from typing import TypeAlias

TipoPI: TypeAlias = float

CONSTANTE_GLOBAL_CON_NOMBRE_MUY_LARGO: TipoPI = pi
```

## Clases

Los nombres con los que se definen las clases deben seguir la convención [PascalCase](#pascalcase).
```py
class PuntoConMasa(Coords):
    ...
```
Las clases, al igual que las funciones, deberían tener un brevísimo *docstring* que explique el
propósito de las mismas.

## *imports*

Los *imports* se subdividen en 3 subgrupos (que una extensión que se usa parece aplicar):
1. *imports* de la librería estándar
2. *imports* de librerías externas (como las que se instalan con *pip*)
3. *imports* locales

Deben ir en ese orden de arriba a abajo, sin separar líneas si son del mismo subgrupo, y con una
línea vacía para separar grupos:
```py
from math import inf, pi
from pathlib import Path
from os import environ

from pygame import Rect, Surface

from ..cat_1.arch_sup import func_esp # <- Los que están "más arriba" en el directorio deberían aparecer antes, pero tampoco hace falta
from .arch_local import func1
```
<br/>

Siempre se preferirá el patrón `from modulo import funcion` por sobre `import modulo`, haciendo uso
de `from modulo import funcion as alias_de_funcion` si es necesario.

* Dicho eso, todavía se prefiere `import modulo` por sobre `from modulo import *`. Eso es mala
práctica, y como mucho debería usarse sólo en los `__init__.py` de cada subpaquete para elevar los
módulos.

<br/>

Por último, en caso de tener muchos *imports* viniendo de un módulo, se los puede encerrar en una
"tupla", por así decir (respetando la sangría):
```py
from typing import (TYPE_CHECKING, Collection, Dict, Iterable, List, Optional,
                    Tuple, Type, TypeAlias, TypeVar, Union)
```
Dando prioridad (al parecer) a constantes por sobre orden alfabético.

<br/>

En donde se haga conflicto de mismos niveles, se separan los módulos a importar (así como las
funciones importadas desde cada uno), se ordena por orden alfabético.

## Archivos

Los nombres de los archivos creados _(así como también de las carpetas)_ deben seguir también
la convención de [snake_case](#snake_case). <br/>
Además, el encabezado de cada archivo (incluyendo los `__init__.py`) debe haber un *docstring* de
comillas triples explicando brevemente el propósito del módulo.

## Espaciado

Esto no promete ser tan riguroso, pero por establecer un estándar, acá es como se pondrían los
espacios en diferentes ocaciones. <br/>
Si un caso no está detallado, se toma como que queda a elección libre del programador.

### Espaciado con respecto a *Type Hints*

Siempre que se haga algo del estilo:
```
atributo: tipo
```
debe estar los dos puntos (`":"`) obligatorios que da la sintaxis, y nosotros le agregamos un
espacio (`" "`) para emprolijarlo. <br/>
Es decir, `atributo` y `tipo` deben ir siempre separados por
los caracteres `": "` exactamente. <br/>

Esto es independiente de cómo se separa `tipo` con cualquer valor subsecuente mediante el
caracter `"="`. Lo mismo se detalla más adelante.

### Espaciado en declaración de variables

También aplicable a atributos de clase y constantes, siempre que tengamos el patrón:
```
variable = valor
```
debe haber un espacio entre `variable` y el `=`; así como entre el `=` y `valor`. <br/>
Es decir, `variable` y `valor` deben ir separados por los caracteres `" = "` exactamente. Hay
una [excepción](#espaciado-de-parámetros-en-funciones) a esta regla.

### Espaciado en funciones

Entre la última línea de una función, y la primera línea de otra, deben haber dos líneas vacías
(es decir, sin ningún caracter) de separación:
```py
def suma(x: int, y: int) -> int:
    """
    Suma dos números.
    -
    'x/y': Los números a sumar.
    """

    return x + y


def producto(x: int, y: int) -> int:
    """
    Multiplica dos números.
    -
    'x/y': Los números a multiplicar.
    """

    return x * y
```
Esto también aplica entre métodos y *dunders* de una clase, y a los espacios entre una primera 
función en el módulo y la última de las constantes globales _(que, se sobreentiende, deben ir de
lo primero en el módulo)_.

#### Espaciado de parámetros en funciones
Cada parámetro (de haberlos) de una función, deben estar separados por los caracteres `", "`,
o bien por `","` y un salto de línea (para el caso de varias líneas). <br/>
En el caso de **valores por defecto**, no debe haber espacios entre el tipo, el `=` y el valor en
cuestión:
```py
def producto_punto(x1: float, y1: float, z1: float,
                   x2: float=0.0, y2: float=0.0, z2: float=0.0) -> float:
    ...
```

#### Espaciado después de *docstrings* en funciones

Entre la primera línea de código del cuerpo de una función y la última de su *docstring*, debe
haber *una* línea vacía de separación:
```py
def resta(x: int, y: int) -> int:
    """
    Resta dos números.
    -
    'x/y': Los números a restar.
    """

    return x - y
```

### Espaciado de *imports* y constantes globales

Los *imports*, tipos personalizados y constantes deben ir cada grupo en ese orden, separadas por
una línea vacía entre grupo y grupo.
```py
from typing import TYPE_CHECKING, TypeAlias, Union
from math import sqrt

Coords: TypeAlias = tuple[Union[float, int], Union[float, int]]

CONSTANTE_MUY_CHULA: int = 6913
```

### Espaciado al final de archivos

En lo posible, cada archivo de terminar con *una línea vacía*, y no más, conforme al
[PEP8](https://peps.python.org/pep-0008/) de Python.

## Estructura de Tests

Por temas organizativos, se tratará en lo posible de que la estructura de directorios de los tests
refleje fielmente a la del código fuente. <br/>
Es decir, si se tiene algo del estilo:
```
├─ src/
│   ├─main/
│   │  ├─main.py
│   │  ├─cat_1/
│   │  └─cat_2/
│   │     └─obj2.py
│   │
│   └─tests/
│
└─[...]
```
Y se desea armar tests unitarios para una clase que se encuentra en `obj2.py`, entonces es
conveniente imitar la estructura de `main/` y dejar algo como:
```
├─ src/
│   ├─main/
│   │  ├─main.py
│   │  ├─cat_1/
│   │  └─cat_2/
│   │     └─obj2.py
│   │
│   └─tests/
│       └─cat_2/
│           └─obj2_test.py
│
└─[...]
```
Omitiendo sin problema las carpetas vacías o que no contengan clases cuyo comportamiento interese
comprobar; además de anexar `_test` al nombre del archivo para diferenciar.

<hr/>

# *Pull Requests*

Los *pull requests* o "PRs" deben seguir el estilo de la
[plantilla](./templates/pull_requests/pr_template.md) diseñada para tal fin. <br/>
En ella, se encuentran las siguientes secciones:

## Motivación

Acá debería ir una descripción breve del PR y el propósito que pretende cumplir.

## Cambios Hechos

Una descripción breve de los cambios hechos, y cómo podrían afectar desde ahora al código con el
que interactúa.

## Lista de cambios

Una lista (sino es exhaustiva, que comprenda los puntos más importantes), detallando los cambios
precisos hechos en el código u en otro lugar.

* Normalmente
* tendrá un
* formato
    - más o
    - menos
        * parecido
* a esto.

## *Checklist*

He aquí una casilla de casos más comunes para llenar en todo modelo de PRs. En caso de querer
agregar más para el PR en cuestión se puede, pero no quitar alguna de las que ya vienen en la
plantilla. <br/>

**Nota:** *El estilo que aparece en GitHub parece exclusivo de esta página y no funciona sólo con MarkDown,
así que a continuación se detalla la forma de crear y editar algunas.*

```md
#### Casillas vacías:

*(válidas)*
* [ ]
- [ ]

*(inválidas)*
* []
- []
* [asd]

#### Casillas "llenas":

* [x]
* [X]
- [x]
- [X]
```

**Todos** los *pull requests* deberían ir acompañados de un "asignado" _(asignee)_, etiquetas, y
el proyecto correspondiente cuando se lo publica en GitHub. Opcionalmente, también debería estar
asociado a un *issue* y *milestone*.

<hr/>

# *Commits*

Los títulos de los *commits* deben de ser precedidos por `"<categoria>: "` de la manera:
```
<categoria>: Título del commit
```
Donde `<categoria>` referie a uno de los siguientes casos:

* **feat:** Una nueva *feature*.
* **fix:** Un arreglo de un *bug*.
* **docs:** Cambios en la documentación.
* **style:** Cambios que no afectan al código de manera funcional.
* **refactor:** Cambios que no arreglan errores o agregan *features*.
* **test:** Cambios que agregan tests.
* **chore:** Cambios hechos a programas auxiliares del proyecto, como la compilación automática
del programa.

Si no se identifica la ocasión con uno de estos casos, se puede evitar el prefijo.

**No es obligatorio** que los *commits* tengan una descripción.

<hr/>

# *Issues*

Las *issues* deberán seguir una plantilla según el [caso](./templates/issues/) que convenga.
De no estar contemplado el caso en una plantilla, se puede seguir un
estilo libre (pero se espera uno similar). <br/>

Los casos en cuestión son:

* 🐛 [Reportar un error](./templates/issues/bug_report_template.md)
* 🎨 [Una idea de diseño](./templates/issues/design_idea_template.md)
* 📚 [Una mejora de la documentación](./templates/issues/docs_augmentation_template.md)
* 🚀 [Una idea de *feature*](./templates/issues/feature_request_template.md)
* 🚧 [Una ocasión en la que refactorizar código](./templates/issues/refactor_code_template.md)

Donde el título del *issue* **debe empezar sí o sí** con el emoji correspondiente a esa categoría.
De no entrar en ninguna, el *issue* de estilo "libre" puede incluir cualquier emoji que no sea
uno de esos. <br/>

*En lo posible,* tratar de encajar la necesidad en alguna de esa categorías. **Por ejemplo:** un
reporte de una vulnerabilidad de seguridad podría ir acompañada de una refactorización, entonces
caería en la categoría 🚧; también, agregar librerías o extensiones para compilar el juego u otras
operaciones externas bien podrían ser 📚 o 🚀.
