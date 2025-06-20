#!/usr/bin/env python3
"""
Script para generar predicciones de YRFI basadas en los datos locales.

Este script puede generar tanto predicciones básicas como informes detallados de YRFI.
"""
import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import load_season_data
from src.trend_analyzer import TrendAnalyzer

def calculate_team_yrfi_percentage(team_id: str, team_data: Dict, is_home: bool) -> float:
    """
    Calcula el porcentaje de YRFI para un equipo en condición de local o visitante.
    
    Args:
        team_id: ID del equipo
        team_data: Datos del equipo
        is_home: Si es True, calcula para juegos como local; si es False, como visitante
        
    Returns:
        Porcentaje de YRFI (0-1)
    """
    if not team_data:
        return 0.0
    
    total_games = team_data['home_games'] if is_home else team_data['away_games']
    yrfi_games = team_data['home_yrfi'] if is_home else team_data['away_yrfi']
    
    if total_games == 0:
        return 0.0
    
    return yrfi_games / total_games

def get_pitcher_yrfi_percentage(pitcher_stats: Dict, is_home: bool = True) -> float:
    """
    Obtiene el porcentaje de YRFI para un lanzador.
    
    Args:
        pitcher_stats: Estadísticas del lanzador (del data manager)
        is_home: Si es True, devuelve estadísticas como local; si es False, como visitante
        
    Returns:
        Porcentaje de YRFI (0-1)
    """
    if not pitcher_stats:
        return 0.5  # Valor por defecto si no hay datos
    
    if is_home:
        starts = pitcher_stats.get('home_starts', 0)
        yrfi = pitcher_stats.get('home_yrfi', 0)
    else:
        starts = pitcher_stats.get('away_starts', 0)
        yrfi = pitcher_stats.get('away_yrfi', 0)
    
    # Si no hay suficientes aperturas, usar el total
    if starts < 3:
        total_starts = pitcher_stats.get('total_starts', 0)
        if total_starts > 0:
            return pitcher_stats.get('total_yrfi', 0) / total_starts
        return 0.5  # Valor por defecto si no hay datos
    
    return yrfi / starts if starts > 0 else 0.5

def predict_yrfi_probability(
    home_team_id: str, 
    away_team_id: str, 
    home_pitcher_id: Optional[str], 
    away_pitcher_id: Optional[str], 
    season_data: Dict,
    trend_analyzer: Optional[TrendAnalyzer] = None
) -> Tuple[float, Dict]:
    """
    Predice la probabilidad de que haya carreras en el primer inning basado en:
    - Rendimiento de equipos (temporada completa y tendencia reciente)
    - Rendimiento de lanzadores
    - Promedio de la liga
    
    Ponderaciones del modelo:
    - Equipos (temporada completa): 20% (10% local, 10% visitante)
    - Tendencias recientes (últimos 15 partidos): 20% (10% local, 10% visitante)
    - Lanzadores: 30% (15% local, 15% visitante) o 0% si no hay datos
    - Promedio de la MLB: 30% o más si faltan otros datos
    
    Args:
        home_team_id: ID del equipo local
        away_team_id: ID del equipo visitante
        home_pitcher_id: ID del lanzador local (opcional)
        away_pitcher_id: ID del lanzador visitante (opcional)
        season_data: Datos de la temporada
        trend_analyzer: Instancia de TrendAnalyzer para calcular tendencias recientes
        
    Returns:
        Tuple[float, Dict]: Probabilidad (0-1) y detalles de la predicción
    """
    # Verificar que los datos de la temporada sean válidos
    if not season_data or 'teams' not in season_data:
        raise ValueError("Datos de temporada inválidos o faltantes")
    
    # Obtener datos de los equipos
    home_team_data = season_data['teams'].get(home_team_id, {})
    away_team_data = season_data['teams'].get(away_team_id, {})
    
    # Verificar que los equipos tengan datos suficientes
    if not home_team_data or not away_team_data:
        missing_teams = []
        if not home_team_data:
            missing_teams.append(f"local ({home_team_id})")
        if not away_team_data:
            missing_teams.append(f"visitante ({away_team_id})")
        raise ValueError(f"No se encontraron datos para los equipos: {', '.join(missing_teams)}")
    
    # Calcular porcentajes de YRFI para la temporada completa
    home_team_yrfi = calculate_team_yrfi_percentage(home_team_id, home_team_data, is_home=True)
    away_team_yrfi = calculate_team_yrfi_percentage(away_team_id, away_team_data, is_home=False)
    
    # Inicializar variables para tendencias recientes
    home_recent_yrfi = None
    away_recent_yrfi = None
    recent_home_games = []
    recent_away_games = []
    
    # Calcular tendencias recientes si está disponible el analizador
    if trend_analyzer:
        try:
            # Obtener juegos recientes (últimos 15) para el equipo local
            recent_home_games = trend_analyzer.get_team_games(
                home_team_id, 
                limit=15, 
                is_home=True
            )
            
            if recent_home_games:
                home_recent_yrfi = sum(1 for g in recent_home_games if g.get('first_inning_run', 0) > 0) / len(recent_home_games)
            
            # Obtener juegos recientes (últimos 15) para el equipo visitante
            recent_away_games = trend_analyzer.get_team_games(
                away_team_id, 
                limit=15, 
                is_home=False
            )
            
            if recent_away_games:
                away_recent_yrfi = sum(1 for g in recent_away_games if g.get('first_inning_run', 0) > 0) / len(recent_away_games)
                
        except Exception as e:
            print(f"Error al calcular tendencias recientes: {e}")
    
    # Obtener estadísticas de lanzadores
    home_pitcher_yrfi = None
    away_pitcher_yrfi = None
    home_pitcher_data = {}
    away_pitcher_data = {}
    
    if home_pitcher_id and 'pitchers' in season_data and home_pitcher_id in season_data['pitchers']:
        home_pitcher_data = season_data['pitchers'][home_pitcher_id]
        home_pitcher_yrfi = get_pitcher_yrfi_percentage(home_pitcher_data, is_home=True)
    
    if away_pitcher_id and 'pitchers' in season_data and away_pitcher_id in season_data['pitchers']:
        away_pitcher_data = season_data['pitchers'][away_pitcher_id]
        away_pitcher_yrfi = get_pitcher_yrfi_percentage(away_pitcher_data, is_home=False)
    
    # Calcular promedio de la MLB
    total_yrfi = sum(t.get('total_yrfi', 0) for t in season_data['teams'].values())
    total_games = sum(t.get('total_games', 0) for t in season_data['teams'].values())
    mlb_avg_yrfi = total_yrfi / total_games if total_games > 0 else 0.3  # 30% por defecto
    
    # Determinar qué componentes están disponibles para el cálculo
    has_season_data = True  # Siempre deberíamos tener datos de temporada
    has_recent_data = home_recent_yrfi is not None or away_recent_yrfi is not None
    has_pitcher_data = home_pitcher_yrfi is not None or away_pitcher_yrfi is not None
    
    # Ajustar ponderaciones según los datos disponibles
    if has_recent_data and has_pitcher_data:
        # Todos los componentes disponibles
        weights = {
            'home_team': 0.1,    # 10%
            'away_team': 0.1,    # 10%
            'home_recent': 0.1,  # 10%
            'away_recent': 0.1,  # 10%
            'home_pitcher': 0.15, # 15%
            'away_pitcher': 0.15, # 15%
            'mlb_avg': 0.3       # 30%
        }
    elif has_recent_data:
        # Sin datos de lanzadores, redistribuir su peso al promedio de la MLB
        weights = {
            'home_team': 0.1,    # 10%
            'away_team': 0.1,    # 10%
            'home_recent': 0.1,  # 10%
            'away_recent': 0.1,  # 10%
            'home_pitcher': 0.0,  # 0% (no disponible)
            'away_pitcher': 0.0,  # 0% (no disponible)
            'mlb_avg': 0.6       # 60% (30% original + 30% de lanzadores)
        }
    elif has_pitcher_data:
        # Sin datos recientes, redistribuir su peso a temporada completa
        weights = {
            'home_team': 0.2,    # 20% (10% + 10% de tendencias)
            'away_team': 0.2,    # 20% (10% + 10% de tendencias)
            'home_recent': 0.0,  # 0% (no disponible)
            'away_recent': 0.0,  # 0% (no disponible)
            'home_pitcher': 0.15, # 15%
            'away_pitcher': 0.15, # 15%
            'mlb_avg': 0.3       # 30%
        }
    else:
        # Solo datos de temporada y promedio de la MLB
        weights = {
            'home_team': 0.2,    # 20% (10% + 10% de tendencias)
            'away_team': 0.2,    # 20% (10% + 10% de tendencias)
            'home_recent': 0.0,  # 0% (no disponible)
            'away_recent': 0.0,  # 0% (no disponible)
            'home_pitcher': 0.0,  # 0% (no disponible)
            'away_pitcher': 0.0,  # 0% (no disponible)
            'mlb_avg': 0.6       # 60% (30% + 30% de lanzadores)
        }
    
    # Calcular contribución de cada componente
    components = {
        'home_team': home_team_yrfi * weights['home_team'],
        'away_team': away_team_yrfi * weights['away_team'],
        'home_recent': (home_recent_yrfi if home_recent_yrfi is not None else home_team_yrfi) * weights['home_recent'],
        'away_recent': (away_recent_yrfi if away_recent_yrfi is not None else away_team_yrfi) * weights['away_recent'],
        'home_pitcher': (home_pitcher_yrfi if home_pitcher_yrfi is not None else mlb_avg_yrfi) * weights['home_pitcher'],
        'away_pitcher': (away_pitcher_yrfi if away_pitcher_yrfi is not None else mlb_avg_yrfi) * weights['away_pitcher'],
        'mlb_avg': mlb_avg_yrfi * weights['mlb_avg']
    }
    
    # Calcular probabilidad final
    final_prob = sum(components.values())
    
    # Asegurar que la probabilidad esté entre 0 y 1
    final_prob = max(0.0, min(1.0, final_prob))
    
    # Obtener datos de los equipos desde season_data
    home_team_data = season_data.get('teams', {}).get(home_team_id, {})
    away_team_data = season_data.get('teams', {}).get(away_team_id, {})
    
    # 9. Calcular el promedio de la MLB
    total_yrfi = 0
    total_games = 0
    
    # Sumar todos los YRFI y juegos de todos los equipos
    for team_id, team_data in season_data.get('teams', {}).items():
        total_yrfi += team_data.get('home_yrfi', 0) + team_data.get('away_yrfi', 0)
        total_games += team_data.get('home_games', 0) + team_data.get('away_games', 0)
    
    # Calcular el promedio de la MLB
    mlb_average = total_yrfi / total_games if total_games > 0 else 0.4  # 40% por defecto si no hay datos
    
    # 10. Inicializar detalles de la predicción
    prediction_details = {
        'home_team': {
            'id': home_team_id,
            'name': home_team_data.get('name', 'Equipo Local'),
            'yrfi_pct': home_team_yrfi * 100,
            'recent_yrfi_pct': home_team_yrfi_recent * 100 if has_recent_data else None,
            'games_analyzed': home_team_data.get('home_games', 0),
            'yrfi': home_team_data.get('home_yrfi', 0),
            'total_games': home_team_data.get('home_games', 0)
        },
        'away_team': {
            'id': away_team_id,
            'name': away_team_data.get('name', 'Equipo Visitante'),
            'yrfi_pct': away_team_yrfi * 100,
            'recent_yrfi_pct': away_team_yrfi_recent * 100 if has_recent_data else None,
            'games_analyzed': away_team_data.get('away_games', 0),
            'yrfi': away_team_data.get('away_yrfi', 0),
            'total_games': away_team_data.get('away_games', 0)
        },
        'home_pitcher': {
            'id': home_pitcher_id,
            'name': 'Desconocido',
            'yrfi_pct': (1 - home_pitcher_yrfi) * 100,  # Convertir de vuelta a % de YRFI
            'starts_analyzed': games_analyzed.get('home_pitcher', 0)
        } if home_pitcher_id else None,
        'away_pitcher': {
            'id': away_pitcher_id,
            'name': 'Desconocido',
            'yrfi_pct': (1 - away_pitcher_yrfi) * 100,  # Convertir de vuelta a % de YRFI
            'starts_analyzed': games_analyzed.get('away_pitcher', 0)
        } if away_pitcher_id else None,
        'mlb_average': {
            'yrfi_pct': mlb_average * 100,
            'total_yrfi': total_yrfi,
            'total_games': total_games
        },
        'season_prob': season_prob,
        'recent_prob': recent_prob if has_recent_data else None,
        'final_probability': final_prob,
        'has_recent_data': has_recent_data,
        'calculation_breakdown': {
            'home_team_contribution': home_team_yrfi * (0.10 if has_recent_data else 0.20),
            'away_team_contribution': away_team_yrfi * (0.10 if has_recent_data else 0.20),
            'home_team_recent_contribution': home_team_yrfi_recent * 0.10 if has_recent_data else 0.0,
            'away_team_recent_contribution': away_team_yrfi_recent * 0.10 if has_recent_data else 0.0,
            'home_pitcher_contribution': home_pitcher_yrfi * 0.15,
            'away_pitcher_contribution': away_pitcher_yrfi * 0.15,
            'mlb_average_contribution': mlb_average * 0.30
        }
    }
    
    return final_prob, prediction_details

def format_yrfi_report(prediction_details: Dict, game_date: str = None) -> str:
    """
    Formatea un informe detallado de la predicción YRFI.
    
    Args:
        prediction_details: Diccionario con los detalles de la predicción
        game_date: Fecha del juego (opcional)
        
    Returns:
        Cadena con el informe formateado
    """
    # Obtener información básica
    home_team = prediction_details['home_team']
    away_team = prediction_details['away_team']
    home_pitcher = prediction_details.get('home_pitcher')
    away_pitcher = prediction_details.get('away_pitcher')
    mlb_avg = prediction_details['mlb_average']
    
    # Obtener probabilidades
    season_prob = prediction_details['season_prob']
    recent_prob = prediction_details.get('recent_prob')
    
    # Calcular probabilidad final
    if recent_prob is not None and recent_prob > 0:
        final_prob = (season_prob * 0.7) + (recent_prob * 0.3)
    else:
        final_prob = season_prob
    
    # Formatear encabezado
    report = []
    if game_date:
        report.append(f"=== PREDICCIÓN YRFI - {game_date} ===\n")
    else:
        report.append("=== PREDICCIÓN YRFI ===\n")
    
    # Información de los equipos
    report.append(f"⚾ {away_team['name']} @ {home_team['name']} ⚾\n")
    
    # Información de lanzadores si está disponible
    if home_pitcher or away_pitcher:
        report.append("🔵 Lanzadores:")
        if away_pitcher:
            report.append(f"   {away_team['name']}: {away_pitcher.get('name', 'Por anunciar')}")
        if home_pitcher:
            report.append(f"   {home_team['name']}: {home_pitcher.get('name', 'Por anunciar')}")
        report.append("")
    
    # Estadísticas de equipos
    report.append("📊 ESTADÍSTICAS DE EQUIPOS")
    report.append("-" * 40)
    
    # Equipo visitante
    report.append(f"🔵 {away_team['name']} (Visitante):")
    report.append(f"   • YRFI en la temporada: {away_team['yrfi_pct']:.1f}% ({away_team['yrfi']}/{away_team['total_games']} juegos)")
    
    # Equipo local
    report.append(f"🔴 {home_team['name']} (Local):")
    report.append(f"   • YRFI en la temporada: {home_team['yrfi_pct']:.1f}% ({home_team['yrfi']}/{home_team['total_games']} juegos)")
    
    # Promedio de la MLB
    report.append(f"\n🏆 Promedio de la MLB: {mlb_avg['yrfi_pct']:.1f}% ({mlb_avg['total_yrfi']}/{mlb_avg['total_games']} juegos)")
    
    # Tendencias recientes si están disponibles
    if recent_prob is not None:
        report.append("\n📈 TENDENCIAS RECIENTES")
        report.append("-" * 40)
        
        # Juegos analizados
        games = prediction_details['games_analyzed']
        if games['home_team'] > 0 or games['away_team'] > 0:
            report.append(f"Últimos {games['home_team']} juegos de {home_team['name']} y {games['away_team']} de {away_team['name']} analizados")
        
        # Probabilidad de tendencia reciente
        report.append(f"Probabilidad basada en tendencias recientes: {recent_prob:.1f}%")
    
    # Desglose de la predicción
    breakdown = prediction_details['calculation_breakdown']
    report.append("\n🔍 DESGLOSE DE LA PREDICCIÓN")
    report.append("-" * 40)
    report.append(f"• Equipo local: {breakdown['home_team_contribution']*100:.1f}% (20% peso)")
    report.append(f"• Equipo visitante: {breakdown['away_team_contribution']*100:.1f}% (20% peso)")
    report.append(f"• Lanzador local: {breakdown['home_pitcher_contribution']*100:.1f}% (15% peso)")
    report.append(f"• Lanzador visitante: {breakdown['away_pitcher_contribution']*100:.1f}% (15% peso)")
    report.append(f"• Promedio MLB: {breakdown['mlb_average_contribution']*100:.1f}% (30% peso)")
    
    if breakdown['recent_trend_contribution'] is not None:
        report.append(f"• Tendencias recientes: {breakdown['recent_trend_contribution']*100:.1f}% (30% del total)")
    
    # Probabilidad final
    report.append("\n🎯 PROBABILIDAD FINAL YRFI")
    report.append("-" * 40)
    report.append(f"Probabilidad de carreras en el primer inning: {final_prob:.1f}%")
    
    # Recomendación basada en la probabilidad
    if final_prob >= 60:
        recommendation = "🔴 ALTA probabilidad de YRFI (Apoyar SÍ)"
    elif final_prob >= 40:
        recommendation = "🟡 Probabilidad media de YRFI (Cuidado o buscar mejores opciones)"
    else:
        recommendation = "🟢 BAJA probabilidad de YRFI (Apoyar NO o buscar alternativas)"
    
    report.append(f"\n💡 Recomendación: {recommendation}")
    
    # Pie de informe
    report.append("\n" + "=" * 50)
    report.append("Nota: Los porcentajes se basan en datos históricos y pueden variar.")
    report.append("Se recomienda combinar este análisis con información de última hora.")
    
    return "\n".join(report)

def format_prediction(
    home_team: str, 
    away_team: str, 
    probability: float, 
    home_team_data: Dict, 
    away_team_data: Dict,
    home_pitcher_data: Optional[Dict] = None,
    away_pitcher_data: Optional[Dict] = None,
    home_pitcher_stats_str: Optional[str] = None,
    away_pitcher_stats_str: Optional[str] = None,
    prob_details: Optional[Dict] = None
) -> str:
    """
    Formatea la predicción para mostrarla al usuario, mostrando estadísticas de temporada completa,
    tendencia reciente de los últimos 15 partidos y rendimiento de lanzadores.
    
    Args:
        home_team: Nombre del equipo local
        away_team: Nombre del equipo visitante
        probability: Probabilidad de YRFI (0-1)
        home_team_data: Datos del equipo local
        away_team_data: Datos del equipo visitante
        home_pitcher_data: Datos del lanzador local (opcional)
        away_pitcher_data: Datos del lanzador visitante (opcional)
        home_pitcher_stats_str: Estadísticas formateadas del lanzador local (opcional)
        away_pitcher_stats_str: Estadísticas formateadas del lanzador visitante (opcional)
        prob_details: Detalles adicionales de la predicción (opcional)
        
    Returns:
        str: Texto formateado con la predicción
    """
    # Encabezado con equipos y probabilidad total
    lines = [
        f"⚾ {away_team} @ {home_team}:",
        f"📊 Probabilidad YRFI: {probability*100:.1f}%"
    ]
    
    # Añadir detalles de la predicción si están disponibles
    if prob_details:
        # Obtener datos de los equipos
        home_team_yrfi = prob_details.get('home_team', {}).get('yrfi_pct', 0) / 100
        away_team_yrfi = prob_details.get('away_team', {}).get('yrfi_pct', 0) / 100
        home_team_recent = prob_details.get('home_team', {}).get('recent_yrfi_pct')
        home_team_recent = home_team_recent / 100 if home_team_recent is not None else None
        away_team_recent = prob_details.get('away_team', {}).get('recent_yrfi_pct')
        away_team_recent = away_team_recent / 100 if away_team_recent is not None else None
        
        # Obtener datos de lanzadores
        home_p_yrfi = prob_details.get('home_pitcher', {}).get('yrfi_pct')
        home_p_yrfi = (100 - home_p_yrfi) / 100 if home_p_yrfi is not None else 0.5  # Invertir para mostrar efectividad
        away_p_yrfi = prob_details.get('away_pitcher', {}).get('yrfi_pct')
        away_p_yrfi = (100 - away_p_yrfi) / 100 if away_p_yrfi is not None else 0.5  # Invertir para mostrar efectividad
        
        mlb_avg = prob_details.get('mlb_average', 0) / 100
        
        # Sección de equipos
        lines.append("\n🏟️ EQUIPOS")
        lines.append(f"  {home_team} (Local):")
        lines.append(f"    • Temporada completa: {home_team_yrfi:.1%} YRFI")
        if home_team_recent is not None:
            lines.append(f"    • Últimos 15 partidos: {home_team_recent:.1%} YRFI")
        
        lines.append(f"\n  {away_team} (Visitante):")
        lines.append(f"    • Temporada completa: {away_team_yrfi:.1%} YRFI")
        if away_team_recent is not None:
            lines.append(f"    • Últimos 15 partidos: {away_team_recent:.1%} YRFI")
        
        # Sección de lanzadores
        lines.append("\n🎯 LANZADORES")
        if home_pitcher_data:
            lines.append(f"  {home_team} (Local):")
            lines.append(f"    • {home_pitcher_data.get('name', 'Lanzador no disponible')}")
            lines.append(f"    • Efectividad: {home_p_yrfi:.1%} (1 - %YRFI permitido)")
            if home_pitcher_stats_str:
                lines.append(f"    • {home_pitcher_stats_str}")
        
        if away_pitcher_data:
            lines.append(f"\n  {away_team} (Visitante):")
            lines.append(f"    • {away_pitcher_data.get('name', 'Lanzador no disponible')}")
            lines.append(f"    • Efectividad: {away_p_yrfi:.1%} (1 - %YRFI permitido)")
            if away_pitcher_stats_str:
                lines.append(f"    • {away_pitcher_stats_str}")
        
        # Desglose del modelo
        lines.append("\n📈 DESGLOSE DEL MODELO")
        
        # Contribución de equipos (temporada completa y tendencia)
        if home_team_recent is not None and away_team_recent is not None:
            # Usar tendencia reciente y temporada completa
            lines.append(f"  • Equipo local (temporada): {home_team_yrfi:.1%} × 10% = {home_team_yrfi * 0.10:.1%}")
            lines.append(f"  • Equipo local (tendencia): {home_team_recent:.1%} × 10% = {home_team_recent * 0.10:.1%}")
            lines.append(f"  • Equipo visitante (temporada): {away_team_yrfi:.1%} × 10% = {away_team_yrfi * 0.10:.1%}")
            lines.append(f"  • Equipo visitante (tendencia): {away_team_recent:.1%} × 10% = {away_team_recent * 0.10:.1%}")
        else:
            # Usar solo temporada completa con mayor peso
            lines.append(f"  • Equipo local: {home_team_yrfi:.1%} × 20% = {home_team_yrfi * 0.20:.1%}")
            lines.append(f"  • Equipo visitante: {away_team_yrfi:.1%} × 20% = {away_team_yrfi * 0.20:.1%}")
        
        # Contribución de lanzadores
        lines.append(f"  • Lanzador local: {home_p_yrfi:.1%} × 15% = {home_p_yrfi * 0.15:.1%}")
        lines.append(f"  • Lanzador visitante: {away_p_yrfi:.1%} × 15% = {away_p_yrfi * 0.15:.1%}")
        
        # Contribución del promedio de la MLB
        lines.append(f"  • Promedio MLB: {mlb_avg:.1%} × 30% = {mlb_avg * 0.30:.1%}")
        
        # Línea de total
        lines.append(f"\n  Total: {probability*100:.1f}%")
    
    # Añadir recomendación basada en la probabilidad
    lines.append("\n💡 RECOMENDACIÓN")
    if probability >= 0.6:
        recommendation = "🔴 ALTA probabilidad de YRFI (Buena oportunidad de apuesta)"
    elif probability >= 0.5:
        recommendation = "🟡 Probabilidad media de YRFI (Cuidado o buscar mejores opciones)"
    else:
        recommendation = "🟢 BAJA probabilidad de YRFI (Apoyar NO o buscar alternativas)"
    
    lines.append(recommendation)
    
    # Añadir nota sobre los datos
    lines.append("\n📝 Nota: Los porcentajes se basan en datos históricos y pueden variar.")
    lines.append("Se recomienda combinar este análisis con información de última hora.")
    
    return "\n".join(lines)

def get_todays_games() -> List[Dict]:
    """
    Obtiene los partidos programados para hoy.
    
    Returns:
        Lista de diccionarios con información de los partidos, incluyendo game_id
    """
    client = MLBClient()
    today = datetime.now().strftime('%Y-%m-%d')
    schedule = client.get_schedule(date=today)
    
    games = []
    if 'dates' in schedule and schedule['dates'] and 'games' in schedule['dates'][0]:
        for game in schedule['dates'][0]['games']:
            # Asegurarse de que cada juego tenga un game_id
            if 'gamePk' in game and 'teams' in game and 'home' in game['teams'] and 'away' in game['teams']:
                # Asegurar que los equipos tengan la estructura correcta
                home_team = game['teams']['home'].get('team', {})
                away_team = game['teams']['away'].get('team', {})
                
                # Verificar que los equipos tengan ID y nombre
                if 'id' not in home_team or 'name' not in home_team or 'id' not in away_team or 'name' not in away_team:
                    print(f"Advertencia: Estructura de equipo inválida en el juego {game.get('gamePk')}")
                    continue
                
                game_info = {
                    'game_id': str(game['gamePk']),
                    'gamePk': game['gamePk'],
                    'teams': {
                        'home': {'team': home_team},
                        'away': {'team': away_team}
                    },
                    'gameDate': game.get('gameDate', today)
                }
                games.append(game_info)
    
    print(f"Se encontraron {len(games)} juegos con estructura válida para hoy.")
    return games

def generate_detailed_report(games, season_data):
    """
    Genera un informe detallado de YRFI para los partidos dados.
    
    Args:
        games: Lista de diccionarios con información de los partidos
        season_data: Datos de la temporada cargados
        
    Returns:
        Lista de informes formateados para cada partido
    """
    if not games:
        print("No hay partidos para generar informes.")
        return []
        
    if not season_data or 'teams' not in season_data:
        print("Error: Datos de temporada inválidos o faltantes.")
        return []
    
    # Inicializar analizador de tendencias
    trend_analyzer = TrendAnalyzer(season_data)
    
    game_reports = []
    processed_count = 0
    
    # Procesar cada partido
    for game in games:
        game_id = game.get('gamePk', 'desconocido')
        try:
            # Verificar estructura básica del juego
            if 'teams' not in game or 'home' not in game['teams'] or 'away' not in game['teams']:
                print(f"\n⚠ Advertencia: Estructura de juego inválida (ID: {game_id}). Omitiendo...")
                continue
                
            # Obtener información básica del partido con manejo de errores
            home_team = game['teams']['home'].get('team', {})
            away_team = game['teams']['away'].get('team', {})
            
            if not home_team or 'id' not in home_team or not away_team or 'id' not in away_team:
                print(f"\n⚠ Advertencia: Datos de equipos incompletos (ID: {game_id}). Omitiendo...")
                continue
            
            home_team_id = str(home_team['id'])
            away_team_id = str(away_team['id'])
            
            # Verificar que los equipos existan en los datos de temporada
            if home_team_id not in season_data['teams'] or away_team_id not in season_data['teams']:
                missing_teams = []
                if home_team_id not in season_data['teams']:
                    missing_teams.append(f"local ({home_team_id})")
                if away_team_id not in season_data['teams']:
                    missing_teams.append(f"visitante ({away_team_id})")
                print(f"\n⚠ Advertencia: No se encontraron datos para equipos: {', '.join(missing_teams)} (ID: {game_id}). Omitiendo...")
                continue
            
            # Obtener lanzadores probables si están disponibles
            home_pitcher = game.get('probable_pitcher', {}).get('home', {})
            away_pitcher = game.get('probable_pitcher', {}).get('away', {})
            
            home_pitcher_id = str(home_pitcher['id']) if home_pitcher and 'id' in home_pitcher else None
            away_pitcher_id = str(away_pitcher['id']) if away_pitcher and 'id' in away_pitcher else None
            
            home_pitcher_name = home_pitcher.get('name', 'Por definir') if home_pitcher else 'Por definir'
            away_pitcher_name = away_pitcher.get('name', 'Por definir') if away_pitcher else 'Por definir'
            
            print(f"\n📊 Procesando juego {game_id}: {away_team.get('name', 'Visitante')} @ {home_team.get('name', 'Local')}")
            if home_pitcher_id or away_pitcher_id:
                print(f"   Lanzadores: {away_pitcher_name} vs {home_pitcher_name}")
            
            # Calcular probabilidad de YRFI
            try:
                prob, prediction_details = predict_yrfi_probability(
                    home_team_id=home_team_id,
                    away_team_id=away_team_id,
                    home_pitcher_id=home_pitcher_id,
                    away_pitcher_id=away_pitcher_id,
                    season_data=season_data,
                    trend_analyzer=trend_analyzer
                )
                
                # Añadir nombres de equipos y lanzadores a los detalles
                prediction_details['home_team']['name'] = home_team.get('name', 'Equipo Local')
                prediction_details['away_team']['name'] = away_team.get('name', 'Equipo Visitante')
                
                if 'home_pitcher' in prediction_details and prediction_details['home_pitcher']:
                    prediction_details['home_pitcher']['name'] = home_pitcher_name
                if 'away_pitcher' in prediction_details and prediction_details['away_pitcher']:
                    prediction_details['away_pitcher']['name'] = away_pitcher_name
                
                # Generar el informe
                report = format_yrfi_report(prediction_details)
                game_reports.append(report)
                
                # Mostrar el informe en consola
                print("\n" + "=" * 80)
                print(report)
                processed_count += 1
                
            except Exception as pred_error:
                print(f"\n⚠ Error al calcular la probabilidad para el juego {game_id}: {str(pred_error)}")
                print("Continuando con el siguiente partido...")
                continue
            
        except Exception as e:
            import traceback
            print(f"\n❌ Error crítico al procesar el juego {game_id}:")
            print(traceback.format_exc())
            print("Continuando con el siguiente partido...")
            continue
    
    # Resumen del procesamiento
    print("\n" + "=" * 80)
    print(f"✅ Procesamiento completado. Se generaron {processed_count} de {len(games)} informes correctamente.")
    if processed_count < len(games):
        print(f"   - Se omitieron {len(games) - processed_count} partidos debido a errores o datos faltantes.")
    
    return game_reports

def get_probable_pitchers_for_games(games: List[Dict]) -> Dict[str, Dict]:
    """
    Obtiene los lanzadores probables para los juegos dados.
    
    Args:
        games: Lista de juegos con información básica
        
    Returns:
        Diccionario con los lanzadores probables por juego
    """
    from src.mlb_client import MLBClient
    
    client = MLBClient()
    pitchers = {}
    
    if not games:
        print("No se proporcionaron juegos para buscar lanzadores probables.")
        return pitchers
    
    print(f"Buscando lanzadores probables para {len(games)} juegos...")
    
    for game in games:
        game_id = game.get('game_id')
        if not game_id:
            print("Advertencia: Juego sin game_id, omitiendo...")
            continue
            
        try:
            # Obtener información detallada del juego para los lanzadores probables
            game_data = client.get_game(game_id)
            if not game_data:
                print(f"No se pudo obtener información del juego {game_id}")
                continue
                
            # Extraer lanzadores probables
            probable_pitchers = client.get_starting_pitchers(game_data)
            if probable_pitchers:
                home_pitcher = probable_pitchers.get('home', {})
                away_pitcher = probable_pitchers.get('away', {})
                
                # Asegurarse de que los lanzadores tengan la estructura correcta
                if home_pitcher and ('id' not in home_pitcher or 'fullName' not in home_pitcher):
                    print(f"Advertencia: Estructura inválida para lanzador local en juego {game_id}")
                    home_pitcher = {}
                    
                if away_pitcher and ('id' not in away_pitcher or 'fullName' not in away_pitcher):
                    print(f"Advertencia: Estructura inválida para lanzador visitante en juego {game_id}")
                    away_pitcher = {}
                
                pitchers[game_id] = {
                    'home_pitcher': home_pitcher if home_pitcher else None,
                    'away_pitcher': away_pitcher if away_pitcher else None
                }
                
                # Mostrar información de los lanzadores encontrados
                home_name = home_pitcher.get('fullName', 'Por definir') if home_pitcher else 'Por definir'
                away_name = away_pitcher.get('fullName', 'Por definir') if away_pitcher else 'Por definir'
                print(f"Juego {game_id}: {away_name} @ {home_name}")
            else:
                print(f"No se encontraron lanzadores probables para el juego {game_id}")
                
        except Exception as e:
            print(f"Error al obtener lanzadores probables para el juego {game_id}: {str(e)}")
    
    print(f"Se encontraron lanzadores para {len(pitchers)} de {len(games)} juegos.")
    return pitchers

def main(args=None) -> List[Dict[str, Any]]:
    """
    Función principal que genera predicciones o informes de YRFI.
    
    Args:
        args: Argumentos de línea de comandos. Si es None, se usarán los argumentos de sys.argv
    """
    # Lista para almacenar las salidas a guardar
    output_to_save = []
    
    print("=== Generando predicciones YRFI ===")
    
    # Actualizar datos si se solicita
    if args and hasattr(args, 'update') and args.update:
        print("Actualizando datos...")
        try:
            # Importar aquí para evitar dependencia circular
            from scripts.update_daily_data import main as update_data
            update_data()
            print("Datos actualizados exitosamente.")
        except Exception as e:
            print(f"Error al actualizar datos: {e}")
            print("Continuando con los datos existentes...")
    
    # Obtener partidos del día
    games = get_todays_games()
    
    if not games:
        print("No hay partidos programados para hoy.")
        return []
    
    # Cargar datos de la temporada primero
    print("Cargando datos de la temporada...")
    season_data = load_season_data()
    
    if not season_data or 'games' not in season_data:
        print("No se pudieron cargar los datos de la temporada.")
        return []
        
    print(f"Datos cargados hasta: {season_data.get('last_updated', 'fecha desconocida')}")
    
    # Obtener partidos de hoy
    print(f"Encontrados {len(games)} partidos programados para hoy.")
    
    # Obtener lanzadores probables para los partidos de hoy
    print("\nObteniendo lanzadores probables...")
    probable_pitchers = get_probable_pitchers_for_games(games)
    
    # Si no hay lanzadores probables, continuar con predicciones sin ellos
    if not probable_pitchers:
        print("\n⚠ Advertencia: No se pudieron obtener lanzadores probables. Se generarán predicciones sin esta información.")
    
    # Inicializar analizador de tendencias
    trend_analyzer = TrendAnalyzer(season_data) if season_data else None
    
    # Generar predicciones
    predictions = []
    for game in games:
        game_id = game.get('game_id', 'desconocido')
        try:
            # Verificar estructura básica del juego
            if 'teams' not in game or 'home' not in game['teams'] or 'away' not in game['teams']:
                print(f"\n⚠ Advertencia: Estructura de juego inválida (ID: {game_id}). Omitiendo...")
                continue
                
            # Obtener información de equipos con manejo de errores
            try:
                home_team = game['teams']['home'].get('team', {})
                away_team = game['teams']['away'].get('team', {})
                
                if not home_team or 'id' not in home_team or not away_team or 'id' not in away_team:
                    print(f"\n⚠ Advertencia: Datos de equipos incompletos (ID: {game_id}). Omitiendo...")
                    continue
                
                home_team_id = str(home_team['id'])
                away_team_id = str(away_team['id'])
                home_team_name = home_team.get('name', 'Equipo Local')
                away_team_name = away_team.get('name', 'Equipo Visitante')
                
                # Verificar que los equipos existan en los datos de temporada
                if home_team_id not in season_data.get('teams', {}) or away_team_id not in season_data.get('teams', {}):
                    missing_teams = []
                    if home_team_id not in season_data.get('teams', {}):
                        missing_teams.append(f"local ({home_team_id})")
                    if away_team_id not in season_data.get('teams', {}):
                        missing_teams.append(f"visitante ({away_team_id})")
                    print(f"\n⚠ Advertencia: No se encontraron datos para equipos: {', '.join(missing_teams)} (ID: {game_id}). Omitiendo...")
                    continue
                
            except Exception as team_error:
                print(f"\n❌ Error al obtener información de equipos (ID: {game_id}): {str(team_error)}")
                continue
            
            # Obtener lanzadores probables para este juego
            game_pitchers = probable_pitchers.get(game_id, {})
            home_pitcher = game_pitchers.get('home_pitcher', {}) if game_pitchers else {}
            away_pitcher = game_pitchers.get('away_pitcher', {}) if game_pitchers else {}
            
            home_pitcher_id = str(home_pitcher['id']) if home_pitcher and 'id' in home_pitcher else None
            away_pitcher_id = str(away_pitcher['id']) if away_pitcher and 'id' in away_pitcher else None
            home_pitcher_name = home_pitcher.get('name', home_pitcher.get('fullName', 'Por definir')) if home_pitcher else 'Por definir'
            away_pitcher_name = away_pitcher.get('name', away_pitcher.get('fullName', 'Por definir')) if away_pitcher else 'Por definir'
            
            print(f"\n📊 Procesando juego {game_id}: {away_team_name} @ {home_team_name}")
            if home_pitcher_id or away_pitcher_id:
                print(f"   Lanzadores: {away_pitcher_name} vs {home_pitcher_name}")
            
            # Crear objetos de lanzadores para el data manager
            home_pitcher_obj = {'id': home_pitcher_id, 'name': home_pitcher_name} if home_pitcher_id else None
            away_pitcher_obj = {'id': away_pitcher_id, 'name': away_pitcher_name} if away_pitcher_id else None
            
            # Obtener estadísticas históricas de YRFI para los lanzadores
            game_data_for_stats = {
                'home_team': home_team_id,
                'away_team': away_team_id,
                'home_pitcher': home_pitcher_obj,
                'away_pitcher': away_pitcher_obj
            }
            
            try:
                from src.data.data_manager import get_game_pitchers_yrfi_stats
                pitcher_stats = get_game_pitchers_yrfi_stats(game_data_for_stats, season_data.get('games', []))
                
                # Obtener estadísticas de rendimiento de los lanzadores
                home_pitcher_stats = pitcher_stats.get('home_pitcher', {}).get('stats', {}) if home_pitcher_id else {}
                away_pitcher_stats = pitcher_stats.get('away_pitcher', {}).get('stats', {}) if away_pitcher_id else {}
                
                # Formatear estadísticas para mostrar
                def format_pitcher_stats(stats):
                    if not stats or stats.get('total_starts', 0) == 0:
                        return "Sin datos suficientes"
                        
                    total_yrfi = stats.get('total_yrfi', 0)
                    total_starts = stats.get('total_starts', 1)
                    yrfi_pct = (total_yrfi / total_starts) * 100
                    
                    return f"{total_yrfi} YRFI en {total_starts} aperturas ({yrfi_pct:.1f}%)"
                
                home_pitcher_stats_str = format_pitcher_stats(home_pitcher_stats)
                away_pitcher_stats_str = format_pitcher_stats(away_pitcher_stats)
                
            except Exception as stats_error:
                print(f"⚠ Error al obtener estadísticas de lanzadores: {str(stats_error)}")
                home_pitcher_stats_str = "Error al cargar estadísticas"
                away_pitcher_stats_str = "Error al cargar estadísticas"
                home_pitcher_stats = {}
                away_pitcher_stats = {}
            
            try:
                # Predecir probabilidad de YRFI con análisis de tendencias
                probability, prob_details = predict_yrfi_probability(
                    home_team_id=home_team_id,
                    away_team_id=away_team_id,
                    home_pitcher_id=home_pitcher_id,
                    away_pitcher_id=away_pitcher_id,
                    season_data=season_data,
                    trend_analyzer=trend_analyzer
                )
                
                # Obtener datos para mostrar en el resumen
                home_team_data = season_data['teams'].get(home_team_id, {})
                away_team_data = season_data['teams'].get(away_team_id, {})
                home_pitcher_data = season_data.get('pitchers', {}).get(home_pitcher_id) if home_pitcher_id else None
                away_pitcher_data = season_data.get('pitchers', {}).get(away_pitcher_id) if away_pitcher_id else None
                
                # Preparar datos para guardar
                prediction_data = {
                    'game_date': datetime.now().strftime('%Y-%m-%d'),
                    'home_team': home_team_name,
                    'away_team': away_team_name,
                    'yrfi_probability': probability,
                    'probability_details': {
                        'base_probability': prob_details.get('base_prob', 0) if isinstance(prob_details, dict) else 0,
                        'trend_adjustment': prob_details.get('trend_adjustment', 0) if isinstance(prob_details, dict) else 0,
                        'final_probability': prob_details.get('final_prob', 0) if isinstance(prob_details, dict) else 0
                    },
                    'home_team_stats': {
                        'games': home_team_data.get('home_games', 0) if isinstance(home_team_data, dict) else 0,
                        'yrfi_games': home_team_data.get('home_yrfi', 0) if isinstance(home_team_data, dict) else 0,
                        'yrfi_percentage': (home_team_data.get('home_yrfi', 0) / home_team_data.get('home_games', 1) * 100) 
                                          if isinstance(home_team_data, dict) and home_team_data.get('home_games', 0) > 0 else 0,
                    },
                    'away_team_stats': {
                        'games': away_team_data.get('away_games', 0) if isinstance(away_team_data, dict) else 0,
                        'yrfi_games': away_team_data.get('away_yrfi', 0) if isinstance(away_team_data, dict) else 0,
                        'yrfi_percentage': (away_team_data.get('away_yrfi', 0) / away_team_data.get('away_games', 1) * 100) 
                                          if isinstance(away_team_data, dict) and away_team_data.get('away_games', 0) > 0 else 0,
                    },
                    'home_pitcher': {
                        'id': home_pitcher_id,
                        'name': home_pitcher_name,
                        'stats': home_pitcher_stats_str,
                        'yrfi_percentage': home_pitcher_stats.get('yrfi_percentage', 0) if home_pitcher_stats else None,
                        'starts_analyzed': home_pitcher_stats.get('total_starts', 0) if home_pitcher_stats else 0
                    } if home_pitcher_id else None,
                    'away_pitcher': {
                        'id': away_pitcher_id,
                        'name': away_pitcher_name,
                        'stats': away_pitcher_stats_str,
                        'yrfi_percentage': away_pitcher_stats.get('yrfi_percentage', 0) if away_pitcher_stats else None,
                        'starts_analyzed': away_pitcher_stats.get('total_starts', 0) if away_pitcher_stats else 0
                    } if away_pitcher_id else None,
                    'game_time': game.get('gameDate', '')
                }
                
                # Formatear predicción para mostrar
                prediction_text = format_prediction(
                    home_team=home_team_name,
                    away_team=away_team_name,
                    probability=probability,
                    home_team_data=home_team_data,
                    away_team_data=away_team_data,
                    home_pitcher_data=home_pitcher_data,
                    away_pitcher_data=away_pitcher_data,
                    home_pitcher_stats_str=home_pitcher_stats_str,
                    away_pitcher_stats_str=away_pitcher_stats_str,
                    prob_details=prob_details if isinstance(prob_details, dict) else {}
                )
                
                # Mostrar predicción
                print("\n" + "=" * 80)
                print(prediction_text)
                
                # Agregar a la lista de predicciones
                predictions.append(prediction_data)
                output_to_save.append(prediction_text)
                
            except Exception as pred_error:
                print(f"\n❌ Error al predecir probabilidad para el juego {game_id}:")
                print(f"   Error: {str(pred_error)}")
                import traceback
                print("\nDetalles técnicos:")
                print(traceback.format_exc())
                continue
                
        except Exception as e:
            print(f"\n❌ Error inesperado al procesar el juego {game_id}:")
            print(f"   Error: {str(e)}")
            import traceback
            print("\nDetalles técnicos:")
            print(traceback.format_exc())
            continue
    
    if not predictions:
        print("No se pudieron generar predicciones para ningún partido.")
        return []
    
    # Ordenar predicciones por probabilidad (de mayor a menor)
    predictions.sort(reverse=True, key=lambda x: x[0])
    
    # Generar salida
    today = datetime.now().strftime('%Y-%m-%d')
    output = [f"Predicciones de carreras en el primer inning (YRFI) para {today}\n"]
    
    for prob, pred, home_team, away_team, prob_details in predictions:
        output.append(pred)
        output.append("-" * 60)
    
    # Calcular probabilidad promedio
    avg_prob = sum(p[0] for p in predictions) / len(predictions)
    output.append(f"\nProbabilidad promedio YRFI: {avg_prob*100:.1f}%")
    
    # Mostrar mejores apuestas
    if len(predictions) >= 3:
        output.append("\n🔝 Mejores apuestas YRFI:")
        for prob, pred, home_team, away_team, prob_details in predictions[:3]:
            base_prob = prob_details.get('base_prob', prob) * 100
            trend_adj = prob_details.get('trend_adjustment', 0) * 100
            output.append(
                f"- {away_team} @ {home_team}: {prob*100:.1f}% "
                f"(Base: {base_prob:.1f}%, Tendencia: {trend_adj:+.1f}%)"
            )
        
        output.append("\n⬇️ Peores apuestas YRFI:")
        for prob, pred, home_team, away_team, prob_details in predictions[-3:]:
            base_prob = prob_details.get('base_prob', prob) * 100
            trend_adj = prob_details.get('trend_adjustment', 0) * 100
            output.append(
                f"- {away_team} @ {home_team}: {prob*100:.1f}% "
                f"(Base: {base_prob:.1f}%, Tendencia: {trend_adj:+.1f}%)"
            )
    
    # Unir todo el output
    output_text = "\n".join(output)
    
    # Mostrar en consola
    print("\n" + "="*70)
    print(output_text)
    
    # Guardar en archivo de texto si se especificó
    if args.output and not args.report:  # Solo guardar texto si no es un informe
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"\nResumen de predicciones guardado en {args.output}")
        except Exception as e:
            print(f"\nError al guardar el archivo de texto: {e}")
    
    # Generar informe detallado si se solicitó
    if args.report:
        output_to_save = generate_detailed_report(games, season_data)
    
    # Guardar salida si se especificó un archivo de salida
    if (args.output or args.update) and (args.report or predictions):
        try:
            data_to_save = output_to_save if args.report else predictions
            output_path = save_predictions_to_file(
                data_to_save,
                args.output,
                report_format=args.report
            )
            print(f"\n{'Informe' if args.report else 'Predicciones'} guardado en: {output_path}")
        except Exception as e:
            print(f"\nError al guardar la salida: {e}")
    
    # Devolver los datos generados
    if args.report:
        return output_to_save
    else:
        return predictions

def save_predictions_to_file(predictions: List[Dict[str, Any]], output_file: str = None, report_format: bool = False) -> str:
    """
    Guarda las predicciones en un archivo.
    
    Args:
        predictions: Lista de predicciones o informes
        output_file: Ruta del archivo de salida. Si es None, se genera un nombre automático.
        report_format: Si es True, guarda en formato de texto plano. Si es False, guarda como JSON.
    
    Returns:
        str: Ruta del archivo generado
    """
    if not output_file:
        # Crear directorio de salida si no existe
        output_dir = Path('reports' if report_format else 'predictions')
        output_dir.mkdir(exist_ok=True)
        
        # Generar nombre de archivo con la fecha actual
        today = datetime.now().strftime('%Y-%m-%d')
        ext = 'txt' if report_format else 'json'
        output_file = output_dir / f'yrfi_{today}.{ext}'
    else:
        output_file = Path(output_file)
    
    # Asegurarse de que el directorio padre existe
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar las predicciones en el formato correspondiente
    with open(output_file, 'w', encoding='utf-8') as f:
        if report_format:
            f.write(f"Reporte YRFI - {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("=" * 50 + "\n\n")
            f.write("\n\n".join(predictions))
        else:
            json.dump(predictions, f, indent=2, ensure_ascii=False)
    
    return str(output_file)

if __name__ == "__main__":
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Genera predicciones YRFI para partidos de MLB.')
    parser.add_argument('--output', '-o', type=str, help='Ruta del archivo de salida (opcional)')
    parser.add_argument('--update', action='store_true', help='Actualizar datos antes de generar predicciones')
    parser.add_argument('--report', '-r', action='store_true', help='Generar un informe detallado YRFI')
    args = parser.parse_args()
    
    # Ejecutar main con los argumentos
    predictions = main(args)
    
    # Si no se generó el informe, guardar las predicciones
    if not args.report and predictions:
        output_file = save_predictions_to_file(predictions, args.output, report_format=False)
        print(f"\n✅ Predicciones guardadas en: {output_file}")
    elif not predictions:
        print("\n⚠ No se generaron predicciones para guardar.")
