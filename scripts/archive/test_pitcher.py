#!/usr/bin/env python3
"""
Script de prueba para obtener información de un lanzador específico.
"""
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient

def main():
    """Función principal."""
    # Crear cliente de MLB
    mlb_client = MLBClient()
    
    # ID de Logan Webb como ejemplo
    player_id = 657656
    
    try:
        # Obtener información básica del jugador
        print(f"Obteniendo información para el jugador ID: {player_id}")
        player_info = mlb_client.get_player(player_id)
        
        if not player_info:
            print("No se pudo obtener información del jugador")
            return
            
        # Mostrar información básica
        print("\nInformación del jugador:")
        print(f"Nombre: {player_info.get('fullName', 'Desconocido')}")
        print(f"Posición: {player_info.get('primaryPosition', {}).get('name', 'Desconocida')}")
        print(f"Equipo actual: {player_info.get('currentTeam', {}).get('name', 'Desconocido')}")
        
        # Obtener estadísticas de pitcheo
        print("\nObteniendo estadísticas de pitcheo...")
        endpoint = f"people/{player_id}"
        params = {
            'hydrate': 'stats(group=[pitching],type=[season],season=2025)',
            'season': 2025
        }
        
        response = mlb_client._make_request(endpoint, params=params)
        
        if not response or 'people' not in response or not response['people']:
            print("No se encontraron estadísticas para este jugador")
            return
            
        # Mostrar estadísticas
        print("\nEstadísticas de pitcheo (2025):")
        player_data = response['people'][0]
        
        if 'stats' in player_data and player_data['stats']:
            for stat_group in player_data['stats']:
                if stat_group.get('group', {}).get('displayName') == 'pitching':
                    stats = stat_group.get('splits', [{}])[0].get('stat', {})
                    print(f"• Juegos: {stats.get('gamesPlayed', 0)}")
                    print(f"• Juegos como abridor: {stats.get('gamesStarted', 0)}")
                    print(f"• Inning lanzados: {stats.get('inningsPitched', '0.0')}")
                    print(f"• ERA: {stats.get('era', '0.00')}")
                    print(f"• WHIP: {stats.get('whip', '0.00')}")
                    print(f"• Ponches: {stats.get('strikeOuts', 0)}")
                    print(f"• Bases por bolas: {stats.get('baseOnBalls', 0)}")
                    break
        
    except Exception as e:
        print(f"Error al obtener información del jugador: {str(e)}")

if __name__ == "__main__":
    main()
