#!/usr/bin/env python3
"""
Script para generar predicciones de YRFI basadas en estadísticas de temporada completa
y tendencias recientes, con ponderación personalizable.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.data.data_manager import load_season_data
from src.yrfi_calculator import YRFICalculator

def format_prediction(prediction_details: Dict) -> str:
    """
    Formatea los detalles de la predicción para mostrarlos al usuario.
    
    Args:
        prediction_details: Detalles de la predicción
        
    Returns:
        str: Texto formateado
    """
    lines = []
    details = prediction_details
    
    # Encabezado
    lines.append("=" * 80)
    lines.append(f"PREDICCIÓN YRFI: {details['home_team']['name']} vs {details['away_team']['name']}")
    lines.append("=" * 80)
    
    # Probabilidades
    probs = details['probabilities']
    lines.append(f"\nPROBABILIDADES:")
    lines.append(f"- Temporada completa: {probs['season']*100:.1f}%")
    lines.append(f"- Tendencias recientes: {probs['recent']*100:.1f}%")
    lines.append(f"- Ponderación: Temporada ({probs['season_weight']*100:.0f}%) + Recientes ({probs['recent_weight']*100:.0f}%)")
    lines.append(f"- Probabilidad final: {probs['final']*100:.1f}%")
    
    # Estadísticas de equipos
    lines.append("\nESTADÍSTICAS DE EQUIPOS:")
    
    # Equipo local
    lines.append(f"\n{details['home_team']['name']} (Local):")
    lines.append(f"  Temporada: {details['home_team']['season']['yrfi_pct']*100:.1f}% YRFI "
               f"({details['home_team']['season']['games_analyzed']} partidos)")
    
    if details['home_team']['recent']['games_analyzed'] > 0:
        lines.append(f"  Últimos {details['home_team']['recent']['games_analyzed']} partidos: "
                   f"{details['home_team']['recent']['yrfi_pct']*100:.1f}% YRFI")
    
    # Equipo visitante
    lines.append(f"\n{details['away_team']['name']} (Visitante):")
    lines.append(f"  Temporada: {details['away_team']['season']['yrfi_pct']*100:.1f}% YRFI "
               f"({details['away_team']['season']['games_analyzed']} partidos)")
    
    if details['away_team']['recent']['games_analyzed'] > 0:
        lines.append(f"  Últimos {details['away_team']['recent']['games_analyzed']} partidos: "
                   f"{details['away_team']['recent']['yrfi_pct']*100:.1f}% YRFI")
    
    # Estadísticas de lanzadores si están disponibles
    if details['home_pitcher'] or details['away_pitcher']:
        lines.append("\nLANZADORES:")
        
        if details['home_pitcher'] and details['home_pitcher']['starts_analyzed'] > 0:
            p = details['home_pitcher']
            lines.append(f"\n{p['name']} ({details['home_team']['name']} - Local):")
            lines.append(f"  - YRFI en {p['yrfi_pct']*100:.1f}% de sus aperturas")
            lines.append(f"  - Promedio de carreras permitidas en 1er inning: {p['avg_runs_allowed_1st']:.2f}")
            lines.append(f"  - Aperturas analizadas: {p['starts_analyzed']}")
        
        if details['away_pitcher'] and details['away_pitcher']['starts_analyzed'] > 0:
            p = details['away_pitcher']
            lines.append(f"\n{p['name']} ({details['away_team']['name']} - Visitante):")
            lines.append(f"  - YRFI en {p['yrfi_pct']*100:.1f}% de sus aperturas")
            lines.append(f"  - Promedio de carreras permitidas en 1er inning: {p['avg_runs_allowed_1st']:.2f}")
            lines.append(f"  - Aperturas analizadas: {p['starts_analyzed']}")
    
    # Últimos partidos recientes
    lines.append("\nÚLTIMOS PARTIDOS RECIENTES:")
    
    # Mostrar últimos 5 partidos del equipo local
    home_games = details['home_team']['recent'].get('recent_games', [])[:5]
    if home_games:
        lines.append(f"\n{details['home_team']['name']} (últimos {len(home_games)} partidos):")
        for game in home_games:
            vs = "vs" if game['is_home'] else "@"
            opponent = game.get('opponent_name', 'Rival')
            yrfi = "SÍ" if game['yrfi'] else "NO"
            lines.append(f"  - {game['date']} {vs} {opponent}: {game['team_runs_1st']}-{game['opponent_runs_1st']} (YRFI: {yrfi})")
    
    # Mostrar últimos 5 partidos del equipo visitante
    away_games = details['away_team']['recent'].get('recent_games', [])[:5]
    if away_games:
        lines.append(f"\n{details['away_team']['name']} (últimos {len(away_games)} partidos):")
        for game in away_games:
            vs = "vs" if game['is_home'] else "@"
            opponent = game.get('opponent_name', 'Rival')
            yrfi = "SÍ" if game['yrfi'] else "NO"
            lines.append(f"  - {game['date']} {vs} {opponent}: {game['team_runs_1st']}-{game['opponent_runs_1st']} (YRFI: {yrfi})")
    
    # Recomendación basada en la probabilidad
    prob = details['probabilities']['final']
    if prob >= 0.6:
        recommendation = "Fuerte apuesta a YRFI (Sí habrá carreras en el primer inning)"
    elif prob >= 0.55:
        recommendation = "Apuesta moderada a YRFI"
    elif prob >= 0.45:
        recommendation = "Sin apuesta clara"
    elif prob >= 0.4:
        recommendation = "Apuesta moderada a NO YRFI"
    else:
        recommendation = "Fuerte apuesta a NO YRFI"
    
    lines.append("\n" + "=" * 80)
    lines.append(f"RECOMENDACIÓN: {recommendation}")
    lines.append("=" * 80)
    
    return "\n".join(lines)

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Genera predicciones de YRFI combinando estadísticas de temporada y tendencias recientes.')
    parser.add_argument('home_team_id', type=str, help='ID del equipo local')
    parser.add_argument('away_team_id', type=str, help='ID del equipo visitante')
    parser.add_argument('--home-pitcher', type=str, help='ID del lanzador local (opcional)')
    parser.add_argument('--away-pitcher', type=str, help='ID del lanzador visitante (opcional)')
    parser.add_argument('--season-weight', type=float, default=0.6,
                       help='Peso para estadísticas de temporada (0-1, default: 0.6)')
    parser.add_argument('--recent-weight', type=float, default=0.4,
                       help='Peso para estadísticas recientes (0-1, default: 0.4)')
    parser.add_argument('--window-size', type=int, default=15,
                       help='Número de partidos a considerar para tendencias recientes (default: 15)')
    
    args = parser.parse_args()
    
    # Cargar datos de la temporada
    try:
        print("Cargando datos de la temporada...")
        season_data = load_season_data()
    except Exception as e:
        print(f"Error al cargar los datos de la temporada: {e}")
        return
    
    # Inicializar calculadora
    calculator = YRFICalculator(season_data, window_size=args.window_size)
    
    # Generar predicción
    try:
        prob, details = calculator.predict_yrfi_probability(
            home_team_id=args.home_team_id,
            away_team_id=args.away_team_id,
            home_pitcher_id=args.home_pitcher,
            away_pitcher_id=args.away_pitcher,
            season_weight=args.season_weight,
            recent_weight=args.recent_weight
        )
        
        # Mostrar resultados
        print("\n" + "=" * 80)
        print(f"PREDICCIÓN YRFI: {details['home_team']['name']} vs {details['away_team']['name']}")
        print("=" * 80)
        print(f"Probabilidad de YRFI: {prob*100:.1f}%")
        print("\nEjecute el script con --help para ver más opciones.")
        
        # Preguntar si desea ver el informe detallado
        if input("\n¿Desea ver el informe detallado? (s/n): ").lower() == 's':
            print("\n" + "=" * 80)
            print(format_prediction(details))
    
    except Exception as e:
        print(f"\nError al generar la predicción: {e}")
        return

if __name__ == "__main__":
    main()
