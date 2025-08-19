#!/usr/bin/env python3
"""
Script para generar un archivo JSON con datos para predicciones ML de partidos de MLB.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Añadir el directorio raíz al path para poder importar los módulos
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

# Configuración
BASE_DIR = Path(__file__).parent.parent
PREDICTIONS_DIR = BASE_DIR / "predictions"
OUTPUT_DIR = BASE_DIR / "data"
OUTPUT_FILE = "datos_prediccion_{}.json".format(datetime.now().strftime("%Y%m%d"))

def cargar_predicciones() -> Dict[int, Dict]:
    """
    Carga todos los archivos de predicción de la carpeta predictions.
    
    Returns:
        Diccionario con los datos de predicción indexados por game_pk
    """
    predicciones = {}
    for archivo in PREDICTIONS_DIR.glob("yrfi_*.json"):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                game_pk = datos.get('game_pk')
                if game_pk:
                    predicciones[game_pk] = datos
        except Exception as e:
            print(f"Error al cargar {archivo}: {e}")
    return predicciones

def calcular_suavizado(base: float, ultimos: float, peso_base: float = 0.7) -> float:
    """
    Calcula un valor suavizado entre las estadísticas base y las más recientes.
    
    Args:
        base: Valor base (histórico)
        ultimos: Valor de los últimos partidos
        peso_base: Peso del valor base (0-1)
        
    Returns:
        Valor suavizado
    """
    return (base * peso_base) + (ultimos * (1 - peso_base))

def obtener_estadisticas_partido(prediccion: Dict) -> Dict[str, float]:
    """
    Extrae y calcula las estadísticas de un partido desde los datos de predicción.
    
    Args:
        prediccion: Diccionario con los datos de predicción
        
    Returns:
        Diccionario con las estadísticas del partido
    """
    home = prediccion.get('home_team', {})
    away = prediccion.get('away_team', {})
    pred = prediccion.get('prediction', {}).get('calculation', {})
    
    # Obtener porcentajes base
    home_base = home.get('stats', {}).get('base', {}).get('value', 0) / 100
    home_tend = home.get('stats', {}).get('tendency', {}).get('value', 0) / 100
    away_base = away.get('stats', {}).get('base', {}).get('value', 0) / 100
    away_tend = away.get('stats', {}).get('tendency', {}).get('value', 0) / 100
    
    # Calcular valores suavizados
    home_pct = calcular_suavizado(home_base, home_tend)
    away_pct = calcular_suavizado(away_base, away_tend)
    
    # Obtener estadísticas de los lanzadores
    home_pitcher_stats = obtener_estadisticas_lanzador(home.get('pitcher', {}))
    away_pitcher_stats = obtener_estadisticas_lanzador(away.get('pitcher', {}))
    
    home_pitcher = home_pitcher_stats['pct_permite_carrera_suavizado']
    away_pitcher = away_pitcher_stats['pct_permite_carrera_suavizado']
    
    return {
        'local_pct_anota_1inn_local': home_base,
        'local_pct_anota_1inn_ult15': home_tend,
        'visit_pct_anota_1inn_visit': away_base,
        'visit_pct_anota_1inn_ult15': away_tend,
        'pitcher_local_pct_permite_carrera_suavizado': home_pitcher,
        'pitcher_visit_pct_permite_carrera_suavizado': away_pitcher
    }

def calcular_promedio_liga_yrfi() -> float:
    """
    Calcula el promedio de YRFI de la liga a partir de season_data.json
    """
    try:
        season_data_path = os.path.join(BASE_DIR, 'data', 'season_data.json')
        with open(season_data_path, 'r') as f:
            data = json.load(f)
            
        total_yrfi = 0
        total_games = 0
        
        for team_id, team_data in data.get('teams', {}).items():
            total_yrfi += team_data.get('total_yrfi', 0)
            total_games += team_data.get('total_games', 0)
            
        return total_yrfi / total_games if total_games > 0 else 0.25  # 25% si no hay datos
        
    except Exception as e:
        print(f"Error al calcular promedio de liga: {e}")
        return 0.25  # Valor por defecto si hay error

def calcular_pct_permite_carrera_suavizado(yrfi_allowed: float, yrfi_ratio: str) -> float:
    """
    Calcula el porcentaje de carreras permitidas suavizado
    
    Args:
        yrfi_allowed: Porcentaje de carreras permitidas (ej: 23.07)
        yrfi_ratio: String en formato "3/13" donde 3 es carreras permitidas y 13 es aperturas
        
    Returns:
        Porcentaje suavizado de carreras permitidas
    """
    try:
        # Obtener n (aperturas) del ratio
        if '/' in yrfi_ratio:
            allowed, n_str = yrfi_ratio.split('/')
            n = int(n_str)
            allowed = int(allowed)
        else:
            n = 1  # Valor por defecto si no hay ratio
            allowed = 0
            
        # Convertir a decimal (viene como porcentaje)
        p_raw = yrfi_allowed / 100.0
        
        # Obtener promedio de la liga
        league_avg = calcular_promedio_liga_yrfi()
        
        # Aplicar suavizado
        CREDIBILITY_CONSTANT_C = 15  # Misma constante que en generar_dataset_final.py
        p_smoothed = ((n * p_raw) + (CREDIBILITY_CONSTANT_C * league_avg)) / (n + CREDIBILITY_CONSTANT_C)
        
        # Debug: Mostrar información del cálculo
        print(f"Lanzador: {yrfi_ratio} (YRFI: {yrfi_allowed}%)")
        print(f"  - Aperturas (n): {n}, Carreras permitidas: {allowed}")
        print(f"  - p_raw: {p_raw:.4f}, league_avg: {league_avg:.4f}")
        print(f"  - p_smoothed: {p_smoothed:.4f}\n")
        
        return p_smoothed
        
    except Exception as e:
        print(f"Error al calcular porcentaje suavizado: {e}")
        return 0.35  # Valor por defecto si hay error

def obtener_estadisticas_lanzador(pitcher_data: Dict) -> Dict[str, float]:
    """
    Obtiene las estadísticas de un lanzador desde los datos de predicción.
    """
    if not pitcher_data:
        return {
            'pct_permite_carrera_suavizado': 0.35  # Valor por defecto
        }
    
    # Obtener datos del lanzador
    yrfi_allowed = pitcher_data.get('yrfi_allowed', 0)
    yrfi_ratio = pitcher_data.get('yrfi_ratio', '0/1')
    
    # Debug: Mostrar datos del lanzador
    print(f"\nProcesando lanzador: {pitcher_data.get('name', 'Desconocido')}")
    print(f"- YRFI allowed: {yrfi_allowed}%")
    print(f"- YRFI ratio: {yrfi_ratio}")
    
    # Calcular el porcentaje suavizado
    pct_suavizado = calcular_pct_permite_carrera_suavizado(yrfi_allowed, yrfi_ratio)
    
    return {
        'pct_permite_carrera_suavizado': pct_suavizado
    }

def obtener_detalle_lanzador(pitcher_data: Dict) -> Dict[str, Any]:
    """
    Obtiene los detalles de un lanzador a partir de los datos de la API.
    
    Args:
        pitcher_data: Datos del lanzador de la API
        
    Returns:
        Diccionario con los detalles del lanzador
    """
    if not pitcher_data or 'id' not in pitcher_data:
        return {
            'id': None,
            'nombre': 'Por anunciar',
            'pct_permite_carrera_suavizado': 0.35  # Valor por defecto
        }
    
    # Obtener estadísticas del lanzador
    stats = obtener_estadisticas_lanzador(pitcher_data['id'])
    
    return {
        'id': pitcher_data['id'],
        'nombre': pitcher_data.get('fullName', 'Por anunciar'),
        'pct_permite_carrera_suavizado': stats['pct_permite_carrera_suavizado']
    }

def obtener_partidos_del_dia() -> List[Dict]:
    """
    Obtiene los partidos programados para el día actual desde los archivos de predicción.
    
    Returns:
        Lista de diccionarios con información de los partidos
    """
    try:
        # Cargar todas las predicciones
        predicciones = cargar_predicciones()
        
        partidos = []
        for game_pk, prediccion in predicciones.items():
            try:
                home_team = prediccion.get('home_team', {})
                away_team = prediccion.get('away_team', {})
                
                # Obtener estadísticas del partido
                stats = obtener_estadisticas_partido(prediccion)
                
                # Calcular probabilidades
                prob_local = stats['local_pct_anota_1inn_local'] * (1 - stats['pitcher_visit_pct_permite_carrera_suavizado'])
                prob_visit = stats['visit_pct_anota_1inn_visit'] * (1 - stats['pitcher_local_pct_permite_carrera_suavizado'])
                prob_yrfi = 1 - ((1 - prob_local) * (1 - prob_visit))
                
                # Formatear la salida simplificada
                partido = {
                    'game_pk': game_pk,
                    'fecha': prediccion.get('game_date', '').split('T')[0],  # Solo la fecha
                    'estado': 'Scheduled',
                    'equipo_local': {
                        'nombre': home_team.get('name', 'Desconocido'),
                        'lanzador': {
                            'nombre': home_team.get('pitcher', {}).get('name', 'Por anunciar'),
                        }
                    },
                    'equipo_visitante': {
                        'nombre': away_team.get('name', 'Desconocido'),
                        'lanzador': {
                            'nombre': away_team.get('pitcher', {}).get('name', 'Por anunciar'),
                        }
                    },
                    'estadisticas': {
                        'local_pct_anota_1inn_local': stats['local_pct_anota_1inn_local'],
                        'local_pct_anota_1inn_ult15': stats['local_pct_anota_1inn_ult15'],
                        'visit_pct_anota_1inn_visit': stats['visit_pct_anota_1inn_visit'],
                        'visit_pct_anota_1inn_ult15': stats['visit_pct_anota_1inn_ult15'],
                        'pitcher_local_pct_permite_carrera_suavizado': stats['pitcher_local_pct_permite_carrera_suavizado'],
                        'pitcher_visit_pct_permite_carrera_suavizado': stats['pitcher_visit_pct_permite_carrera_suavizado']
                    }
                }
                
                partidos.append(partido)
                
            except Exception as e:
                print(f"Error al procesar partido {game_pk}: {e}")
        
        return partidos
        
    except Exception as e:
        print(f"Error al obtener partidos: {e}")
        return []

def guardar_datos(partidos: List[Dict]) -> str:
    """
    Guarda los datos de los partidos en un archivo JSON.
    
    Args:
        partidos: Lista de diccionarios con información de los partidos
        
    Returns:
        Ruta al archivo guardado
    """
    # Crear directorio si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Crear estructura del archivo
    datos = {
        'fecha_consulta': datetime.now().strftime("%Y-%m-%d"),
        'total_partidos': len(partidos),
        'partidos': partidos
    }
    
    # Guardar en archivo
    output_path = OUTPUT_DIR / OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    return str(output_path)

def main():
    """Función principal."""
    print("Obteniendo partidos del día...")
    partidos = obtener_partidos_del_dia()
    
    if not partidos:
        print("No se encontraron partidos para hoy.")
        return
    
    print(f"Procesando {len(partidos)} partidos...")
    output_path = guardar_datos(partidos)
    
    print(f"\n✅ Datos guardados en: {output_path}")
    print(f"Total de partidos procesados: {len(partidos)}")

if __name__ == "__main__":
    main()
