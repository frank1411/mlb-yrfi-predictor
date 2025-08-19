import json
import pandas as pd
import os
from datetime import datetime
from collections import defaultdict

# --- Parámetros de Configuración ---

# Constante de Credibilidad (C): El "peso" que le damos a la media de la liga.
# Un valor más alto significa que un pitcher necesita más juegos para que confiemos
# en su estadística personal. Un buen punto de partida es 15.
CREDIBILITY_CONSTANT_C = 15

# Nombres de los archivos de entrada y salida
import os
INPUT_JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'season_data.json')
OUTPUT_CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'partidos_mlb_para_ml.csv')

# Número de juegos para calcular la "tendencia reciente"
LAST_N_GAMES = 15

# --- Inicio del Script ---

def calculate_team_stats(team_id, games):
    """Calcula estadísticas para un equipo basado en sus juegos previos."""
    if not games:
        return {}
    
    # Filtrar solo juegos del equipo
    team_games = [g for g in games if g.get('home_team') == team_id or g.get('away_team') == team_id]
    
    if not team_games:
        return {}
    
    # Calcular estadísticas básicas
    total_games = len(team_games)
    total_yrfi = sum(1 for g in team_games if (g.get('home_team') == team_id and g.get('home_yrfi')) or 
                     (g.get('away_team') == team_id and g.get('away_yrfi')))
    
    # Últimos 10 juegos para tendencia
    recent_games = team_games[-10:]
    recent_yrfi = sum(1 for g in recent_games if (g.get('home_team') == team_id and g.get('home_yrfi')) or 
                      (g.get('away_team') == team_id and g.get('away_yrfi')))
    
    return {
        'games_played': total_games,
        'yrfi_percentage': total_yrfi / total_games if total_games > 0 else 0,
        'recent_yrfi_percentage': recent_yrfi / len(recent_games) if recent_games else 0
    }

def safe_get_pitcher_id(game, team_type):
    """Obtiene el ID del lanzador de manera segura."""
    try:
        return game.get('pitchers', {}).get(team_type, {}).get('id')
    except (AttributeError, TypeError):
        return None

def calculate_pitcher_stats(pitcher_id, games):
    """Calcula estadísticas para un lanzador basado en sus juegos previos."""
    if not games or not pitcher_id:
        return {}
    
    # Filtrar juegos donde el pitcher es abridor
    pitcher_games = []
    for game in games:
        if not isinstance(game, dict):
            continue
            
        home_pitcher = safe_get_pitcher_id(game, 'home')
        away_pitcher = safe_get_pitcher_id(game, 'away')
        
        if home_pitcher == pitcher_id or away_pitcher == pitcher_id:
            pitcher_games.append(game)
    
    if not pitcher_games:
        return {}
    
    # Calcular estadísticas básicas de manera segura
    total_starts = len(pitcher_games)
    total_yrfi = 0
    
    for g in pitcher_games:
        if not isinstance(g, dict):
            continue
            
        home_pitcher = safe_get_pitcher_id(g, 'home')
        away_pitcher = safe_get_pitcher_id(g, 'away')
        
        if home_pitcher == pitcher_id and 'home_yrfi' in g:
            total_yrfi += 1 if not g['home_yrfi'] else 0
        elif away_pitcher == pitcher_id and 'away_yrfi' in g:
            total_yrfi += 1 if not g['away_yrfi'] else 0
    
    # Calcular tendencia reciente (últimos 5 juegos)
    recent_games = pitcher_games[-5:]
    recent_yrfi = 0
    
    for g in recent_games:
        if not isinstance(g, dict):
            continue
            
        home_pitcher = safe_get_pitcher_id(g, 'home')
        away_pitcher = safe_get_pitcher_id(g, 'away')
        
        if home_pitcher == pitcher_id and 'home_yrfi' in g:
            recent_yrfi += 1 if not g['home_yrfi'] else 0
        elif away_pitcher == pitcher_id and 'away_yrfi' in g:
            recent_yrfi += 1 if not g['away_yrfi'] else 0
    
    return {
        'starts': total_starts,
        'yrfi_percentage': 1 - (total_yrfi / total_starts) if total_starts > 0 else 0,
        'recent_yrfi_percentage': 1 - (recent_yrfi / len(recent_games)) if recent_games else 0
    }

def process_season_data(input_file, output_file):
    """
    Carga los datos de la temporada desde un JSON, calcula las características
    para cada juego y guarda el resultado en un archivo CSV.
    """
    print(f"Cargando datos desde '{input_file}'...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer los juegos
    games = data.get('games', [])
    
    # Filtramos solo juegos finalizados ('F') para asegurar que tenemos el resultado
    final_games = [g for g in games if g.get('status', {}).get('statusCode') == 'F']
    
    # Ordenamos los juegos por fecha, de más antiguo a más reciente
    sorted_games = sorted(final_games, key=lambda x: x.get('date', '9999-12-31'))
    
    print(f"Se encontraron {len(sorted_games)} partidos finalizados. Procesando...")

    processed_data = []
    
    # Procesar cada partido
    for i, game in enumerate(sorted_games):
        if i % 100 == 0 and i > 0:
            print(f"Procesando partido {i+1}/{len(sorted_games)}...")
        
        # Obtener información básica del partido
        game_date = game.get('date')
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        home_pitcher = safe_get_pitcher_id(game, 'home')
        away_pitcher = safe_get_pitcher_id(game, 'away')
        
        # Si no hay información de lanzadores, usar valores por defecto
        if home_pitcher is None or away_pitcher is None:
            continue
        
        # Obtener juegos previos (historial hasta el momento del partido actual)
        history = sorted_games[:i]
        
        # Saltar si no hay suficiente historial
        if len(history) < 20:  # Mínimo de juegos para tener estadísticas significativas
            continue
        
        # Calcular estadísticas de equipos y lanzadores
        home_team_stats = calculate_team_stats(home_team, history)
        away_team_stats = calculate_team_stats(away_team, history)
        home_pitcher_stats = calculate_pitcher_stats(home_pitcher, history) if home_pitcher else {}
        away_pitcher_stats = calculate_pitcher_stats(away_pitcher, history) if away_pitcher else {}
        
        # Crear registro para el dataset
        record = {
            'game_id': game.get('game_id'),
            'date': game_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_pitcher': home_pitcher,
            'away_pitcher': away_pitcher,
            
            # Estadísticas del equipo local
            'home_team_yrfi_pct': home_team_stats.get('yrfi_percentage', 0),
            'home_team_recent_yrfi_pct': home_team_stats.get('recent_yrfi_percentage', 0),
            'home_team_games_played': home_team_stats.get('games_played', 0),
            
            # Estadísticas del equipo visitante
            'away_team_yrfi_pct': away_team_stats.get('yrfi_percentage', 0),
            'away_team_recent_yrfi_pct': away_team_stats.get('recent_yrfi_percentage', 0),
            'away_team_games_played': away_team_stats.get('games_played', 0),
            
            # Estadísticas del lanzador local
            'home_pitcher_yrfi_pct': home_pitcher_stats.get('yrfi_percentage', 0),
            'home_pitcher_recent_yrfi_pct': home_pitcher_stats.get('recent_yrfi_percentage', 0),
            'home_pitcher_starts': home_pitcher_stats.get('starts', 0),
            
            # Estadísticas del lanzador visitante
            'away_pitcher_yrfi_pct': away_pitcher_stats.get('yrfi_percentage', 0),
            'away_pitcher_recent_yrfi_pct': away_pitcher_stats.get('recent_yrfi_percentage', 0),
            'away_pitcher_starts': away_pitcher_stats.get('starts', 0),
            
            # Variable objetivo (1 si hubo carreras en la primera entrada, 0 si no)
            'target_yrfi': 1 if game.get('game_yrfi') else 0
        }
        
        processed_data.append(record)
    
    # Convertir a DataFrame y guardar a CSV
    if processed_data:
        print("\nCreando DataFrame y guardando en CSV...")
        df = pd.DataFrame(data=processed_data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        # Mostrar resumen de los datos
        print(f"\nResumen de los datos procesados:")
        print(f"- Total de partidos procesados: {len(processed_data)}")
        print(f"- Tasa de YRFI: {df['target_yrfi'].mean():.2%}")
        print(f"¡Éxito! Se ha creado el archivo '{output_file}' con {len(df)} filas.")
        
        # Mostrar un ejemplo de los datos
        print("\nEjemplo de las últimas 5 filas del archivo generado:")
        print(df.tail())
    else:
        print("No se encontraron datos para procesar.")

# --- Ejecutar el script ---
if __name__ == "__main__":
    process_season_data(INPUT_JSON_FILE, OUTPUT_CSV_FILE)