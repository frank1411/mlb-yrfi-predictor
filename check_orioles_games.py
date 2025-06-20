#!/usr/bin/env python3
"""
Script para verificar el número exacto de partidos jugados por los Baltimore Orioles.
"""
import sys
from datetime import datetime, timedelta
from src.mlb_client import MLBClient

def main():
    client = MLBClient()
    start_date = '2025-03-27'
    end_date = '2025-06-13'
    
    print(f"Verificando partidos de Baltimore Orioles del {start_date} al {end_date}...")
    
    # Convertir fechas a objetos datetime
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Inicializar contadores
    total_games = 0
    game_dates = {}
    
    # Iterar por cada día
    current_date = start
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        try:
            # Obtener el calendario para el día actual
            schedule = client.get_schedule(date=date_str)
            
            # Procesar cada fecha en la respuesta
            for date_data in schedule.get('dates', []):
                for game in date_data.get('games', []):
                    # Verificar si es un partido de los Orioles
                    home_team = game.get('teams', {}).get('home', {}).get('team', {}).get('name')
                    away_team = game.get('teams', {}).get('away', {}).get('team', {}).get('name')
                    
                    if home_team == 'Baltimore Orioles' or away_team == 'Baltimore Orioles':
                        # Verificar si el juego ya finalizó
                        status = game.get('status', {})
                        abstract_code = status.get('abstractGameCode')
                        detailed_state = status.get('detailedState', '').lower()
                        
                        # Solo contar juegos que realmente hayan finalizado
                        is_final = (
                            abstract_code == 'F' and  # Juego finalizado
                            detailed_state in ['final', 'game over'] and
                            status.get('statusCode') in ['F', 'O', 'D'] and  # Final, Final en extras, Final definitivo
                            game.get('gameType') == 'R'  # Solo juegos de temporada regular
                        )
                        
                        if is_final:
                            game_date = game.get('gameDate', '')[:10]  # Solo la fecha
                            if game_date not in game_dates:
                                game_dates[game_date] = 0
                            game_dates[game_date] += 1
                            total_games += 1
                            
                            # Imprimir detalles del partido
                            print(f"{game_date} | {away_team} @ {home_team} | Finalizado")
                        else:
                            # Imprimir partidos que no se están contando
                            game_date = game.get('gameDate', '')[:10]
                            print(f"[NO CONTADO] {game_date} | {away_team} @ {home_team} | Estado: {detailed_state} (Código: {abstract_code})")
            
        except Exception as e:
            print(f"Error al procesar {date_str}: {str(e)}")
        
        # Pasar al siguiente día
        current_date += timedelta(days=1)
    
    # Imprimir resumen
    print("\nResumen de partidos por fecha:")
    for date, count in sorted(game_dates.items()):
        print(f"{date}: {count} partido{'s' if count > 1 else ''}")
    
    print(f"\nTotal de partidos jugados por Baltimore Orioles: {total_games}")

if __name__ == "__main__":
    main()
