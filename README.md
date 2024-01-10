# TP Aninfo - 2023C2

![version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Tests](https://github.com/InspectorDave/TP-Aninfo/actions/workflows/tests.yml/badge.svg)
![Pylint](https://github.com/InspectorDave/TP-Aninfo/actions/workflows/pylint.yml/badge.svg)

Repositorio para el trabajo práctico de la materia "Análisis de la Información" (Camejo),
2do cuatrimestre de 2023.

## Índice

* [Objetivo](#objetivo)
* [Alcance](#alcance-del-proyecto)
    - [Prototipo](#prototipo)
* [Integrantes](#integrantes)
* [Dependencias](#dependencias)
* [Cómo correr el proyecto](#cómo-correr-el-proyecto)
* [Convenciones](#convenciones)

<hr/>

# Objetivo

Se busca crear un juego tipo *platformer* en el cual un individuo evita obstáculos y colecciona
objetos antes de llegar a la meta. 


<hr width="30%" align="left" />

# Alcance del proyecto

El juego a desarrollar constará de 3 niveles, en cada uno de ellos el objetivo es el mismo; superar
distintos obstaculos hasta llegar a una meta para así poder avanzar al siguiente nivel.
El juego termina cuando el jugador haya completado los 3 niveles.

El proyecto en su primer entregable se limitará a implementar la siguiente funcionalidad en
cada nivel:

1. Un punto inicial y final al que hay que llegar para completar cada nivel y avanzar al siguiente.

2. Un sistema de vidas por corazones.

3. Obstáculos que le restan vidas al jugador si este cae en uno de ellos. Estos obstaculos serán
pinches y/o espacios vacíos.

4. Objetos coleccionables que desbloqueen puertas que impidan terminar un nivel.

## Prototipo

Un ejemplo del diseño que implementan los puntos anteriormente dichos se pueden ver en las imágenes
del [prototipo](./documentation/prototipos/Versión%202/) hecho para tal fin:

| <center>Ventana</center> | <center>Imagen</center> |
|:------------------------:|:-----------------------:|
| Menú principal | <img align="center" src="./documentation/prototipos/Versión 2/Menu Principal.png" height=225 width=200 /> |
| Nivel 1 | <img align="center" src="./documentation/prototipos/Versión 2/Nivel 1.png" height=225 width=360 /> |
| Nivel 2 | <img align="center" src="./documentation/prototipos/Versión 2/Nivel 2.png" height=225 width=360 /> |
| Nivel 3 | <img align="center" src="./documentation/prototipos/Versión 2/Nivel 3.png" height=225 width=360 /> |

<hr width="30%" align="left" />

# Integrantes

| <center>Alumno</center> | <center>Padrón</center> | <center>Mail</center> | <center>GitHub</center> |
|:------------------------|:-----------------------:|:----------------------|:------------------------|
| **Lighterman Reismann, Franco** | 106714| flighterman@fi.uba.ar | <img align="center" src="https://github.com/NLGS2907.png" height=32 width=32 /> [NLGS2907](https://github.com/NLGS2907) |
| **Mundani Vegega, Ezequiel** | 102312 | emundani@fi.uba.ar | <img align="center" src="https://github.com/InspectorDave.png" height=32 width=32 /> [InspectorDave](https://github.com/InspectorDave) |
| **Regazzoli, Ignacio** | 105167 | iregazzoli@fi.uba.ar | <img align="center" src="https://github.com/iregazzoli.png" height=32 width=32 /> [iregazzoli](https://github.com/iregazzoli) |
| **Rivera Villatte, Manuel** | 106041 | mriverav@fi.uba.ar | <img align="center" src="https://github.com/ManusaRivi.png" height=32 width=32 /> [ManusaRivi](https://github.com/ManusaRivi) |
| **Zacarías Rojas, Víctor Manuel** | 107080 | vzacarias@fi.uba.ar | <img align="center" src="https://github.com/vic02505.png" height=32 width=32 /> [vic02505](https://github.com/vic02505) |

<hr width="30%" align="left" />

# Dependencias

Las siguientes librerías externas son utilizadas para este proyecto, instaladas con
`pip` y explicitadas en el [archivo correspondiente](./requirements.txt):

| <center>Dependencia</center> | <center>Versión</center> | <center>Motivo</center> |
|:-----------------------------|:------------------------:|:------------------------|
| [Pygame](https://pypi.org/project/pygame/) | 2.5.2 | Es la librería base sobre la que la lógica del juego es construida. |
| [Pygame-menu](https://pypi.org/project/pygame-menu/) | 4.4.3 | Una extensión de terceros de Pygame, especialmente hecha para crear menús y otros _widgets._ |

<hr width="30%" align="left" />

# Cómo correr el proyecto

Suponiendo que se ejecute desde consola, uno primero debe "pararse" en la carpeta raíz del proyecto
(ya sea con ayuda del comando `cd` de *shell* o *batch* o similar) y luego instalar las
[dependencias](./requirements.txt) con el comando:
```console
$ python -m pip install --upgrade -r requirements.txt
```
y luego, aún parado en la misma carpeta, ejecutar el proyecto desde el código fuente con:
```console
$ python -m src.main.main
```

Donde `python` se refiere al comando con el que se llama al intérprete de
[Python](https://www.python.org/) instalado. Bien podría ser `python3` o `py` dependiendo del
sistema operativo y de si se tienen múltiples intérpretes en una máquina. <br/>
El proyecto se desarrolla con Python 3.11, por lo que se recomienda esa versión.

<hr width="30%" align="left" />

# Convenciones

Las convenciones utilizadas en el proyecto, como las utilizadas para el
[código fuente](./CONTRIBUTING.md#código-fuente),
[*pull requests*](./CONTRIBUTING.md#pull-requests) o la formación de
[*issues*](./CONTRIBUTING.md#issues) se encuentran en el [archivo](./CONTRIBUTING.md)
correspondiente.
