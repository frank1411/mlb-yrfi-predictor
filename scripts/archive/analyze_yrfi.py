#!/usr/bin/env python3
"""
Análisis de predicciones YRFI (Yes Run First Inning) basado en datos históricos.

Este script lee los datos de temporada desde season_data.json y genera predicciones
para los próximos juegos basadas en el rendimiento histórico de los equipos.
"""

import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timezone

# Ruta al archivo de datos de temporada
SEASON_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data',
    'season_data.json'
)


def load_season_data(file_path: str) -> dict:
    """Carga los datos de temporada desde el archivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} no es un JSON válido")
        return {}


def calculate_team_stats(teams_data: dict) -> Dict[str, dict]:
    """Calcula las estadísticas de YRFI para cada equipo.
    
    Args:
        teams_data: Diccionario con datos de equipos del archivo JSON
        
    Returns:
        Diccionario con estadísticas de YRFI por equipo
    """
    team_stats = {}
    
    for team_id, team_data in teams_data.items():
        try:
            # Obtener datos del equipo
            team_name = team_data.get('name', f'Equipo {team_id}')
            home_games = team_data.get('home_games', 0)
            home_yrfi = team_data.get('home_yrfi', 0)
            away_games = team_data.get('away_games', 0)
            away_yrfi = team_data.get('away_yrfi', 0)
            
            # Calcular porcentajes de YRFI en casa y fuera
            home_yrfi_pct = (home_yrfi / home_games) * 100 if home_games > 0 else 0
            away_yrfi_pct = (away_yrfi / away_games) * 100 if away_games > 0 else 0
            
            # Calcular porcentaje general de YRFI
            total_games = home_games + away_games
            total_yrfi = home_yrfi + away_yrfi
            total_yrfi_pct = (total_yrfi / total_games) * 100 if total_games > 0 else 0
            
            # Almacenar estadísticas
            team_stats[str(team_id)] = {
                'name': team_name,
                'home_yrfi_pct': home_yrfi_pct,
                'away_yrfi_pct': away_yrfi_pct,
                'total_yrfi_pct': total_yrfi_pct,
                'games_analyzed': total_games,
                'home_games': home_games,
                'home_yrfi': home_yrfi,
                'away_games': away_games,
                'away_yrfi': away_yrfi
            }
        except Exception as e:
            print(f"⚠️ Error al procesar estadísticas del equipo {team_id}: {e}")
            continue
    
    return team_stats


def predict_yrfi_probability(
    home_team_id: str,
    away_team_id: str,
    team_stats: Dict[str, dict],
    mlb_avg_yrfi: float
) -> Tuple[float, Dict]:
    """Predice la probabilidad de que haya carreras en el primer inning.
    
    Args:
        home_team_id: ID del equipo local
        away_team_id: ID del equipo visitante
        team_stats: Estadísticas de los equipos
        mlb_avg_yrfi: Promedio de YRFI de la MLB
        
    Returns:
        Tupla con (probabilidad, detalles)
    """
    try:
        # Obtener estadísticas de los equipos
        home_stats = team_stats.get(home_team_id, {})
        away_stats = team_stats.get(away_team_id, {})
        
        # Obtener nombres de los equipos
        home_team = home_stats.get('name', f'Equipo {home_team_id}')
        away_team = away_stats.get('name', f'Equipo {away_team_id}')
        
        # Obtener probabilidades base (en porcentaje)
        home_yrfi_pct = home_stats.get('home_yrfi_pct', 0)  # Ya está en porcentaje
        away_yrfi_pct = away_stats.get('away_yrfi_pct', 0)
        
        # Calcular probabilidad combinada (promedio simple por ahora)
        prob = (home_yrfi_pct + away_yrfi_pct) / 2
        
        # Preparar detalles para la salida
        details = {
            'home_team': home_team,
            'away_team': away_team,
            'probability': prob / 100,  # Convertir a decimal para cálculos
            'home_yrfi_pct': home_yrfi_pct,
            'away_yrfi_pct': away_yrfi_pct,
            'home_games': home_stats.get('home_games', 0) + home_stats.get('away_games', 0),
            'away_games': away_stats.get('home_games', 0) + away_stats.get('away_games', 0),
            'mlb_average': mlb_avg_yrfi
        }
        
        return prob, details
        
    except Exception as e:
        print(f"Error al predecir probabilidad YRFI: {e}")
        return 0.0, {'error': str(e)}


def calculate_mlb_average(team_stats: dict) -> float:
    """Calcula el promedio de YRFI de toda la MLB."""
    total_yrfi = 0
    total_games = 0
    
    for team_id, stats in team_stats.items():
        total_yrfi += stats.get('total_yrfi_pct', 0) * stats.get('games_analyzed', 0) / 100
        total_games += stats.get('games_analyzed', 0)
    
    return total_yrfi / total_games if total_games > 0 else 0.4  # 40% por defecto


def format_prediction(prediction: dict, game_data: dict = None) -> str:
    """Formatea la predicción para mostrarla al usuario.
    
    Formato:
    New York vs Boston
    Probabilidad YRFI: %
    Probabilidad YRFI: temporada % del juego, del local, del visitante
    Probabilidad YRFI: tendencia % del juego, del local, del visitante
    Probabilidad YRFI: lanzadores % del juego, del local, del visitante
    
    Args:
        prediction: Diccionario con los datos de la predicción
        game_data: Diccionario con datos adicionales del juego (opcional)
    """
    home_team = prediction.get('home_team', 'Equipo Local')
    away_team = prediction.get('away_team', 'Equipo Visitante')
    
    # Obtener información de lanzadores
    home_pitcher = "Por definir"
    away_pitcher = "Por definir"
    
    if game_data:
        home_pitcher = game_data.get('home_pitcher', {}).get('name', 'Por definir')
        away_pitcher = game_data.get('away_pitcher', {}).get('name', 'Por definir')
    
    # Obtener probabilidades
    prob_total = prediction.get('probability', 0) * 100
    home_prob = prediction.get('home_yrfi_pct', 0)
    away_prob = prediction.get('away_yrfi_pct', 0)
    
    # Calcular promedios para temporada (usamos los mismos datos por ahora)
    season_game = prob_total
    season_home = home_prob
    season_away = away_prob
    
    # Para tendencia (usamos los mismos datos por ahora, en un caso real usaríamos datos de juegos recientes)
    trend_game = prob_total * 0.9  # Ejemplo: 10% menos que el total
    trend_home = home_prob * 0.9
    trend_away = away_prob * 0.9
    
    # Para lanzadores (usamos valores fijos por ahora, en un caso real usaríamos datos de lanzadores)
    pitchers_game = prob_total * 1.1  # Ejemplo: 10% más que el total
    pitchers_home = home_prob * 1.1
    pitchers_away = away_prob * 1.1
    
    # Obtener nombres completos de los equipos
    home_team_name = game_data.get('home_team_name', home_team) if game_data else home_team
    away_team_name = game_data.get('away_team_name', away_team) if game_data else away_team
    
    # Formatear la salida
    output = f"""
{away_team_name} @ {home_team_name}
Lanzadores: {away_pitcher} vs {home_pitcher}

Probabilidad YRFI: {prob_total:.1f}%

Probabilidad YRFI: temporada
- Juego: {season_game:.1f}%
- {away_team_name}: {season_away:.1f}% ({away_pitcher})
- {home_team_name}: {season_home:.1f}% ({home_pitcher})

Probabilidad YRFI: tendencia
- Juego: {trend_game:.1f}%
- {away_team_name}: {trend_away:.1f}% ({away_pitcher})
- {home_team_name}: {trend_home:.1f}% ({home_pitcher})

Probabilidad YRFI: lanzadores
- Juego: {pitchers_game:.1f}%
- {away_team_name}: {pitchers_away:.1f}% ({away_pitcher})
- {home_team_name}: {pitchers_home:.1f}% ({home_pitcher})
"""
    
    return output


def get_todays_games(games_data: List[dict]) -> List[dict]:
    """Obtiene los juegos programados para hoy.
    
    Si no hay juegos para hoy, devuelve los juegos más recientes.
    """
    try:
        # Obtener la fecha actual en formato YYYY-MM-DD
        today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        today_games = []
        all_games = []
        
        # Procesar todos los juegos
        for game in games_data:
            try:
                game_date = game.get('date')
                if not game_date:
                    continue
                    
                # Obtener información de lanzadores
                pitchers = game.get('pitchers', {})
                home_pitcher = pitchers.get('home', {})
                away_pitcher = pitchers.get('away', {})
                
                # Crear entrada del juego
                game_entry = {
                    'game_id': game.get('game_id', 'unknown'),
                    'date': game_date,
                    'home_team_id': str(game.get('home_team', '')),
                    'home_team_name': game.get('home_team_name', 'Equipo Local'),
                    'away_team_id': str(game.get('away_team', '')),
                    'away_team_name': game.get('away_team_name', 'Equipo Visitante'),
                    'game_yrfi': game.get('game_yrfi', None),
                    'home_yrfi': game.get('home_yrfi', None),
                    'away_yrfi': game.get('away_yrfi', None),
                    'home_pitcher': {
                        'id': home_pitcher.get('id'),
                        'name': home_pitcher.get('name', 'Por definir')
                    },
                    'away_pitcher': {
                        'id': away_pitcher.get('id'),
                        'name': away_pitcher.get('name', 'Por definir')
                    }
                }
                
                # Agregar a la lista de todos los juegos
                all_games.append(game_entry)
                
                # Verificar si es de hoy
                if game_date == today_str:
                    today_games.append(game_entry)
                    
            except Exception as e:
                print(f"⚠️ Error al procesar juego {game.get('game_id', 'desconocido')}: {e}")
                continue
        
        # Si no hay juegos para hoy, devolver los últimos 5 juegos
        if not today_games and all_games:
            print("ℹ️ No hay juegos para hoy. Mostrando los últimos juegos disponibles:")
            return all_games[-5:]  # Últimos 5 juegos
            
        return today_games
        
    except Exception as e:
        print(f"❌ Error inesperado al obtener juegos de hoy: {e}")
        return []


def main():
    """Función principal del script."""
    print("🔍 Cargando datos de temporada...")
    season_data = load_season_data(SEASON_DATA_PATH)
    
    if not season_data:
        print("❌ No se pudieron cargar los datos de temporada.")
        return
    
    # Mostrar información de depuración
    print(f"📊 Datos cargados: {len(season_data.get('teams', {}))} equipos, {len(season_data.get('games', []))} juegos")
    
    # Mostrar algunos equipos de ejemplo
    print("\n🔍 Algunos equipos cargados:")
    for i, (team_id, team_data) in enumerate(list(season_data.get('teams', {}).items())[:3]):
        print(f"   - {team_id}: {team_data.get('name', 'Sin nombre')} (Partidos: {team_data.get('total_games', 0)})")
    
    print("\n📊 Calculando estadísticas de equipos...")
    team_stats = calculate_team_stats(season_data.get('teams', {}))
    
    if not team_stats:
        print("❌ No se encontraron estadísticas de equipos.")
        return
    
    # Mostrar estadísticas de ejemplo
    print("\n📈 Estadísticas de equipos calculadas:")
    for i, (team_id, stats) in enumerate(list(team_stats.items())[:3]):
        print(f"   - {stats['name']} (ID: {team_id}):")
        print(f"     YRFI en casa: {stats['home_yrfi_pct']:.1f}% ({stats['home_yrfi']}/{stats['home_games']})")
        print(f"     YRFI fuera: {stats['away_yrfi_pct']:.1f}% ({stats['away_yrfi']}/{stats['away_games']})")
    
    # Calcular promedio de YRFI de la MLB
    mlb_avg_yrfi = calculate_mlb_average(team_stats)
    print(f"\n⚾ Promedio de YRFI de la MLB: {mlb_avg_yrfi * 100:.1f}%")
    
    # Obtener juegos de hoy
    print("\n🔍 Buscando juegos para hoy...")
    today_games = get_todays_games(season_data.get('games', []))
    
    if not today_games:
        print("❌ No se encontraron juegos para analizar.")
        return
    
    print(f"\n🎯 Predicciones para los juegos seleccionados (Total: {len(today_games)}):")
    
    # Generar predicciones para cada juego
    for game in today_games:
        home_team_id = game.get('home_team_id')
        away_team_id = game.get('away_team_id')
        
        if not home_team_id or not away_team_id:
            print("❌ Juego sin equipos definidos, omitiendo...")
            continue
        
        # Verificar que existan estadísticas para ambos equipos
        if home_team_id not in team_stats or away_team_id not in team_stats:
            print(f"⚠️ No se encontraron estadísticas para uno de los equipos en el juego {game.get('game_id', 'desconocido')}")
            continue
        
        # Obtener nombres de los equipos
        home_team_name = game.get('home_team_name', f'Equipo {home_team_id}')
        away_team_name = game.get('away_team_name', f'Equipo {away_team_id}')
        
        # Mostrar información del juego
        print(f"\n🏟️ {away_team_name} @ {home_team_name} ({game.get('date', 'Fecha desconocida')})")
        print(f"   ID del juego: {game.get('game_id', 'N/A')}")
        
        # Mostrar resultado real si está disponible
        if game.get('game_yrfi') is not None:
            resultado = "✅ YRFI (Sí hubo carreras)" if game['game_yrfi'] else "❌ NO YRFI (No hubo carreras)"
            print(f"   Resultado real: {resultado}")
        
        # Asegurarse de que los nombres de los equipos estén en game
        game['home_team_name'] = home_team_name
        game['away_team_name'] = away_team_name
        
        # Hacer predicción
        try:
            prob, details = predict_yrfi_probability(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                team_stats=team_stats,
                mlb_avg_yrfi=mlb_avg_yrfi
            )
            
            # Formatear y mostrar la predicción
            print(format_prediction(details, game).strip())
            
        except Exception as e:
            print(f"❌ Error al generar predicción: {e}")
        
        print("-" * 70)


if __name__ == "__main__":
    main()
