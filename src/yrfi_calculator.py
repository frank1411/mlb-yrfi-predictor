"""
Módulo para calcular estadísticas de YRFI (carreras en el primer inning).
"""
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json

class YRFICalculator:
    """Clase para calcular estadísticas de YRFI (carreras en el primer inning)."""
    
    def __init__(self, season_data: Dict, window_size: int = 15):
        """
        Inicializa el calculador con los datos de la temporada.
        
        Args:
            season_data: Datos de la temporada
            window_size: Tamaño de la ventana para estadísticas recientes (en partidos)
        """
        self.season_data = season_data
        self.window_size = window_size
    
    def get_team_name(self, team_id: str) -> str:
        """Obtiene el nombre de un equipo por su ID."""
        team = self.season_data.get('teams', {}).get(team_id, {})
        return team.get('team', {}).get('name', f'Equipo {team_id}')
    
    def calculate_season_stats(self, team_id: str, is_home: bool) -> Dict:
        """
        Calcula las estadísticas de temporada completa para un equipo.
        
        Args:
            team_id: ID del equipo
            is_home: Si es local (True) o visitante (False)
            
        Returns:
            Dict con estadísticas de temporada completa
        """
        team_data = self.season_data.get('teams', {}).get(team_id, {})
        
        if not team_data:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_1st': 0.0,
                'games_analyzed': 0
            }
        
        # Obtener estadísticas de local/visitante
        if is_home:
            total_games = team_data.get('home_games', 0)
            yrfi_games = team_data.get('home_yrfi', 0)
            total_runs = team_data.get('home_runs_1st', 0)
        else:
            total_games = team_data.get('away_games', 0)
            yrfi_games = team_data.get('away_yrfi', 0)
            total_runs = team_data.get('away_runs_1st', 0)
        
        # Calcular porcentajes
        yrfi_pct = yrfi_games / total_games if total_games > 0 else 0.0
        avg_runs = total_runs / total_games if total_games > 0 else 0.0
        
        return {
            'yrfi_pct': yrfi_pct,
            'avg_runs_1st': avg_runs,
            'games_analyzed': total_games
        }
    
    def calculate_recent_stats(self, team_id: str, is_home: Optional[bool] = None) -> Dict:
        """
        Calcula las estadísticas recientes para un equipo.
        
        Args:
            team_id: ID del equipo
            is_home: Si es local (True), visitante (False) o no importa (None)
            
        Returns:
            Dict con estadísticas recientes
        """
        team_games = []
        
        # Buscar partidos del equipo
        for game in self.season_data.get('games', []):
            # Obtener IDs de equipos del partido
            home_team_id = str(game.get('home_team', ''))
            away_team_id = str(game.get('away_team', ''))
            
            # Verificar si el equipo participó en este partido
            is_home_game = team_id == home_team_id
            is_away_game = team_id == away_team_id
            
            if not (is_home_game or is_away_game):
                continue
                
            # Filtrar por local/visitante si se especificó
            if is_home is not None and ((is_home and not is_home_game) or (not is_home and not is_away_game)):
                continue
                
            # Obtener información del partido
            try:
                game_date = datetime.strptime(game['date'], '%Y-%m-%d')
            except (ValueError, KeyError):
                # Si hay un error con la fecha, saltar este partido
                continue
            
            # Obtener estadísticas del primer inning directamente del juego
            team_yrfi = game['home_yrfi'] if is_home_game else game['away_yrfi']
            opp_yrfi = game['away_yrfi'] if is_home_game else game['home_yrfi']
            
            # Para compatibilidad con el código existente, establecer team_runs y opp_runs
            team_runs = 1 if team_yrfi else 0
            opp_runs = 1 if opp_yrfi else 0
            yrfi = team_yrfi  # Solo cuenta si el equipo en cuestión anotó
            
            # Obtener nombre del oponente
            opponent_id = away_team_id if is_home_game else home_team_id
            opponent_name = self.season_data.get('teams', {}).get(opponent_id, {}).get('name', 'Desconocido')
            
            # Agregar a la lista de partidos
            team_games.append({
                'date': game_date,
                'game_id': game.get('game_id', ''),
                'is_home': is_home_game,
                'opponent_id': opponent_id,
                'opponent_name': opponent_name,
                'team_runs_1st': team_runs,
                'opponent_runs_1st': opp_runs,
                'yrfi': yrfi
            })
        
        # Ordenar partidos por fecha (más reciente primero)
        team_games.sort(key=lambda x: x['date'], reverse=True)
        
        # Tomar solo los últimos N partidos según window_size
        recent_games = team_games[:self.window_size]
        total_games = len(recent_games)
        
        if total_games == 0:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_1st': 0.0,
                'games_analyzed': 0,
                'recent_games': []
            }
        
        # Calcular estadísticas
        yrfi_count = sum(1 for g in recent_games if g['yrfi'])
        yrfi_pct = yrfi_count / total_games
        avg_runs = sum(g['team_runs_1st'] for g in recent_games) / total_games
        
        return {
            'yrfi_pct': yrfi_pct,
            'avg_runs_1st': avg_runs,
            'games_analyzed': total_games,
            'recent_games': recent_games
        }
    
    def calculate_pitcher_stats(self, pitcher_id: str) -> Dict:
        """
        Calcula las estadísticas de un lanzador.
        
        Args:
            pitcher_id: ID del lanzador
            
        Returns:
            Dict con estadísticas del lanzador
        """
        pitcher_data = self.season_data.get('pitchers', {}).get(str(pitcher_id))
        
        if not pitcher_data or pitcher_data.get('starts', 0) == 0:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_allowed_1st': 0.0,
                'starts_analyzed': 0
            }
        
        yrfi_pct = pitcher_data.get('yrfi_starts', 0) / pitcher_data.get('starts', 1)
        avg_runs = pitcher_data.get('runs_allowed_1st', 0) / pitcher_data.get('starts', 1)
        
        return {
            'yrfi_pct': yrfi_pct,
            'avg_runs_allowed_1st': avg_runs,
            'starts_analyzed': pitcher_data.get('starts', 0),
            'name': pitcher_data.get('fullName', f'Lanzador {pitcher_id}')
        }
    
    def predict_yrfi_probability(
        self,
        home_team_id: str,
        away_team_id: str,
        home_pitcher_id: Optional[str] = None,
        away_pitcher_id: Optional[str] = None,
        season_weight: float = 0.6,
        recent_weight: float = 0.4
    ) -> Tuple[float, Dict]:
        """
        Predice la probabilidad de que haya carreras en el primer inning.
        
        Combina estadísticas de temporada completa con tendencias recientes,
        aplicando una ponderación personalizable.
        
        Args:
            home_team_id: ID del equipo local
            away_team_id: ID del equipo visitante
            home_pitcher_id: ID del lanzador local (opcional)
            away_pitcher_id: ID del lanzador visitante (opcional)
            season_weight: Peso para estadísticas de temporada completa (0-1)
            recent_weight: Peso para estadísticas recientes (0-1)
            
        Returns:
            Tuple[float, Dict]: Probabilidad (0-1) y detalles de la predicción
        """
        # Validar pesos
        if not (0 <= season_weight <= 1 and 0 <= recent_weight <= 1):
            raise ValueError("Los pesos deben estar entre 0 y 1")
            
        if season_weight + recent_weight == 0:
            raise ValueError("Al menos uno de los pesos debe ser mayor que 0")
        
        # 1. Calcular estadísticas de temporada completa
        home_team_season = self.calculate_season_stats(home_team_id, is_home=True)
        away_team_season = self.calculate_season_stats(away_team_id, is_home=False)
        
        # 2. Calcular estadísticas recientes
        home_team_recent = self.calculate_recent_stats(home_team_id, is_home=True)
        away_team_recent = self.calculate_recent_stats(away_team_id, is_home=False)
        
        # 3. Obtener estadísticas de lanzadores si están disponibles
        home_pitcher_stats = None
        away_pitcher_stats = None
        
        if home_pitcher_id:
            home_pitcher_stats = self.calculate_pitcher_stats(home_pitcher_id)
        if away_pitcher_id:
            away_pitcher_stats = self.calculate_pitcher_stats(away_pitcher_id)
        
        # 4. Calcular probabilidades
        # Temporada completa
        season_prob = (
            (home_team_season['yrfi_pct'] * 0.4) +  # 40% del total
            (away_team_season['yrfi_pct'] * 0.4)    # 40% del total
        )
        
        # Ajustar por lanzadores (si hay datos)
        if home_pitcher_stats and home_pitcher_stats['starts_analyzed'] > 0:
            # Invertir el porcentaje (un buen lanzador reduce el YRFI)
            season_prob *= (1 - home_pitcher_stats['yrfi_pct'] * 0.2)  # Hasta 20% de ajuste
            
        if away_pitcher_stats and away_pitcher_stats['starts_analyzed'] > 0:
            # Invertir el porcentaje (un buen lanzador reduce el YRFI)
            season_prob *= (1 - away_pitcher_stats['yrfi_pct'] * 0.2)  # Hasta 20% de ajuste
        
        # Tendencias recientes (solo equipos por ahora)
        home_yrfi_recent = home_team_recent['yrfi_pct'] if home_team_recent['games_analyzed'] >= 5 else None
        away_yrfi_recent = away_team_recent['yrfi_pct'] if away_team_recent['games_analyzed'] >= 5 else None
        
        # Si no hay suficientes datos recientes, usar temporada completa
        if home_yrfi_recent is None:
            home_yrfi_recent = home_team_season['yrfi_pct']
        if away_yrfi_recent is None:
            away_yrfi_recent = away_team_season['yrfi_pct']
        
        recent_prob = (home_yrfi_recent + away_yrfi_recent) / 2
        
        # 5. Combinar probabilidades con ponderación
        total_weight = season_weight + recent_weight
        weighted_prob = ((season_prob * season_weight) + (recent_prob * recent_weight)) / total_weight
        
        # Asegurar que la probabilidad esté en un rango razonable
        final_prob = max(0.20, min(0.80, weighted_prob))
        
        # Preparar detalles para el informe
        details = {
            'home_team': {
                'id': home_team_id,
                'name': self.get_team_name(home_team_id),
                'season': home_team_season,
                'recent': home_team_recent
            },
            'away_team': {
                'id': away_team_id,
                'name': self.get_team_name(away_team_id),
                'season': away_team_season,
                'recent': away_team_recent
            },
            'home_pitcher': home_pitcher_stats,
            'away_pitcher': away_pitcher_stats,
            'probabilities': {
                'season': season_prob,
                'recent': recent_prob,
                'season_weight': season_weight,
                'recent_weight': recent_weight,
                'weighted': weighted_prob,
                'final': final_prob
            }
        }
        
        return final_prob, details
