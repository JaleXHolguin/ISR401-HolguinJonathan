# ISR401 — Ingeniería de Requerimientos

## Compilar un informe

Requisito: Python 3 instalado en Windows x64.

Abrir una terminal en la carpeta raíz del proyecto, donde está `compilar.py`, y ejecutar el siguiente comando.

~~~powershell
py compilar.py
~~~

El script comprueba Tectonic 0.17.0 y lo descarga si hace falta. La primera compilación requiere internet para descargar el compilador y los paquetes de LaTeX.

Después aparece un menú con las carpetas de la raíz que contienen `main.tex`. Escribir el número de la tarea y pulsar Enter. El script compila su `main.tex` y guarda `main.pdf` en la carpeta de esa tarea.

Para generar el PDF en otra carpeta, **usar** `--salida`.

~~~powershell
py compilar.py --salida revision
~~~
