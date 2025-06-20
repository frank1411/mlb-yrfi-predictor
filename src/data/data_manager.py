"""
Módulo para manejar la carga y guardado de datos locales.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple

def get_first_inning_yrfi(game_data: Dict) -> Dict[str, bool]:
    """
    Determina si hubo carreras en el primer inning de un partido.
    
    Args:
        game_data: Diccionario con los datos del partido.
        
    Returns:
        Diccionario con booleanos indicando si hubo carreras en el primer inning
        para cada equipo (local y visitante) y para el juego en general.
    """
    home_runs = 0
    away_runs = 0
    
    # Intentar con la estructura estándar
    if 'linescore' in game_data and 'innings' in game_data['linescore']:
        for inning in game_data['linescore']['innings']:
            if inning.get('num') == 1:  # Primer inning
                home_runs = inning.get('home', {}).get('runs', 0)
                away_runs = inning.get('away', {}).get('runs', 0)
                break
    # Intentar con estructura alternativa
    elif 'innings' in game_data:
        for inning in game_data['innings']:
            if inning.get('num') == 1:  # Primer inning
                home_runs = inning.get('home', {}).get('runs', 0)
                away_runs = inning.get('away', {}).get('runs', 0)
                break
    
    home_yrfi = home_runs > 0
    away_yrfi = away_runs > 0
    
    return {
        'home_yrfi': home_yrfi,
        'away_yrfi': away_yrfi,
        'game_yrfi': home_yrfi or away_yrfi
    }

# Configuración de rutas
DATA_DIR = Path(__file__).parent.parent.parent / "data"
SEASON_DATA_FILE = DATA_DIR / "season_data.json"
LAST_UPDATE_FILE = DATA_DIR / "last_update.txt"

# Asegurar que el directorio de datos exista
os.makedirs(DATA_DIR, exist_ok=True)

def save_season_data(data: Dict[str, Any]) -> None:
    """
    Guarda los datos de la temporada en un archivo JSON con el formato optimizado.
    
    Args:
        data: Diccionario con los datos de la temporada a guardar.
    """
    # Asegurarse de que el directorio de datos exista
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Crear estructura de datos optimizada
    optimized_data = {
        'last_updated': datetime.now().isoformat(),
        'teams': {},
        'pitchers': {},
        'games': []
    }
    
    # Procesar equipos
    for team_id, team_data in data.get('teams', {}).items():
        optimized_data['teams'][team_id] = {
            'name': team_data.get('name', 'Desconocido'),
            'total_games': team_data.get('total_games', 0),
            'total_yrfi': team_data.get('total_yrfi', 0),
            'home_games': team_data.get('home_games', 0),
            'home_yrfi': team_data.get('home_yrfi', 0),
            'away_games': team_data.get('away_games', 0),
            'away_yrfi': team_data.get('away_yrfi', 0)
        }
    
    # Procesar lanzadores
    for pitcher_id, pitcher_data in data.get('pitchers', {}).items():
        optimized_data['pitchers'][pitcher_id] = {
            'name': pitcher_data.get('name', 'Desconocido'),
            'team_id': pitcher_data.get('team_id', ''),
            'starts': pitcher_data.get('starts', 0),
            'yrfi_starts': pitcher_data.get('yrfi_starts', 0)
        }
    
    # Procesar juegos
    for game in data.get('games', []):
        try:
            # Si el juego ya está en formato optimizado, usarlo directamente
            if all(key in game for key in ['game_id', 'home_team', 'away_team', 'home_yrfi', 'away_yrfi', 'game_yrfi']):
                optimized_data['games'].append(game)
                continue
                
            # Obtener YRFI para el juego
            yrfi_data = get_first_inning_yrfi(game)
            
            # Manejar diferentes formatos de juego
            if 'teams' in game and 'home' in game['teams'] and 'away' in game['teams']:
                # Formato completo de la API
                home_team_id = str(game['teams']['home']['team']['id'])
                away_team_id = str(game['teams']['away']['team']['id'])
                home_pitcher = game['teams']['home'].get('probablePitcher', {}) or {}
                away_pitcher = game['teams']['away'].get('probablePitcher', {}) or {}
            else:
                # Formato optimizado parcial
                home_team_id = str(game.get('home_team', ''))
                away_team_id = str(game.get('away_team', ''))
                home_pitcher = {}
                away_pitcher = {}
            
            optimized_game = {
                'game_id': game.get('game_id', get_game_id(game)),
                'date': game.get('date', game.get('gameDate', '')),
                'home_team': home_team_id,
                'away_team': away_team_id,
                'home_yrfi': game.get('home_yrfi', yrfi_data.get('home_yrfi', False)),
                'away_yrfi': game.get('away_yrfi', yrfi_data.get('away_yrfi', False)),
                'game_yrfi': game.get('game_yrfi', yrfi_data.get('game_yrfi', False))
            }
            
            # Agregar lanzadores si están disponibles
            if 'home_pitcher' in game:
                optimized_game['home_pitcher'] = str(game['home_pitcher'])
            elif home_pitcher and 'id' in home_pitcher:
                optimized_game['home_pitcher'] = str(home_pitcher['id'])
                
            if 'away_pitcher' in game:
                optimized_game['away_pitcher'] = str(game['away_pitcher'])
            elif away_pitcher and 'id' in away_pitcher:
                optimized_game['away_pitcher'] = str(away_pitcher['id'])
            
            optimized_data['games'].append(optimized_game)
            
        except Exception as e:
            print(f"Error procesando juego {game.get('game_id', 'desconocido')}: {str(e)}")
            continue
    
    # Guardar los datos en el archivo
    with open(SEASON_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(optimized_data, f, ensure_ascii=False, indent=2)
    
    # Actualizar la fecha de última actualización
    with open(LAST_UPDATE_FILE, 'w', encoding='utf-8') as f:
        f.write(optimized_data['last_updated'])

def load_season_data() -> Dict[str, Any]:
    """
    Carga los datos de la temporada desde el archivo JSON.
    
    Returns:
        Diccionario con los datos de la temporada en el formato optimizado.
    """
    if not os.path.exists(SEASON_DATA_FILE):
        return {
            'last_updated': '',
            'teams': {},
            'pitchers': {},
            'games': []
        }
    
    try:
        with open(SEASON_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Verificar si es el formato antiguo
            if 'teams' in data and 'games' in data and 'pitchers' in data and 'last_updated' not in data:
                # Convertir del formato antiguo al nuevo formato
                return _convert_legacy_data(data)
                
            return data
            
    except Exception as e:
        print(f"Error al cargar los datos de la temporada: {e}")
        return {
            'last_updated': '',
            'teams': {},
            'pitchers': {},
            'games': []
        }

def _convert_legacy_data(legacy_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte los datos del formato antiguo al nuevo formato optimizado.
    
    Args:
        legacy_data: Datos en el formato antiguo.
        
    Returns:
        Datos en el nuevo formato optimizado.
    """
    optimized_data = {
        'last_updated': datetime.now().isoformat(),
        'teams': {},
        'pitchers': {},
        'games': []
    }
    
    # Procesar equipos
    for team_id, team_data in legacy_data.get('teams', {}).items():
        optimized_data['teams'][team_id] = {
            'name': team_data.get('name', 'Desconocido'),
            'total_games': team_data.get('games', 0),
            'total_yrfi': team_data.get('yrfi_games', 0),
            'home_games': team_data.get('home_games', 0),
            'home_yrfi': team_data.get('home_yrfi', 0),
            'away_games': team_data.get('away_games', 0),
            'away_yrfi': team_data.get('away_yrfi', 0)
        }
    
    # Procesar lanzadores
    for pitcher_id, pitcher_data in legacy_data.get('pitchers', {}).items():
        optimized_data['pitchers'][pitcher_id] = {
            'name': pitcher_data.get('name', 'Desconocido'),
            'team_id': pitcher_data.get('team_id', ''),
            'starts': pitcher_data.get('starts', 0),
            'yrfi_starts': pitcher_data.get('yrfi_starts', 0)
        }
    
    # Procesar juegos
    for game in legacy_data.get('games', []):
        # Obtener YRFI para el juego
        yrfi_data = get_first_inning_yrfi(game)
        
        optimized_game = {
            'game_id': get_game_id(game),
            'date': game.get('gameDate', ''),
            'home_team': str(game['teams']['home']['team']['id']),
            'away_team': str(game['teams']['away']['team']['id']),
            'home_yrfi': yrfi_data['home_yrfi'],
            'away_yrfi': yrfi_data['away_yrfi'],
            'game_yrfi': yrfi_data['game_yrfi']
        }
        
        # Agregar lanzadores si están disponibles
        home_pitcher = game['teams']['home'].get('probablePitcher', {}) or {}
        if home_pitcher and 'id' in home_pitcher:
            optimized_game['home_pitcher'] = str(home_pitcher['id'])
            
        away_pitcher = game['teams']['away'].get('probablePitcher', {}) or {}
        if away_pitcher and 'id' in away_pitcher:
            optimized_game['away_pitcher'] = str(away_pitcher['id'])
        
        optimized_data['games'].append(optimized_game)
    
    return optimized_data

def get_last_update_date() -> Optional[datetime]:
    """
    Obtiene la fecha de la última actualización.
    
    Returns:
        Objeto datetime con la fecha de la última actualización, o None si no se puede determinar.
    """
    # Primero intentar cargar los datos para ver si ya están en el nuevo formato
    try:
        data = load_season_data()
        if data and 'last_updated' in data and data['last_updated']:
            return datetime.fromisoformat(data['last_updated'])
    except Exception:
        pass
    
    # Si no está en el nuevo formato, intentar con el archivo de última actualización
    if os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, 'r', encoding='utf-8') as f:
                date_str = f.read().strip()
                if date_str:  # Asegurarse de que no esté vacío
                    return datetime.fromisoformat(date_str)
        except (FileNotFoundError, ValueError):
            pass
    
    return None

def get_game_id(game: Dict) -> str:
    """Obtiene el ID único de un juego de diferentes formatos posibles."""
    # Intentar diferentes claves posibles para el ID del juego
    if 'gamePk' in game:
        return str(game['gamePk'])
    elif 'game_pk' in game:
        return str(game['game_pk'])
    elif 'id' in game:
        return str(game['id'])
    elif 'gameID' in game:
        return str(game['gameID'])
    else:
        # Si no se encuentra un ID, generar uno basado en los equipos y la fecha
        try:
            home_team = game.get('teams', {}).get('home', {}).get('team', {}).get('id', 'UNK')
            away_team = game.get('teams', {}).get('away', {}).get('team', {}).get('id', 'UNK')
            game_date = game.get('gameDate', '')[:10]  # Tomar solo la fecha (YYYY-MM-DD)
            return f"{game_date}_{home_team}_{away_team}"
        except Exception:
            # Si todo falla, usar un hash del diccionario completo
            return str(hash(frozenset(game.items())))

def merge_games(existing_games: List[Dict], new_games: List[Dict]) -> List[Dict]:
    """Combina listas de juegos, eliminando duplicados."""
    # Usar un diccionario para evitar duplicados por ID de juego
    games_dict = {}
    
    # Primero añadir los juegos existentes
    for game in existing_games:
        try:
            game_id = get_game_id(game)
            games_dict[game_id] = game
        except Exception as e:
            print(f"Error al procesar juego existente: {e}")
            continue
    
    # Luego añadir/actualizar con los nuevos juegos
    for game in new_games:
        try:
            game_id = get_game_id(game)
            games_dict[game_id] = game
        except Exception as e:
            print(f"Error al procesar nuevo juego: {e}")
            continue
    
    return list(games_dict.values())

def update_team_stats(teams_data: Dict, games: List[Dict]) -> Dict:
    """
    Actualiza las estadísticas de los equipos basado en los juegos proporcionados.
    Incluye estadísticas generales y de tendencia de los últimos 15 juegos.
    
    Args:
        teams_data: Diccionario con las estadísticas actuales de los equipos.
        games: Lista de diccionarios con información de los juegos.
        
    Returns:
        Diccionario con las estadísticas actualizadas de los equipos.
    """
    # Ordenar juegos por fecha (más recientes primero)
    sorted_games = sorted(
        games,
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d') if isinstance(x.get('date'), str) else x.get('date', datetime.min),
        reverse=True
    )
    
    # Inicializar estadísticas de equipos si no existen
    for team_id in {game.get('home_team') for game in games if game.get('home_team')} | \
                   {game.get('away_team') for game in games if game.get('away_team')}:
        if team_id and team_id not in teams_data:
            teams_data[team_id] = {
                'name': f'Equipo {team_id}',  # Se actualizará con el nombre real más adelante
                'total_games': 0,
                'total_yrfi': 0,
                'home_games': 0,
                'home_yrfi': 0,
                'away_games': 0,
                'away_yrfi': 0,
                'last_home_games': 0,
                'last_home_yrfi': 0,
                'last_away_games': 0,
                'last_away_yrfi': 0
            }
    
    # Obtener nombres de equipos de los juegos
    for game in games:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        
        if home_team and home_team in teams_data and 'name' not in teams_data[home_team]:
            teams_data[home_team]['name'] = game.get('teams', {}).get('home', {}).get('team', {}).get('name', f'Equipo {home_team}')
        
        if away_team and away_team in teams_data and 'name' not in teams_data[away_team]:
            teams_data[away_team]['name'] = game.get('teams', {}).get('away', {}).get('team', {}).get('name', f'Equipo {away_team}')
    
    # Procesar cada juego para actualizar estadísticas generales
    for game in games:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        
        if not home_team or not away_team:
            continue
            
        home_yrfi = game.get('home_yrfi', False)
        away_yrfi = game.get('away_yrfi', False)
        
        # Actualizar estadísticas del equipo local
        if home_team in teams_data:
            teams_data[home_team]['total_games'] += 1
            teams_data[home_team]['home_games'] += 1
            if home_yrfi:
                teams_data[home_team]['total_yrfi'] += 1
                teams_data[home_team]['home_yrfi'] += 1
        
        # Actualizar estadísticas del equipo visitante
        if away_team in teams_data:
            teams_data[away_team]['total_games'] += 1
            teams_data[away_team]['away_games'] += 1
            if away_yrfi:
                teams_data[away_team]['total_yrfi'] += 1
                teams_data[away_team]['away_yrfi'] += 1
    
    # Calcular estadísticas de tendencia (últimos 15 juegos por equipo)
    team_last_games = {team_id: [] for team_id in teams_data}
    
    # Recolectar los últimos 15 juegos por equipo
    for game in sorted_games:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        
        if not home_team or not away_team:
            continue
        
        home_yrfi = game.get('home_yrfi', False)
        away_yrfi = game.get('away_yrfi', False)
        
        # Agregar a los últimos juegos del equipo local
        if home_team in team_last_games and len(team_last_games[home_team]) < 15:
            team_last_games[home_team].append({
                'is_home': True,
                'yrfi': home_yrfi
            })
        
        # Agregar a los últimos juegos del equipo visitante
        if away_team in team_last_games and len(team_last_games[away_team]) < 15:
            team_last_games[away_team].append({
                'is_home': False,
                'yrfi': away_yrfi
            })
    
    # Calcular estadísticas de tendencia
    for team_id, last_games in team_last_games.items():
        if team_id not in teams_data:
            continue
            
        last_home_games = [g for g in last_games if g['is_home']]
        last_away_games = [g for g in last_games if not g['is_home']]
        
        teams_data[team_id].update({
            'last_home_games': len(last_home_games),
            'last_home_yrfi': sum(1 for g in last_home_games if g['yrfi']),
            'last_away_games': len(last_away_games),
            'last_away_yrfi': sum(1 for g in last_away_games if g['yrfi'])
        })
    
    return teams_data


def get_pitcher_yrfi_stats(pitcher_id: str, games: List[Dict]) -> Dict:
    """
    Obtiene las estadísticas YRFI de un lanzador específico basado en juegos históricos.
    
    Args:
        pitcher_id: ID del lanzador.
        games: Lista de juegos para analizar.
        
    Returns:
        Diccionario con las estadísticas del lanzador.
    """
    stats = {
        'total_starts': 0,
        'total_yrfi': 0,
        'home_starts': 0,
        'home_yrfi': 0,
        'away_starts': 0,
        'away_yrfi': 0
    }
    
    for game in games:
        # Verificar si el lanzador es el abridor local
        home_pitcher = game.get('home_pitcher', {})
        if isinstance(home_pitcher, dict) and str(home_pitcher.get('id')) == str(pitcher_id):
            stats['total_starts'] += 1
            stats['home_starts'] += 1
            if game.get('away_yrfi', False):
                stats['total_yrfi'] += 1
                stats['home_yrfi'] += 1
        
        # Verificar si el lanzador es el abridor visitante
        away_pitcher = game.get('away_pitcher', {})
        if isinstance(away_pitcher, dict) and str(away_pitcher.get('id')) == str(pitcher_id):
            stats['total_starts'] += 1
            stats['away_starts'] += 1
            if game.get('home_yrfi', False):
                stats['total_yrfi'] += 1
                stats['away_yrfi'] += 1
    
    # Calcular porcentajes
    stats['total_yrfi_pct'] = (stats['total_yrfi'] / stats['total_starts'] * 100) if stats['total_starts'] > 0 else 0
    stats['home_yrfi_pct'] = (stats['home_yrfi'] / stats['home_starts'] * 100) if stats['home_starts'] > 0 else 0
    stats['away_yrfi_pct'] = (stats['away_yrfi'] / stats['away_starts'] * 100) if stats['away_starts'] > 0 else 0
    
    return stats

def get_game_pitchers_yrfi_stats(game: Dict, games: List[Dict]) -> Dict:
    """
    Obtiene las estadísticas YRFI de los lanzadores de un juego específico.
    
    Args:
        game: Información del juego a analizar.
        games: Lista de juegos históricos para calcular estadísticas.
        
    Returns:
        Diccionario con las estadísticas de los lanzadores del juego.
    """
    result = {
        'home_pitcher': None,
        'away_pitcher': None
    }
    
    # Obtener estadísticas del lanzador local
    home_pitcher = game.get('home_pitcher', {})
    if isinstance(home_pitcher, dict) and 'id' in home_pitcher:
        result['home_pitcher'] = {
            'id': home_pitcher['id'],
            'name': home_pitcher.get('name', 'Desconocido'),
            'stats': get_pitcher_yrfi_stats(home_pitcher['id'], games)
        }
    
    # Obtener estadísticas del lanzador visitante
    away_pitcher = game.get('away_pitcher', {})
    if isinstance(away_pitcher, dict) and 'id' in away_pitcher:
        result['away_pitcher'] = {
            'id': away_pitcher['id'],
            'name': away_pitcher.get('name', 'Desconocido'),
            'stats': get_pitcher_yrfi_stats(away_pitcher['id'], games)
        }
    
    return result
