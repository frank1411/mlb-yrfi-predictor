#!/usr/bin/env python3
"""
Script de automatización para el sistema de predicción YRFI de MLB.

Uso:
    python run_yrfi_analysis.py [opciones]

Opciones:
    --init           Inicializa el entorno (crea venv e instala dependencias)
    --force-update   Fuerza la actualización de datos aunque ya se haya actualizado hoy
    --no-update      No actualiza los datos, usa solo los existentes
    --output FILE    Guarda las predicciones en el archivo especificado
    --help           Muestra este mensaje de ayuda
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# Configuración
PROJECT_DIR = Path(__file__).parent.absolute()
VENV_DIR = PROJECT_DIR / "venv"
PYTHON = sys.executable
VENV_PYTHON = str(VENV_DIR / "bin" / "python")
REQUIREMENTS = PROJECT_DIR / "requirements.txt"
LAST_UPDATE_FILE = PROJECT_DIR / ".last_update"

# Colores para la salida
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Imprime un encabezado con formato."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime una advertencia."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime un mensaje de error."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def run_command(command, cwd=None, check=True, capture_output=False):
    """Ejecuta un comando en la terminal."""
    if cwd is None:
        cwd = PROJECT_DIR
    
    print(f"Ejecutando: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            text=True,
            capture_output=capture_output
        )
        if capture_output:
            return result.stdout.strip()
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al ejecutar el comando: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def setup_venv():
    """Configura el entorno virtual."""
    print_header("Configurando entorno virtual")
    
    if VENV_DIR.exists():
        print_success(f"Entorno virtual encontrado en {VENV_DIR}")
        return True
    
    print("Creando entorno virtual...")
    if run_command([PYTHON, "-m", "venv", str(VENV_DIR)]):
        print_success("Entorno virtual creado exitosamente")
        return True
    return False

def install_dependencies():
    """Instala las dependencias del proyecto."""
    print_header("Instalando dependencias")
    
    if not REQUIREMENTS.exists():
        print_error(f"Archivo de requisitos no encontrado: {REQUIREMENTS}")
        return False
    
    # Actualizar pip primero
    run_command([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Instalar dependencias
    if run_command([VENV_PYTHON, "-m", "pip", "install", "-r", str(REQUIREMENTS)]):
        print_success("Dependencias instaladas exitosamente")
        return True
    return False

def needs_update():
    """Verifica si es necesario actualizar los datos."""
    if not LAST_UPDATE_FILE.exists():
        return True
    
    try:
        last_update = datetime.fromtimestamp(LAST_UPDATE_FILE.stat().st_mtime).date()
        today = datetime.now().date()
        return last_update < today
    except Exception as e:
        print_warning(f"Error al verificar la última actualización: {e}")
        return True

def update_last_run():
    """Actualiza la marca de tiempo de la última ejecución."""
    try:
        LAST_UPDATE_FILE.touch(exist_ok=True)
        return True
    except Exception as e:
        print_warning(f"No se pudo actualizar la marca de tiempo: {e}")
        return False

def initialize_environment():
    """Inicializa el entorno del proyecto."""
    if not setup_venv():
        return False
    return install_dependencies()

def initialize_season_data():
    """Inicializa los datos de la temporada."""
    print_header("Inicializando datos de la temporada")
    script_path = PROJECT_DIR / "scripts" / "initialize_season_data.py"
    if not script_path.exists():
        print_error(f"Script no encontrado: {script_path}")
        return False
    
    if run_command([VENV_PYTHON, str(script_path)]):
        update_last_run()
        return True
    return False

def update_daily_data():
    """Actualiza los datos diarios."""
    print_header("Actualizando datos diarios")
    script_path = PROJECT_DIR / "scripts" / "update_daily_data.py"
    if not script_path.exists():
        print_error(f"Script no encontrado: {script_path}")
        return False
    
    if run_command([VENV_PYTHON, str(script_path)]):
        update_last_run()
        return True
    return False

def generate_predictions(output_file=None):
    """Genera las predicciones."""
    print_header("Generando predicciones")
    script_path = PROJECT_DIR / "scripts" / "generate_predictions.py"
    if not script_path.exists():
        print_error(f"Script no encontrado: {script_path}")
        return False
    
    cmd = [VENV_PYTHON, str(script_path)]
    if output_file:
        cmd.extend(["--output", str(output_file)])
    
    return run_command(cmd)

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Sistema de predicción YRFI de MLB')
    parser.add_argument('--init', action='store_true', help='Inicializa el entorno')
    parser.add_argument('--force-update', action='store_true', help='Fuerza la actualización de datos')
    parser.add_argument('--no-update', action='store_true', help='No actualiza los datos')
    parser.add_argument('--output', type=str, help='Archivo de salida para las predicciones')
    
    args = parser.parse_args()
    
    # Inicializar entorno si se solicita
    if args.init:
        if not initialize_environment():
            print_error("Error al inicializar el entorno")
            return 1
    
    # Verificar si el entorno virtual existe
    if not VENV_DIR.exists():
        print_error("El entorno virtual no existe. Ejecuta con --init primero.")
        print("  python run_yrfi_analysis.py --init")
        return 1
    
    # Inicializar datos de temporada si no existen
    season_data = PROJECT_DIR / "data" / "season_data.json"
    if not season_data.exists():
        print_warning("No se encontraron datos de temporada. Inicializando...")
        if not initialize_season_data():
            print_error("Error al inicializar los datos de temporada")
            return 1
    
    # Actualizar datos si es necesario
    should_update = not args.no_update and (args.force_update or needs_update())
    if should_update:
        if not update_daily_data():
            print_warning("No se pudieron actualizar los datos. Continuando con los datos existentes.")
    else:
        print_success("Los datos ya están actualizados. Omitiendo actualización.")
    
    # Generar predicciones
    if not generate_predictions(args.output):
        print_error("Error al generar predicciones")
        return 1
    
    print_success("Proceso completado exitosamente!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)
