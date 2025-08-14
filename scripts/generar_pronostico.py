#!/usr/bin/env python3
"""
Script para generar pronósticos YRFI (Yes Run First Inning) para los partidos de MLB.
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

def load_season_data(file_path: str) -> Dict:
    """Carga los datos de la temporada desde el archivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_team_stats(season_data: Dict, team_id: str) -> Dict:
    """
    Obtiene las estadísticas de un equipo específico, incluyendo tendencia de últimos 15 partidos.
    
    Args:
        season_data: Diccionario con todos los datos de la temporada
        team_id: ID del equipo
        
    Returns:
        Diccionario con estadísticas del equipo
    """
    # Obtener estadísticas base del equipo
    team_stats = season_data.get('teams', {}).get(team_id, {
        'games': 0,
        'yrfi': 0,
        'home_games': 0,
        'home_yrfi': 0,
        'away_games': 0,
        'away_yrfi': 0,
        'last_15_games': 0,
        'last_15_yrfi': 0
    })
    
    # Si no hay juegos, devolver las estadísticas base
    if 'games' not in season_data or not season_data['games']:
        return team_stats
    
    # Filtrar los últimos 15 juegos del equipo
    team_games = []
    for game in season_data['games']:
        # Verificar si el equipo participó en el juego
        if game.get('home_team') == team_id or game.get('away_team') == team_id:
            team_games.append(game)
    
    # Ordenar por fecha (más reciente primero)
    # Convertir fechas a objetos datetime para ordenación correcta
    team_games.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), '%Y-%m-%d'), reverse=True)
    
    # Tomar los últimos 15 juegos (ya están ordenados del más reciente al más antiguo)
    last_15_games = team_games[:15]
    
    # Depuración: Mostrar fechas de los últimos 15 juegos
    print(f"\nÚltimos 15 partidos para el equipo {team_id}:")
    for i, game in enumerate(last_15_games, 1):
        print(f"{i}. {game.get('date')} - {game.get('home_team_name', '?')} vs {game.get('away_team_name', '?')} - ", end="")
        if game.get('home_team') == team_id:
            print(f"Local - YRFI: {game.get('home_yrfi', False)}")
        else:
            print(f"Visitante - YRFI: {game.get('away_yrfi', False)}")
    print(f"Total YRFI en últimos 15: {sum(1 for g in last_15_games if (g.get('home_team') == team_id and g.get('home_yrfi')) or (g.get('away_team') == team_id and g.get('away_yrfi')))}")
    
    # Calcular estadísticas de los últimos 15 juegos
    last_15_yrfi = 0
    for game in last_15_games:
        if game.get('home_team') == team_id and game.get('home_yrfi', False):
            last_15_yrfi += 1
        elif game.get('away_team') == team_id and game.get('away_yrfi', False):
            last_15_yrfi += 1
    
    # Actualizar estadísticas con los últimos 15 juegos
    team_stats.update({
        'last_15_games': len(last_15_games),
        'last_15_yrfi': last_15_yrfi
    })
    
    return team_stats

def get_pitcher_stats(season_data: Dict, pitcher_id: Optional[str] = None, pitcher_name: Optional[str] = None) -> Dict:
    """
    Obtiene las estadísticas de un lanzador específico por ID o nombre.
    
    Args:
        season_data: Datos de la temporada
        pitcher_id: ID del lanzador (opcional)
        pitcher_name: Nombre del lanzador (opcional)
    """
    print(f"\n[DEBUG] Buscando lanzador - ID: {pitcher_id}, Tipo: {type(pitcher_id).__name__}, Nombre: {pitcher_name}")
    
    # Verificar si el lanzador es "Por anunciar"
    is_tba = pitcher_name and 'anunciar' in str(pitcher_name).lower()
    
    # Si es "Por anunciar", establecer valores predeterminados con 50%
    if is_tba:
        return {
            'total_games': 0,
            'yrfi_games': 0,
            'home_games': 0,
            'home_yrfi': 0,
            'away_games': 0,
            'away_yrfi': 0,
            'yrfi_pct': 50.0,  # 50% para lanzadores "Por anunciar"
            'home_yrfi_pct': 50.0,
            'away_yrfi_pct': 50.0,
            'name': pitcher_name,
            'is_tba': True  # Marcar como "Por anunciar"
        }
    
    # Valores predeterminados para lanzadores conocidos
    pitcher_stats = {
        'total_games': 0,
        'yrfi_games': 0,
        'home_games': 0,
        'home_yrfi': 0,
        'away_games': 0,
        'away_yrfi': 0,
        'yrfi_pct': 0.0,
        'home_yrfi_pct': 0.0,
        'away_yrfi_pct': 0.0,
        'name': pitcher_name or 'Desconocido',
        'is_tba': False  # No es "Por anunciar"
    }
    
    if not (pitcher_id or pitcher_name):
        return pitcher_stats
    
    # Buscar en los juegos
    for game in season_data.get('games', []):
        if 'pitchers' not in game:
            continue
            
        game_date = game.get('date', 'Fecha desconocida')
        home_team = game.get('home_team', 'Equipo local')
        away_team = game.get('away_team', 'Equipo visitante')
            
        # Verificar lanzador local
        home_pitcher = game.get('pitchers', {}).get('home')
        if home_pitcher and isinstance(home_pitcher, dict):
            home_pitcher_id = str(home_pitcher.get('id', ''))
            home_pitcher_name = home_pitcher.get('name', 'Desconocido')
            
            id_match = pitcher_id and home_pitcher_id == str(pitcher_id)
            name_match = pitcher_name and pitcher_name.lower() in home_pitcher_name.lower()
            
            if id_match or name_match:
                print(f"[DEBUG] Partido encontrado - Fecha: {game_date}, {away_team} @ {home_team}")
                print(f"[DEBUG] Lanzador local: {home_pitcher_name} (ID: {home_pitcher_id})")
                print(f"[DEBUG] away_yrfi: {game.get('away_yrfi', False)}")
                
                pitcher_stats['total_games'] += 1
                pitcher_stats['home_games'] += 1
                # Contar si el equipo visitante anotó (away_yrfi) cuando el lanzador local está en el juego
                if game.get('away_yrfi', False):
                    pitcher_stats['yrfi_games'] += 1
                    pitcher_stats['home_yrfi'] += 1
                
        # Verificar lanzador visitante
        away_pitcher = game.get('pitchers', {}).get('away')
        if away_pitcher and isinstance(away_pitcher, dict):
            away_pitcher_id = str(away_pitcher.get('id', ''))
            away_pitcher_name = away_pitcher.get('name', 'Desconocido')
            
            id_match = pitcher_id and away_pitcher_id == str(pitcher_id)
            name_match = pitcher_name and pitcher_name.lower() in away_pitcher_name.lower()
            
            if id_match or name_match:
                print(f"[DEBUG] Partido encontrado - Fecha: {game_date}, {away_team} @ {home_team}")
                print(f"[DEBUG] Lanzador visitante: {away_pitcher_name} (ID: {away_pitcher_id})")
                print(f"[DEBUG] home_yrfi: {game.get('home_yrfi', False)}")
                
                pitcher_stats['total_games'] += 1
                pitcher_stats['away_games'] += 1
                # Contar si el equipo local anotó (home_yrfi) cuando el lanzador visitante está en el juego
                if game.get('home_yrfi', False):
                    pitcher_stats['yrfi_games'] += 1
                    pitcher_stats['away_yrfi'] += 1
    
    # Calcular porcentajes
    if pitcher_stats['total_games'] > 0:
        pitcher_stats['yrfi_pct'] = (pitcher_stats['yrfi_games'] / pitcher_stats['total_games']) * 100
    if pitcher_stats['home_games'] > 0:
        pitcher_stats['home_yrfi_pct'] = (pitcher_stats['home_yrfi'] / pitcher_stats['home_games']) * 100
    if pitcher_stats['away_games'] > 0:
        pitcher_stats['away_yrfi_pct'] = (pitcher_stats['away_yrfi'] / pitcher_stats['away_games']) * 100
    
    return pitcher_stats

def calculate_game_probability(home_team_id: str, away_team_id: str, home_pitcher: Dict, away_pitcher: Dict, season_data: Dict) -> Dict:
    """
    Calcula la probabilidad de YRFI para un partido.
    
    Returns:
        Dict con las probabilidades y estadísticas detalladas, incluyendo todos los valores intermedios
        necesarios para la generación de informes.
    """
    # Obtener estadísticas de los equipos
    home_stats = get_team_stats(season_data, home_team_id)
    away_stats = get_team_stats(season_data, away_team_id)
    
    # Calcular promedios base
    home_yrfi_pct = (home_stats.get('home_yrfi', 0) / home_stats.get('home_games', 1)) * 100 if home_stats.get('home_games', 0) > 0 else 0
    away_yrfi_pct = (away_stats.get('away_yrfi', 0) / away_stats.get('away_games', 1)) * 100 if away_stats.get('away_games', 0) > 0 else 0
    
    # Calcular tendencias (últimos 15 partidos)
    home_trend_pct = (home_stats.get('last_15_yrfi', 0) / home_stats.get('last_15_games', 1)) * 100 if home_stats.get('last_15_games', 0) > 0 else home_yrfi_pct
    away_trend_pct = (away_stats.get('last_15_yrfi', 0) / away_stats.get('last_15_games', 1)) * 100 if away_stats.get('last_15_games', 0) > 0 else away_yrfi_pct
    
    # Calcular estadísticas combinadas para cada equipo (45% base, 55% tendencia)
    home_yrfi_combined = (home_yrfi_pct * 0.45) + (home_trend_pct * 0.55)
    away_yrfi_combined = (away_yrfi_pct * 0.45) + (away_trend_pct * 0.55)
    
    # Calcular probabilidad base usando la fórmula de probabilidad conjunta
    p_home_no_yrfi = 1 - (home_yrfi_combined / 100)
    p_away_no_yrfi = 1 - (away_yrfi_combined / 100)
    base_prob = (1 - (p_home_no_yrfi * p_away_no_yrfi)) * 100  # Convertir a porcentaje
    
    # Obtener el rendimiento YRFI de los lanzadores
    home_pitcher_yrfi = home_pitcher.get('yrfi_pct', home_pitcher.get('yrfi_allowed', 50.0))
    away_pitcher_yrfi = away_pitcher.get('yrfi_pct', away_pitcher.get('yrfi_allowed', 50.0))
    
    # Aplicar el ajuste (65% rendimiento del equipo, 35% rendimiento del lanzador rival)
    home_team_adj = (home_yrfi_combined * 0.65) + (away_pitcher_yrfi * 0.35)
    away_team_adj = (away_yrfi_combined * 0.65) + (home_pitcher_yrfi * 0.35)
    
    # Asegurar que los valores estén dentro del rango 0-100
    home_team_adj = max(0, min(100, home_team_adj))
    away_team_adj = max(0, min(100, away_team_adj))
    
    # Calcular la probabilidad final del partido
    p_home = home_team_adj / 100
    p_away = away_team_adj / 100
    final_prob = (1 - (1 - p_home) * (1 - p_away)) * 100
    
    # Devolver todos los valores intermedios necesarios para los informes
    return {
        'base_prob': base_prob / 100,  # Convertir a decimal
        'final_prob': final_prob / 100,  # Convertir a decimal
        'home_team': {
            'id': home_team_id,
            'name': home_stats.get('name', ''),
            'yrfi_pct': home_yrfi_pct,
            'yrfi': home_stats.get('home_yrfi', 0),
            'games': home_stats.get('home_games', 0),
            'last_15_games': home_stats.get('last_15_games', 0),
            'last_15_yrfi': home_stats.get('last_15_yrfi', 0),
            'trend_pct': home_trend_pct,
            'combined_pct': home_yrfi_combined,
            'adjusted_yrfi_pct': home_team_adj,
            'stats': {
                'base': {
                    'value': home_yrfi_pct,
                    'ratio': f"{home_stats.get('home_yrfi', 0)}/{home_stats.get('home_games', 1)}"
                },
                'tendency': {
                    'value': home_trend_pct,
                    'ratio': f"{home_stats.get('last_15_yrfi', 0)}/{home_stats.get('last_15_games', 1)}"
                },
                'combined': home_yrfi_combined,
                'adjusted': home_team_adj,
                'pitcher_impact': away_pitcher_yrfi
            }
        },
        'away_team': {
            'id': away_team_id,
            'name': away_stats.get('name', ''),
            'yrfi_pct': away_yrfi_pct,
            'yrfi': away_stats.get('away_yrfi', 0),
            'games': away_stats.get('away_games', 0),
            'last_15_games': away_stats.get('last_15_games', 0),
            'last_15_yrfi': away_stats.get('last_15_yrfi', 0),
            'trend_pct': away_trend_pct,
            'combined_pct': away_yrfi_combined,
            'adjusted_yrfi_pct': away_team_adj,
            'stats': {
                'base': {
                    'value': away_yrfi_pct,
                    'ratio': f"{away_stats.get('away_yrfi', 0)}/{away_stats.get('away_games', 1)}"
                },
                'tendency': {
                    'value': away_trend_pct,
                    'ratio': f"{away_stats.get('last_15_yrfi', 0)}/{away_stats.get('last_15_games', 1)}"
                },
                'combined': away_yrfi_combined,
                'adjusted': away_team_adj,
                'pitcher_impact': home_pitcher_yrfi
            }
        },
        'home_pitcher': {
            'name': home_pitcher.get('name', 'Por definir'),
            'yrfi_allowed': home_pitcher_yrfi,
            'yrfi_ratio': f"{home_pitcher.get('yrfi_games', 0)}/{home_pitcher.get('total_games', 1)}",
            'yrfi_used': home_pitcher_yrfi
        },
        'away_pitcher': {
            'name': away_pitcher.get('name', 'Por definir'),
            'yrfi_allowed': away_pitcher_yrfi,
            'yrfi_ratio': f"{away_pitcher.get('yrfi_games', 0)}/{away_pitcher.get('total_games', 1)}",
            'yrfi_used': away_pitcher_yrfi
        },
        'calculation': {
            'home_team': {
                'base': home_yrfi_pct,
                'tendency': home_trend_pct,
                'combined': home_yrfi_combined,
                'pitcher_impact': away_pitcher_yrfi,
                'adjusted': home_team_adj
            },
            'away_team': {
                'base': away_yrfi_pct,
                'tendency': away_trend_pct,
                'combined': away_yrfi_combined,
                'pitcher_impact': home_pitcher_yrfi,
                'adjusted': away_team_adj
            },
            'game_yrfi_probability': final_prob,
            'formula': {
                'combined': "(0.45 × Estadística Base) + (0.55 × Tendencia Reciente)",
                'adjusted': "(0.65 × Puntuación Combinada) + (0.35 × Rendimiento Lanzador Rival)",
                'final': "1 - ((1 - P_local) × (1 - P_visitante))"
            }
        },
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'data_source': 'season_data.json',
            'weights': {
                'base_vs_trend': {'base': 0.45, 'trend': 0.55},
                'team_vs_pitcher': {'team': 0.65, 'pitcher': 0.35}
            }
        }
    }

def format_prediction(game_data: Dict, home_team_name: str, away_team_name: str, game_date: str) -> str:
    """Formatea la predicción en un string legible.
    
    Args:
        game_data: Diccionario con los datos del partido y predicciones
        home_team_name: Nombre del equipo local
        away_team_name: Nombre del equipo visitante
        game_date: Fecha del partido en formato YYYY-MM-DD
        
    Returns:
        str: Texto formateado con la predicción
    """
    # Obtener datos de los equipos
    home_team = game_data['home_team']
    away_team = game_data['away_team']
    home_pitcher = game_data['home_pitcher']
    away_pitcher = game_data['away_pitcher']
    
    # Usar directamente los valores calculados y ajustados
    home_trend_pct = (home_team['last_15_yrfi'] / home_team['last_15_games'] * 100) if home_team['last_15_games'] > 0 else 0
    away_trend_pct = (away_team['last_15_yrfi'] / away_team['last_15_games'] * 100) if away_team['last_15_games'] > 0 else 0

    # Valores ajustados y finales desde calculate_game_probability
    home_combined = home_team['adjusted_yrfi_pct']
    away_combined = away_team['adjusted_yrfi_pct']
    final_prob = game_data.get('final_prob', 0) * 100  # Convertir a porcentaje si viene en decimal

    # Obtener estadísticas de lanzadores
    home_pitcher_name = home_pitcher.get('name', 'Por definir')
    away_pitcher_name = away_pitcher.get('name', 'Por definir')
    home_pitcher_yrfi = home_pitcher.get('yrfi_used', home_pitcher.get('yrfi_allowed', 0))
    away_pitcher_yrfi = away_pitcher.get('yrfi_used', away_pitcher.get('yrfi_allowed', 0))

    # Ratios
    home_pitcher_yrfi_count = home_pitcher.get('yrfi', 0)
    home_pitcher_total = home_pitcher.get('games', 1)
    away_pitcher_yrfi_count = away_pitcher.get('yrfi', 0)
    away_pitcher_total = away_pitcher.get('games', 1)
    home_pitcher_ratio = f"{home_pitcher_yrfi_count}/{home_pitcher_total}"
    away_pitcher_ratio = f"{away_pitcher_yrfi_count}/{away_pitcher_total}"
    
    # Calcular valores intermedios para mostrar en el reporte
    home_combined_calc = (home_team['yrfi_pct'] * 0.45 + home_trend_pct * 0.55)
    away_combined_calc = (away_team['yrfi_pct'] * 0.45 + away_trend_pct * 0.55)

    prediction = [
        f"# Análisis YRFI - {away_team_name} @ {home_team_name} ({game_date})\n",
        "## Información del Partido\n",
        f"**{away_team_name} (Visitante) vs {home_team_name} (Local)**  \n",
        f"**Lanzadores:** {away_pitcher_name} (@{away_team_name}) vs {home_pitcher_name} (@{home_team_name})\n\n",
        "## Probabilidades YRFI\n\n",
        f"### Probabilidad YRFI del Partido\n",
        f"**{final_prob:.1f}%** (probabilidad final ajustada)\n\n",
        f"### Probabilidad YRFI del Equipo Local\n",
        f"**{home_combined:.1f}%** de que {home_team_name} anote en la primera entrada (ajustado)\n",
        f"- Basado en:\n",
        f"  - Rendimiento de {home_team_name} como local: {home_team['yrfi_pct']:.1f}% ({home_team['yrfi']}/{home_team['games']} partidos)\n",
        f"  - Tendencia últimos 15 juegos: {home_trend_pct:.1f}% ({home_team['last_15_yrfi']}/{home_team['last_15_games']} partidos)\n",
        f"  - Rendimiento del lanzador visitante: {away_pitcher_yrfi:.1f}% YRFI permitido ({away_pitcher_ratio})\n\n",
        f"### Probabilidad YRFI del Equipo Visitante\n",
        f"**{away_combined:.1f}%** de que {away_team_name} anote en la primera entrada (ajustado)\n",
        f"- Basado en:\n",
        f"  - Rendimiento de {away_team_name} como visitante: {away_team['yrfi_pct']:.1f}% ({away_team['yrfi']}/{away_team['games']} partidos)\n",
        f"  - Tendencia últimos 15 juegos: {away_trend_pct:.1f}% ({away_team['last_15_yrfi']}/{away_team['last_15_games']} partidos)\n",
        f"  - Rendimiento del lanzador local: {home_pitcher_yrfi:.1f}% YRFI permitido ({home_pitcher_ratio})\n\n",
        "## Cálculo Detallado\n\n",
        "### 1. Estadísticas Base (Temporada Completa)\n",
        f"- **{home_team_name} (Local):** {home_team['yrfi_pct']:.1f}% ({home_team['yrfi']}/{home_team['games']} partidos)\n",
        f"- **{away_team_name} (Visitante):** {away_team['yrfi_pct']:.1f}% ({away_team['yrfi']}/{away_team['games']} partidos)\n\n",
        "### 2. Tendencia Reciente (últimos 15 partidos)\n",
        f"- **{home_team_name} (Local):** {home_trend_pct:.1f}% ({home_team['last_15_yrfi']}/{home_team['last_15_games']} partidos)\n",
        f"- **{away_team_name} (Visitante):** {away_trend_pct:.1f}% ({away_team['last_15_yrfi']}/{away_team['last_15_games']} partidos)\n\n",
        "### 3. Impacto de los Lanzadores\n",
        f"- **{home_pitcher_name} (Local):** {home_pitcher_yrfi:.1f}% YRFI permitido ({home_pitcher_ratio})\n",
        f"- **{away_pitcher_name} (Visitante):** {away_pitcher_yrfi:.1f}% YRFI permitido ({away_pitcher_ratio})\n\n",
        "### 4. Cálculo de Probabilidades\n",
        f"1. **Ponderación Base vs. Tendencia (45% base, 55% tendencia):**\n",
        f"   - {home_team_name}: (45% × {home_team['yrfi_pct']:.1f}%) + (55% × {home_trend_pct:.1f}%) = {home_combined_calc:.1f}%\n",
        f"   - {away_team_name}: (45% × {away_team['yrfi_pct']:.1f}%) + (55% × {away_trend_pct:.1f}%) = {away_combined_calc:.1f}%\n\n",
        f"2. **Ajuste por Lanzadores (65% equipo, 35% lanzador rival):**\n",
        f"   - {home_team_name}: (65% × {home_combined_calc:.1f}%) + (35% × {away_pitcher_yrfi:.1f}%) = {home_combined:.1f}%\n",
        f"   - {away_team_name}: (65% × {away_combined_calc:.1f}%) + (35% × {home_pitcher_yrfi:.1f}%) = {away_combined:.1f}%\n\n",
        f"3. **Probabilidad Final YRFI (eventos independientes):**\n",
        f"   - Fórmula: 1 - ((1 - {home_combined/100:.3f}) × (1 - {away_combined/100:.3f}))\n",
        f"   - Resultado: **{final_prob:.1f}%**\n"
    ]
    
    return "".join(prediction)
    ap_ratio = game_data['away_pitcher'].get('yrfi_ratio', 'N/A')
    prediction += f"- **{ap_name} ({away_team_name} - Visitante)**:\n"
    prediction += f"  - Rendimiento YRFI: {ap_yrfi:.1f}% ({ap_ratio})\n"
    
    # Tendencia
    prediction += f"### Tendencia (Últimos 15 partidos)\n"
    if game_data['home_team']['last_15_games'] > 0:
        home_trend = (game_data['home_team']['last_15_yrfi'] / game_data['home_team']['last_15_games']) * 100
        prediction += f"- **{home_team_name}:** {home_trend:.1f}% ({game_data['home_team']['last_15_yrfi']}/{game_data['home_team']['last_15_games']} partidos)\n"
    else:
        prediction += f"- **{home_team_name}:** Sin datos recientes\n"
        
    if game_data['away_team']['last_15_games'] > 0:
        away_trend = (game_data['away_team']['last_15_yrfi'] / game_data['away_team']['last_15_games']) * 100
        prediction += f"- **{away_team_name}:** {away_trend:.1f}% ({game_data['away_team']['last_15_yrfi']}/{game_data['away_team']['last_15_games']} partidos)\n\n"
    else:
        prediction += f"- **{away_team_name}:** Sin datos recientes\n\n"
    
    # Rendimiento de lanzadores
    prediction += "### Rendimiento de Lanzadores\n"
    
    # Lanzador local
    hp_yrfi = game_data['home_pitcher'].get('home_yrfi_pct', 0)
    hp_games = game_data['home_pitcher'].get('home_games', 0)
    prediction += f"- **{hp_name} ({home_team_name} - Local):**\n"
    if hp_games > 0:
        prediction += f"  - Total: {hp_yrfi:.1f}% ({game_data['home_pitcher'].get('home_yrfi', 0)}/{hp_games} aperturas)\n"
    else:
        prediction += "  - Sin datos suficientes\n"
    
    # Lanzador visitante
    ap_yrfi = game_data['away_pitcher'].get('away_yrfi_pct', 0)
    ap_games = game_data['away_pitcher'].get('away_games', 0)
    prediction += f"- **{ap_name} ({away_team_name} - Visitante):**\n"
    if ap_games > 0:
        prediction += f"  - Total: {ap_yrfi:.1f}% ({game_data['away_pitcher'].get('away_yrfi', 0)}/{ap_games} aperturas)\n"
    else:
        prediction += "  - Sin datos suficientes\n"
    
    # Resumen
    prediction += "\n## Resumen de Cálculos\n"
    prediction += "| Categoría | {:<20} | {:<20} | Promedio |\n".format(home_team_name[:20], away_team_name[:20])
    prediction += "|-----------|{0}|{0}|----------|\n".format("-"*22)
    
    # Línea de base
    prediction += "| **Base** | {:.1f}% ({}/{}) | {:.1f}% ({}/{}) | {:.1f}% |\n".format(
        game_data['home_team']['yrfi_pct'], 
        game_data['home_team']['yrfi'], 
        game_data['home_team']['games'],
        game_data['away_team']['yrfi_pct'],
        game_data['away_team']['yrfi'],
        game_data['away_team']['games'],
        game_data['base_prob']*100
    )
    
    # Obtener los valores ajustados del game_data
    home_adj = game_data['home_team']['adjusted_yrfi_pct']
    away_adj = game_data['away_team']['adjusted_yrfi_pct']
    final_prob = game_data['final_prob'] * 100  # Convertir a porcentaje
    
    # Línea de ajuste
    prediction += "| **Ajustado** | {:.1f}% | {:.1f}% | **{:.1f}%** |\n".format(
        home_combined, away_combined, final_prob
    )
    
    # Línea de tendencia (usar valores ya calculados)
    home_trend = home_trend_pct
    away_trend = away_trend_pct
    
    prediction += "| **Tendencia** | {:.1f}% ({}/{}) | {:.1f}% ({}/{}) | - |\n".format(
        home_trend, game_data['home_team']['last_15_yrfi'], game_data['home_team']['last_15_games'],
        away_trend, game_data['away_team']['last_15_yrfi'], game_data['away_team']['last_15_games']
    )
    
    # Línea de lanzadores (usar yrfi_used que ya incluye el ajuste)
    prediction += "| **Lanzador** | {:.1f}% ({}/{}) | {:.1f}% ({}/{}) | - |\n".format(
        home_pitcher_yrfi, game_data['home_pitcher'].get('yrfi', 0), home_pitcher_total,
        away_pitcher_yrfi, game_data['away_pitcher'].get('yrfi', 0), away_pitcher_total
    )
    
    # Nota final
    prediction += "\n**Nota:** La probabilidad final del partido ({:.1f}%) se calcula considerando tanto el rendimiento histórico de los equipos como el rendimiento específico de los lanzadores en sus respectivos roles (visitante/local). Los cálculos utilizan las siguientes ponderaciones:".format(final_prob)
    prediction += """
- 45% estadísticas base de la temporada
- 55% tendencia reciente (últimos 15 partidos)
- 65% rendimiento del equipo
- 35% rendimiento del lanzador contrario

### 📝 Fórmula de Cálculo

La probabilidad final de que anoten en la primera entrada se calcula en tres pasos:

1. **Puntuación combinada** para cada equipo (45% estadística base + 55% tendencia reciente):
   - `Puntuación = (0.45 × Estadística Base) + (0.55 × Tendencia Reciente)`

2. **Ajuste por lanzador** (65% puntuación combinada + 35% impacto del lanzador contrario):
   - `Puntuación Ajustada = (0.65 × Puntuación) + (0.35 × Rendimiento Lanzador Rival)`

3. **Probabilidad final** considerando ambos equipos como eventos independientes:
   - `Probabilidad Final = 1 - ((1 - P_local) × (1 - P_visitante))`
   - Donde P_local y P_visitante son las probabilidades ajustadas convertidas a decimal (0-1)
"""
    
    return prediction

def generate_prediction(home_team_id: str, away_team_id: str, home_pitcher_name: str, away_pitcher_name: str, 
                        home_team_name: str = None, away_team_name: str = None, game_date: str = None) -> Dict:
    """
    Genera una predicción YRFI para un partido.
    
    Args:
        home_team_id: ID del equipo local
        away_team_id: ID del equipo visitante
        home_pitcher_name: Nombre del lanzador local
        away_pitcher_name: Nombre del lanzador visitante
        home_team_name: Nombre del equipo local (opcional)
        away_team_name: Nombre del equipo visitante (opcional)
        game_date: Fecha del partido en formato YYYY-MM-DD (opcional)
        
    Returns:
        Dict con la predicción y metadatos
    """
    # Cargar datos de la temporada
    data_dir = Path(__file__).parent.parent / 'data'
    data_file = data_dir / 'season_data.json'
    season_data = load_season_data(data_file)
    
    # Obtener estadísticas de los lanzadores
    home_pitcher = get_pitcher_stats(season_data, pitcher_name=home_pitcher_name)
    away_pitcher = get_pitcher_stats(season_data, pitcher_name=away_pitcher_name)
    
    # Calcular probabilidades
    game_data = calculate_game_probability(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        home_pitcher=home_pitcher,
        away_pitcher=away_pitcher,
        season_data=season_data
    )
    
    # Formatear nombres de equipos si no se proporcionan
    if not home_team_name:
        home_team_name = f"Equipo {home_team_id}"
    if not away_team_name:
        away_team_name = f"Equipo {away_team_id}"
    
    # Usar fecha actual si no se proporciona
    if not game_date:
        game_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generar predicción formateada
    prediction_text = format_prediction(game_data, home_team_name, away_team_name, game_date)
    
    # Crear resultado
    result = {
        'game_date': game_date,
        'home_team': {
            'id': home_team_id,
            'name': home_team_name,
            'pitcher': home_pitcher_name,
            'yrfi_pct': game_data['home_team']['yrfi_pct']
        },
        'away_team': {
            'id': away_team_id,
            'name': away_team_name,
            'pitcher': away_pitcher_name,
            'yrfi_pct': game_data['away_team']['yrfi_pct']
        },
        'prediction': {
            'base_prob': game_data['base_prob'],
            'final_prob': game_data['final_prob']
        },
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'data_source': str(data_file)
        }
    }
    
    return result

def save_prediction(prediction: Dict, output_dir: Path = None) -> Path:
    """
    Guarda la predicción en un archivo JSON.
    
    Args:
        prediction: Diccionario con los datos de la predicción
        output_dir: Directorio de salida (opcional)
        
    Returns:
        Ruta al archivo guardado
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'predictions'
    
    # Crear directorio si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo usando la fecha y el ID del partido para garantizar unicidad
    current_date = datetime.now().strftime("%Y-%m-%d")
    home_team = prediction['home_team']['name'].replace(' ', '_')
    away_team = prediction['away_team']['name'].replace(' ', '_')
    game_pk = prediction.get('game_pk', 'N/A')  # Obtener el ID del partido
    
    # Crear nombre de archivo con el formato: yrfi_YYYY-MM-DD_away_at_home_GAME_PK.json
    filename = f"yrfi_{current_date}_{away_team}_at_{home_team}_{game_pk}.json"
    filepath = output_dir / filename
    
    # Guardar como JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(prediction, f, indent=2, ensure_ascii=False)
    
    return filepath

def main():
    """
    Función principal para ejecutar el script desde la línea de comandos.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Generar pronóstico YRFI para un partido de MLB')
    parser.add_argument('--home-team', required=True, help='ID del equipo local')
    parser.add_argument('--away-team', required=True, help='ID del equipo visitante')
    parser.add_argument('--home-pitcher', required=True, help='Nombre del lanzador local')
    parser.add_argument('--away-pitcher', required=True, help='Nombre del lanzador visitante')
    parser.add_argument('--home-name', help='Nombre del equipo local (opcional)')
    parser.add_argument('--away-name', help='Nombre del equipo visitante (opcional)')
    parser.add_argument('--date', help='Fecha del partido (YYYY-MM-DD, opcional)')
    parser.add_argument('--output-dir', help='Directorio de salida para los archivos (opcional)')
    
    args = parser.parse_args()
    
    # Generar predicción
    prediction = generate_prediction(
        home_team_id=args.home_team,
        away_team_id=args.away_team,
        home_pitcher_name=args.home_pitcher,
        away_pitcher_name=args.away_pitcher,
        home_team_name=args.home_name,
        away_team_name=args.away_name,
        game_date=args.date
    )
    
    # Guardar predicción
    output_dir = Path(args.output_dir) if args.output_dir else None
    saved_file = save_prediction(prediction, output_dir)
    
    # Mostrar resumen
    print(f"\n✅ Predicción generada exitosamente:")
    print(f"📊 Probabilidad YRFI: {prediction['prediction']['final_prob']*100:.1f}%")
    print(f"📂 Archivo guardado: {saved_file}")
    print(f"📝 Vista previa:\n")
    print("\n".join(prediction['prediction']['text'].split("\n")[:10]) + "\n...")

if __name__ == "__main__":
    main()
