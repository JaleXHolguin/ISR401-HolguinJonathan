# FORM-TL-01 — Taller de tipos de requisitos

## Compilar el informe

Requisito: Python 3 instalado en Windows x64.

Desde la carpeta del repositorio, ejecutar:

~~~powershell
py compilar.py
~~~

La primera compilación requiere internet para descargar Tectonic 0.17.0 y los paquetes de LaTeX. El script compila `FORM-TL-01/main.tex` y genera `FORM-TL-01/main.pdf`.

Para generar el PDF en otra carpeta, usa `--salida`.

~~~powershell
py compilar.py --salida revision
~~~
