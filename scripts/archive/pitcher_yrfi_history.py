#!/usr/bin/env python3
"""
Script para obtener el historial de YRFI de lanzadores en sus aperturas.
"""
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

def get_pitcher_stats(mlb_client: MLBClient, player_id: int, season: int = 2025):
    """
    Obtiene las estadísticas de pitcheo de un lanzador en una temporada.
    
    Args:
        mlb_client: Instancia de MLBClient
        player_id: ID del lanzador
        season: Año de la temporada
        
    Returns:
        Diccionario con las estadísticas del lanzador
    """
    try:
        # Obtener estadísticas de pitcheo del lanzador
        endpoint = f"people/{player_id}"
        params = {
            'hydrate': f'stats(group=[pitching],type=[season],season={season})',
            'season': season
        }
        
        response = mlb_client._make_request(endpoint, params=params)
        
        # Verificar si hay datos
        if not response or 'people' not in response or not response['people']:
            return {}
            
        # Obtener las estadísticas
        player_data = response['people'][0]
        stats = {}
        
        if 'stats' in player_data and player_data['stats']:
            for stat_group in player_data['stats']:
                if stat_group.get('group', {}).get('displayName') == 'pitching':
                    stats = stat_group.get('splits', [{}])[0].get('stat', {})
                    break
        
        return {
            'id': player_id,
            'name': f"{player_data.get('firstName', '')} {player_data.get('lastName', '')}".strip(),
            'team': player_data.get('currentTeam', {}).get('name', 'Desconocido'),
            'position': player_data.get('primaryPosition', {}).get('name', 'Lanzador'),
            'age': player_data.get('currentAge', 'N/A'),
            'stats': stats
        }
        
    except Exception as e:
        print(f"Error al obtener estadísticas del lanzador {player_id}: {str(e)}")
        return {}

def get_pitcher_yrfi_stats(mlb_client: MLBClient, player_id: int, season: int = 2025):
    """
    Obtiene las estadísticas de YRFI de un lanzador.
    
    Args:
        mlb_client: Instancia de MLBClient
        player_id: ID del lanzador
        season: Año de la temporada
        
    Returns:
        Diccionario con las estadísticas de YRFI del lanzador
    """
    try:
        # Obtener estadísticas del lanzador
        pitcher_stats = get_pitcher_stats(mlb_client, player_id, season)
        
        if not pitcher_stats or 'stats' not in pitcher_stats:
            return {}
            
        # Obtener estadísticas específicas de YRFI
        stats = pitcher_stats['stats']
        
        # Calcular estadísticas relevantes
        games_started = stats.get('gamesStarted', 0)
        innings_pitched = stats.get('inningsPitched', 0)
        era = stats.get('era', 0.0)
        whip = stats.get('whip', 0.0)
        
        # Obtener estadísticas por inning (si están disponibles)
        first_inning_era = stats.get('firstInningEra', era)  # Usar ERA general si no hay datos específicos
        
        # Calcular estimación de YRFI basada en estadísticas
        # Esta es una estimación simple basada en ERA y WHIP
        yrfi_estimate = min(0.5, (era / 4.5) * 0.35 + (whip / 1.3) * 0.25 + 0.15)  # Fórmula de ejemplo
        
        return {
            'player_id': player_id,
            'name': pitcher_stats['name'],
            'team': pitcher_stats['team'],
            'games_started': games_started,
            'innings_pitched': innings_pitched,
            'era': era,
            'whip': whip,
            'first_inning_era': first_inning_era,
            'yrfi_estimate': yrfi_estimate,
            'stats': stats
        }
        
    except Exception as e:
        print(f"Error al obtener estadísticas de YRFI para el lanzador {player_id}: {str(e)}")
        return {}

def analyze_pitcher_yrfi(mlb_client: MLBClient, player_id: int, player_name: str, season: int = 2025):
    """
    Analiza las estadísticas de YRFI de un lanzador.
    
    Args:
        mlb_client: Instancia de MLBClient
        player_id: ID del lanzador
        player_name: Nombre del lanzador
        season: Año de la temporada
    """
    print(f"\nAnalizando estadísticas de YRFI para {player_name} (Temporada {season})...")
    
    try:
        # Obtener estadísticas de YRFI
        yrfi_stats = get_pitcher_yrfi_stats(mlb_client, player_id, season)
        
        if not yrfi_stats:
            print(f"No se pudieron obtener estadísticas para {player_name}")
            return
        
        # Mostrar información del lanzador
        print(f"\nInformación de {yrfi_stats['name']}:")
        print(f"• Equipo: {yrfi_stats['team']}")
        print(f"• Juegos como abridor: {yrfi_stats['games_started']}")
        print(f"• Inning lanzados: {yrfi_stats['innings_pitched']}")
        
        # Mostrar estadísticas clave
        print("\nEstadísticas de pitcheo:")
        print(f"• ERA: {yrfi_stats['era']:.2f}")
        print(f"• WHIP: {yrfi_stats['whip']:.3f}")
        print(f"• ERA en el 1er inning: {yrfi_stats['first_inning_era']:.2f}" if 'first_inning_era' in yrfi_stats else "• No hay datos específicos del 1er inning")
        
        # Mostrar estimación de YRFI
        print(f"\nEstimación de YRFI: {yrfi_stats['yrfi_estimate']*100:.1f}%")
        
        # Interpretación de la estimación
        yrfi_estimate = yrfi_stats['yrfi_estimate']
        if yrfi_estimate > 0.4:
            print("• Riesgo ALTO de YRFI (más del 40% de probabilidad)")
        elif yrfi_estimate > 0.3:
            print("• Riesgo MEDIO de YRFI (entre 30% y 40% de probabilidad)")
        else:
            print("• Riesgo BAJO de YRFI (menos del 30% de probabilidad)")
        
        # Recomendación basada en las estadísticas
        print("\nRecomendación:")
        if yrfi_estimate > 0.4:
            print("🔴 Alto riesgo de YRFI. Considerar apostar por carreras en el 1er inning.")
        elif yrfi_estimate > 0.3:
            print("🟡 Riesgo moderado de YRFI. Evaluar otros factores antes de apostar.")
        else:
            print("🟢 Bajo riesgo de YRFI. Considerar apostar por NO carreras en el 1er inning.")
    
    except Exception as e:
        print(f"Error al analizar las estadísticas de {player_name}: {str(e)}")

def main():
    """Función principal."""
    # Crear cliente de MLB
    mlb_client = MLBClient()
    
    # Diccionario de lanzadores para analizar (ID: Nombre)
    # IDs de los lanzadores para los partidos de hoy
    pitchers = {
        592450: "Ryan Yarbrough",
        656305: "Garrett Crochet",
        663554: "Ryne Nelson",
        657656: "Logan Webb",
        656302: "Yoshinobu Yamamoto",
        605135: "Kevin Gausman",
        605131: "Ranger Suárez",
        665833: "Edward Cabrera",
        680776: "Mitchell Parker"
    }
    
    # Obtener año actual
    current_year = datetime.now().year
    
    print("=== ANÁLISIS DE LANZADORES PARA HOY ===\n")
    
    # Analizar cada lanzador
    for player_id, player_name in pitchers.items():
        print("=" * 50)
        analyze_pitcher_yrfi(mlb_client, player_id, player_name, current_year)
        print("\n")

if __name__ == "__main__":
    main()
