# src/runner/cli.py

import typer
import subprocess
import sys
import os
from pathlib import Path

app = typer.Typer()

SRC_PATH = Path(__file__).resolve().parents[1]

def run_module(module: str):
    subprocess.run(
        [sys.executable, "-m", module],
        cwd=SRC_PATH,
        env={**dict(PYTHONPATH=str(SRC_PATH)), **dict(**os.environ)},
    )

@app.command()
def aspirador():
    """ Executa la tasca aspirador"""
    run_module("aspirador")

@app.command()
def quiques():
    """ Executa la tasca quiques"""
    run_module("quiques")


@app.command()
def monedes():
    """ Executa la tasca monedes"""
    run_module("monedes")

@app.command()
def practica():
    """ Executa la tasca de la pràctica"""
    run_module("practica")

@app.command()
def tictac():
    """ Executa la tasca tic-tac-toe"""
    run_module("tictac")

@app.command()
def prova():
    """ Test per si tot ha funcionat correctament"""
    print("Tot ha funcionat")

if __name__ == "__main__":
    app()
