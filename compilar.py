"""Compila el informe FORM-TL-01 en Windows de 64 bits."""

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


if __name__ == "__main__":
    informe = Path(__file__).resolve().parent / "FORM-TL-01"
    parser = argparse.ArgumentParser(description="Compila el informe FORM-TL-01.")
    parser.add_argument(
        "--salida",
        type=Path,
        default=informe,
        help="Carpeta donde se genera main.pdf (por defecto, FORM-TL-01).",
    )
    opciones = parser.parse_args()
    if platform.system() != "Windows" or platform.machine().upper() not in {"AMD64", "X86_64"}:
        raise SystemExit("Este script requiere Windows x64.")

    try:
        salida = opciones.salida.resolve()
        salida.mkdir(parents=True, exist_ok=True)
        tectonic = preparar_tectonic()
        resultado = subprocess.run(
            [tectonic, "--outdir", salida, "main.tex"], cwd=informe
        )
    except (OSError, BadZipFile) as error:
        raise SystemExit(f"No se pudo compilar el informe: {error}") from error
    raise SystemExit(resultado.returncode)
