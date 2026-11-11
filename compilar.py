"""Compila los informes del repositorio en Windows de 64 bits."""

import argparse
import os
from pathlib import Path
import platform
import subprocess
import tempfile
from urllib.request import urlretrieve
from zipfile import BadZipFile, ZipFile


VERSION = "0.17.0"
URL = (
    "https://github.com/tectonic-typesetting/tectonic/releases/download/"
    f"tectonic%40{VERSION}/tectonic-{VERSION}-x86_64-pc-windows-msvc.zip"
)


def preparar_tectonic():
    carpeta = Path(os.environ["LOCALAPPDATA"]) / "Tectonic" / VERSION
    ejecutable = carpeta / "tectonic.exe"
    if ejecutable.is_file():
        return ejecutable

    print(f"Descargando Tectonic {VERSION}...", flush=True)
    carpeta.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=carpeta) as temporal:
        archivo = Path(temporal) / "tectonic.zip"
        urlretrieve(URL, archivo)
        with ZipFile(archivo) as zip_tectonic:
            extraido = Path(zip_tectonic.extract("tectonic.exe", temporal))
        extraido.replace(ejecutable)
    return ejecutable


def elegir_tarea(tareas):
    print("Tareas disponibles")
    opciones = {str(i): codigo for i, codigo in enumerate(tareas, start=1)}
    for numero, codigo in opciones.items():
        print(f"  {numero}. {codigo}")

    while True:
        try:
            numero = input("Selecciona el número de la tarea (0 para salir): ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit("\nSelección cancelada.") from None
        if numero == "0":
            raise SystemExit(0)
        if numero in opciones:
            return opciones[numero]
        print("Elige uno de los números del menú.")


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent
    tareas = {
        fuente.parent.name: fuente.parent
        for fuente in sorted(raiz.glob("*/main.tex"))
        if fuente.is_file()
    }
    parser = argparse.ArgumentParser(description="Compila un informe del repositorio.")
    parser.add_argument(
        "--salida",
        type=Path,
        help="Carpeta donde se genera main.pdf (por defecto, la carpeta de la tarea).",
    )
    opciones = parser.parse_args()
    if platform.system() != "Windows" or platform.machine().upper() not in {"AMD64", "X86_64"}:
        raise SystemExit("Este script requiere Windows x64.")

    if not tareas:
        parser.error("No se encontraron carpetas con main.tex en la raíz del repositorio.")

    try:
        print("Comprobando Tectonic...", flush=True)
        tectonic = preparar_tectonic()
        subprocess.run([tectonic, "--version"], check=True)

        informe = tareas[elegir_tarea(tareas)]
        salida = (opciones.salida or informe).resolve()
        salida.mkdir(parents=True, exist_ok=True)
        resultado = subprocess.run(
            [tectonic, "--outdir", salida, "main.tex"], cwd=informe
        )
    except (OSError, BadZipFile, subprocess.CalledProcessError) as error:
        raise SystemExit(f"No se pudo compilar el informe: {error}") from error
    raise SystemExit(resultado.returncode)
