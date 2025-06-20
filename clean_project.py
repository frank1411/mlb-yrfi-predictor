#!/usr/bin/env python3
"""
Script para limpiar el proyecto, eliminando archivos generados y caché.
"""
import os
import shutil
from pathlib import Path

# Directorios y archivos a conservar
KEEP_FILES = {
    'src/',
    'src/__init__.py',
    'src/mlb_client.py',
    'src/yrfi_analyzer.py',
    'scripts/',
    'scripts/__init__.py',
    'scripts/initialize_season_data.py',
    'scripts/update_daily_data.py',
    'scripts/generate_predictions.py',
    'src/data/',
    'src/data/__init__.py',
    'src/data/data_manager.py',
    'tests/',
    'tests/__init__.py',
    'requirements.txt',
    'README.md',
    '.gitignore',
    'clean_project.py'  # Este mismo archivo
}

def clean_project():
    """Limpia el proyecto eliminando archivos generados y caché."""
    base_dir = Path(__file__).parent
    
    # Archivos y directorios a eliminar
    to_remove = [
        base_dir / '.cache',
        base_dir / 'data',
        base_dir / 'reports',
        base_dir / 'daily_yrfi_predictions.py',
        base_dir / 'analyze_yrfi.py',
        base_dir / 'example.py',
        base_dir / 'yrfi_report.txt',
        base_dir / '__pycache__',
        base_dir / '.pytest_cache',
    ]
    
    # Eliminar archivos .pyc y __pycache__
    for pyc_file in base_dir.rglob('*.pyc'):
        try:
            pyc_file.unlink()
            print(f"Eliminado: {pyc_file}")
        except Exception as e:
            print(f"Error al eliminar {pyc_file}: {e}")
    
    for pycache in base_dir.rglob('__pycache__'):
        try:
            shutil.rmtree(pycache)
            print(f"Eliminado: {pycache}")
        except Exception as e:
            print(f"Error al eliminar {pycache}: {e}")
    
    # Eliminar directorios y archivos
    for item in to_remove:
        if not item.exists():
            continue
            
        try:
            if item.is_dir():
                shutil.rmtree(item)
                print(f"Eliminado directorio: {item}")
            else:
                item.unlink()
                print(f"Eliminado archivo: {item}")
        except Exception as e:
            print(f"Error al eliminar {item}: {e}")
    
    # Crear directorios necesarios
    (base_dir / 'data').mkdir(exist_ok=True)
    (base_dir / 'reports').mkdir(exist_ok=True)
    (base_dir / '.cache').mkdir(exist_ok=True)
    
    print("\nLimpieza completada. Estructura del proyecto:")
    os.system(f"find {base_dir} -maxdepth 3 -type d | sort")

if __name__ == "__main__":
    print("=== Limpiando proyecto ===\n")
    clean_project()
    print("\n=== Proyecto limpio exitosamente ===")
