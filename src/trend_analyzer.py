"""
Módulo para analizar tendencias recientes de equipos y lanzadores.
"""
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import math
from src.data.data_manager import get_first_inning_yrfi

class TrendAnalyzer:
    def __init__(self, season_data: Dict, window_size: int = 10):
        """
        Inicializa el analizador de tendencias.
        
        Args:
            season_data: Datos completos de la temporada
            window_size: Tamaño de la ventana de juegos para analizar tendencias
        """
        self.season_data = season_data
        self.window_size = window_size
    
    def get_team_games(self, team_id: str, reference_date: str = None, 
                      is_home: bool = None, limit: int = None) -> List[Dict]:
        """
        Obtiene los juegos de un equipo, opcionalmente filtrados por fecha y condición de local/visitante.
        
        Args:
            team_id: ID del equipo
            reference_date: Fecha de referencia en formato 'YYYY-MM-DD' (solo juegos antes de esta fecha)
            is_home: Si es True, solo partidos como local; si es False, solo como visitante; None para todos
            limit: Número máximo de juegos a devolver (los más recientes)
            
        Returns:
            Lista de juegos ordenados del más reciente al más antiguo
        """
        team_games = []
        
        # Convertir la fecha de referencia si se proporciona
        ref_date = None
        if reference_date:
            try:
                ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
            except (ValueError, TypeError):
                ref_date = None
        
        for game in self.season_data.get('games', []):
            # Obtener fecha del juego
            game_date_str = game.get('gameDate')
            if not game_date_str:
                continue
                
            try:
                game_date = datetime.strptime(game_date_str, '%Y-%m-%dT%H:%M:%SZ')
                if ref_date and game_date >= ref_date:
                    continue
            except (ValueError, TypeError):
                continue
            
            # Verificar si el partido ya terminó
            if game.get('status', {}).get('statusCode') != 'F':
                continue
            
            # Obtener información de equipos
            home_team = game.get('teams', {}).get('home', {})
            away_team = game.get('teams', {}).get('away', {})
            
            home_team_id = str(home_team.get('team', {}).get('id', ''))
            away_team_id = str(away_team.get('team', {}).get('id', ''))
            
            # Verificar si el equipo participó en este partido
            if team_id not in (home_team_id, away_team_id):
                continue
                
            # Verificar condición de local/visitante
            is_home_game = team_id == home_team_id
            if is_home is not None and is_home_game != is_home:
                continue
            
            # Obtener carreras del primer inning
            yrfi_data = get_first_inning_yrfi(game)
            home_yrfi = yrfi_data['home_yrfi']
            away_yrfi = yrfi_data['away_yrfi']
            
            # Determinar si el equipo anotó o recibió carreras en el primer inning
            team_yrfi = home_yrfi if is_home_game else away_yrfi
            opp_yrfi = away_yrfi if is_home_game else home_yrfi
            yrfi = team_yrfi or opp_yrfi
            
            # Agregar información del partido
            team_games.append({
                'date': game_date,
                'game_id': game.get('gamePk'),
                'is_home': is_home_game,
                'opponent_id': away_team_id if is_home_game else home_team_id,
                'opponent_name': away_team.get('team', {}).get('name') if is_home_game else home_team.get('team', {}).get('name'),
                'team_runs_1st': team_runs,
                'opponent_runs_1st': opp_runs,
                'yrfi': yrfi
            })
            
            # Crear estructura de juego estándar
            game_data = {
                'game_date': game_date_str,
                'home_team': home_team.get('team', {}).get('name', ''),
                'away_team': away_team.get('team', {}).get('name', ''),
                'home_score': home_team.get('score', 0),
                'away_score': away_team.get('score', 0),
                'linescore': {
                    'home': {'runs': home_team.get('score', 0)},
                    'away': {'runs': away_team.get('score', 0)}
                },
                'probablePitchers': game.get('probablePitchers', {})
            }
            
            # Filtrar por equipo y condición de local/visitante
            if home_team_id == team_id:  # Equipo es local
                if is_home is not None and not is_home:
                    continue
                game_data.update({
                    'is_home': True,
                    'opponent_id': away_team_id,
                    'team_score': game_data['home_score'],
                    'opponent_score': game_data['away_score']
                })
                team_games.append(game_data)
                
            elif away_team_id == team_id:  # Equipo es visitante
                if is_home is not None and is_home:
                    continue
                game_data.update({
                    'is_home': False,
                    'opponent_id': home_team_id,
                    'team_score': game_data['away_score'],
                    'opponent_score': game_data['home_score']
                })
                team_games.append(game_data)
        
        # Ordenar por fecha (más reciente primero)
        team_games.sort(key=lambda x: x['date'], reverse=True)
        
        # Aplicar límite si se especificó
        if limit is not None:
            team_games = team_games[:limit]
        
        return team_games
    
    def analyze_team_yrfi_trends(self, team_id: str, reference_date: str = None, 
                               is_home: bool = None, window_size: int = None) -> Dict[str, Any]:
        """
        Analiza las tendencias recientes de YRFI de un equipo.
        
        Args:
            team_id: ID del equipo
            reference_date: Fecha de referencia en formato 'YYYY-MM-DD' (opcional)
            is_home: Si es True, solo partidos como local; si es False, solo como visitante; None para todos
            window_size: Tamaño de la ventana de juegos a analizar (opcional, por defecto usa el valor de la clase)
            
        Returns:
            Diccionario con estadísticas de tendencia YRFI
        """
        # Usar el tamaño de ventana especificado o el predeterminado
        window = window_size or self.window_size
        
        # Obtener juegos recientes
        recent_games = self.get_team_games(
            team_id=team_id,
            reference_date=reference_date,
            is_home=is_home,
            limit=window
        )
        
        if not recent_games:
            return {
                'total_games': 0,
                'yrfi_count': 0,
                'yrfi_pct': 0.0,
                'team_avg_runs_1st': 0.0,
                'opp_avg_runs_1st': 0.0,
                'trend': 'neutral',
                'last_5_games': []
            }
        
        # Calcular estadísticas
        total_games = len(recent_games)
        yrfi_games = sum(1 for g in recent_games if g.get('yrfi', False))
        yrfi_pct = (yrfi_games / total_games) * 100 if total_games > 0 else 0
        
        team_avg_runs = sum(g.get('team_runs_1st', 0) for g in recent_games) / total_games if total_games > 0 else 0
        opp_avg_runs = sum(g.get('opponent_runs_1st', 0) for g in recent_games) / total_games if total_games > 0 else 0
        
        # Determinar tendencia
        if yrfi_pct >= 70:
            trend = 'strong_yrfi'
        elif yrfi_pct >= 55:
            trend = 'yrfi'
        elif yrfi_pct <= 30:
            trend = 'strong_nyrfi'
        elif yrfi_pct <= 45:
            trend = 'nyrfi'
        else:
            trend = 'neutral'
        
        # Obtener últimos 5 partidos para referencia
        last_5_games = [
            {
                'date': g['date'].strftime('%Y-%m-%d'),
                'opponent': g['opponent_name'],
                'is_home': g['is_home'],
                'team_runs_1st': g['team_runs_1st'],
                'opponent_runs_1st': g['opponent_runs_1st'],
                'yrfi': g['yrfi']
            }
            for g in recent_games[:5]
        ]
        
        return {
            'total_games': total_games,
            'yrfi_count': yrfi_games,
            'yrfi_pct': round(yrfi_pct, 1),
            'team_avg_runs_1st': round(team_avg_runs, 2),
            'opp_avg_runs_1st': round(opp_avg_runs, 2),
            'trend': trend,
            'last_5_games': last_5_games
        }
    
    def calculate_team_trend(self, team_id: str, reference_date: str, is_home: bool = None) -> Dict:
        """
        Calcula la tendencia reciente de un equipo.
        
        Returns:
            Dict con métricas de tendencia:
            - yrfi_pct: Porcentaje de YRFI en los últimos juegos
            - avg_runs_1st: Promedio de carreras en el primer inning
            - trend: Tendencia (1.0 = muy positiva, 0.5 = neutral, 0.0 = muy negativa)
        """
        recent_games = self.get_team_games(team_id, reference_date, is_home)
        if not recent_games:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_1st': 0.0,
                'trend': 0.5  # Neutral si no hay datos
            }
        
        yrfi_count = 0
        total_runs = 0
        
        for game in recent_games:
            if game['is_home']:
                runs = game.get('linescore', {}).get('home', {}).get('runs', 0)
            else:
                runs = game.get('linescore', {}).get('away', {}).get('runs', 0)
            
            if runs > 0:
                yrfi_count += 1
            total_runs += runs
        
        yrfi_pct = yrfi_count / len(recent_games)
        avg_runs = total_runs / len(recent_games)
        
        # Calcular tendencia (valor entre 0 y 1)
        # 0.5 es neutral (promedio de la liga)
        # >0.5 es mejor que el promedio
        # <0.5 es peor que el promedio
        trend = 0.5 + (yrfi_pct - 0.45) * 2  # Ajustar según el promedio de la liga
        trend = max(0.0, min(1.0, trend))  # Asegurar entre 0 y 1
        
        return {
            'yrfi_pct': yrfi_pct,
            'avg_runs_1st': avg_runs,
            'trend': trend,
            'games_analyzed': len(recent_games)
        }
    
    def get_pitcher_stats(self, pitcher_id: str, reference_date: str) -> Dict:
        """
        Obtiene estadísticas recientes de un lanzador.
        
        Args:
            pitcher_id: ID del lanzador
            reference_date: Fecha de referencia en formato 'YYYY-MM-DD'
            
        Returns:
            Diccionario con estadísticas del lanzador, incluyendo YRFI
        """
        pitcher_games = []
        
        # Convertir la fecha de referencia
        try:
            ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            ref_date = None
        
        # Buscar partidos donde el lanzador haya participado
        for game in self.season_data.get('games', []):
            # Obtener fecha del juego
            game_date_str = game.get('gameDate')
            if not game_date_str:
                continue
                
            try:
                game_date = datetime.strptime(game_date_str, '%Y-%m-%dT%H:%M:%SZ')
                if ref_date and game_date >= ref_date:
                    continue
            except (ValueError, TypeError):
                continue
            
            # Verificar si el partido ya terminó
            if game.get('status', {}).get('statusCode') != 'F':
                continue
            
            # Buscar si el lanzador abrió el juego
            pitchers = game.get('probablePitchers', {})
            home_pitcher = pitchers.get('home', {}).get('id') if pitchers else None
            away_pitcher = pitchers.get('away', {}).get('id') if pitchers else None
            
            if str(pitcher_id) not in (str(home_pitcher), str(away_pitcher)):
                continue
            
            # Determinar si es abridor y si es local/visitante
            is_home = str(pitcher_id) == str(home_pitcher)
            
            # Obtener carreras del primer inning
            yrfi_data = get_first_inning_yrfi(game)
            home_yrfi = yrfi_data['home_yrfi']
            away_yrfi = yrfi_data['away_yrfi']
            
            # Determinar si el lanzador permitió carreras en el primer inning
            yrfi = home_yrfi if is_home else away_yrfi
            
            # Agregar información del partido
            pitcher_games.append({
                'date': game_date,
                'game_id': game.get('gamePk'),
                'is_home': is_home,
                'opponent_id': game['teams']['away' if is_home else 'home']['team'].get('id'),
                'opponent_name': game['teams']['away' if is_home else 'home']['team'].get('name'),
                'runs_allowed_1st': 1 if yrfi else 0,  # 1 si permitió carreras, 0 si no
                'yrfi': yrfi
            })
        
        # Ordenar por fecha (más reciente primero)
        pitcher_games.sort(key=lambda x: x['date'], reverse=True)
        
        # Calcular estadísticas
        total_games = len(pitcher_games)
        if total_games == 0:
            return {
                'total_games': 0,
                'yrfi_count': 0,
                'yrfi_pct': 0.0,
                'avg_runs_allowed_1st': 0.0,
                'trend': 'neutral',
                'last_5_games': []
            }
        
        # Estadísticas generales
        yrfi_count = sum(1 for g in pitcher_games if g['yrfi'])
        yrfi_pct = (yrfi_count / total_games) * 100
        avg_runs = sum(g['runs_allowed_1st'] for g in pitcher_games) / total_games
        
        # Determinar tendencia
        if yrfi_pct >= 70:
            trend = 'strong_yrfi'
        elif yrfi_pct >= 55:
            trend = 'yrfi'
        elif yrfi_pct <= 30:
            trend = 'strong_nyrfi'
        elif yrfi_pct <= 45:
            trend = 'nyrfi'
        else:
            trend = 'neutral'
        
        # Últimos 5 partidos
        last_5 = [
            {
                'date': g['date'].strftime('%Y-%m-%d'),
                'opponent': g['opponent_name'],
                'is_home': g['is_home'],
                'runs_allowed_1st': g['runs_allowed_1st'],
                'yrfi': g['yrfi']
            }
            for g in pitcher_games[:5]
        ]
        
        return {
            'total_games': total_games,
            'yrfi_count': yrfi_count,
            'yrfi_pct': round(yrfi_pct, 1),
            'avg_runs_allowed_1st': round(avg_runs, 2),
            'trend': trend,
            'last_5_games': last_5
        }
    
    def calculate_pitcher_trend(self, pitcher_id: str, reference_date: str) -> Dict:
        """
        Calcula la tendencia reciente de un lanzador.
        
        Returns:
            Dict con métricas de tendencia para el lanzador
        """
        if not pitcher_id:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_allowed_1st': 0.0,
                'trend': 0.5,
                'starts_analyzed': 0
            }
        
        recent_starts = []
        ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
        
        # Obtener los últimos juegos donde el lanzador fue abridor
        for game in self.season_data.get('games', []):
            if len(recent_starts) >= self.window_size:
                break
                
            # Filtrar por fecha
            game_date_str = game.get('officialDate')
            if not game_date_str:
                continue
                
            try:
                game_date = datetime.strptime(game_date_str, '%Y-%m-%d')
                if game_date >= ref_date:
                    continue
            except (ValueError, TypeError):
                continue
            
            # Verificar si el lanzador es el abridor
            home_pitcher = game.get('probablePitchers', {}).get('home', {})
            away_pitcher = game.get('probablePitchers', {}).get('away', {})
            
            if str(pitcher_id) in (str(home_pitcher.get('id')), str(away_pitcher.get('id'))):
                # Determinar si es local o visitante
                is_home = str(pitcher_id) == str(home_pitcher.get('id'))
                
                # Obtener puntuación del primer inning (simplificado como puntuación total)
                home_score = game.get('teams', {}).get('home', {}).get('score', 0)
                away_score = game.get('teams', {}).get('away', {}).get('score', 0)
                
                # Crear entrada de juego para el lanzador
                start_data = {
                    'game_date': game_date_str,
                    'is_home': is_home,
                    'runs_allowed': away_score if is_home else home_score,
                    'yrfi_allowed': 1 if (away_score > 0 and is_home) or (home_score > 0 and not is_home) else 0
                }
                recent_starts.append(start_data)
        
        if not recent_starts:
            return {
                'yrfi_pct': 0.0,
                'avg_runs_allowed_1st': 0.0,
                'trend': 0.5,
                'starts_analyzed': 0
            }
        
        # Calcular métricas
        yrfi_count = sum(1 for game in recent_starts if game.get('yrfi_allowed', 0) > 0)
        starts_analyzed = len(recent_starts)
        yrfi_pct = yrfi_count / starts_analyzed if starts_analyzed > 0 else 0.0
        avg_runs_allowed = sum(game.get('runs_allowed', 0) for game in recent_starts) / starts_analyzed if starts_analyzed > 0 else 0.0
        
        # Normalizar a un valor entre 0 y 1
        trend = (yrfi_pct + (avg_runs_allowed / 3)) / 2  # Promedio de ambas métricas
        
        return {
            'yrfi_pct': yrfi_pct,
            'avg_runs_allowed_1st': avg_runs_allowed,
            'trend': min(max(trend, 0.0), 1.0),  # Asegurar que esté entre 0 y 1
            'starts_analyzed': starts_analyzed
        }
    
    def get_game_trend_analysis(self, home_team_id: str, away_team_id: str, 
                             home_pitcher_id: str = None, away_pitcher_id: str = None,
                             game_date: str = None) -> Dict:
        """
        Realiza un análisis completo de tendencias para un partido.
        
        Args:
            home_team_id: ID del equipo local
            away_team_id: ID del equipo visitante
            home_pitcher_id: ID del lanzador local (opcional)
            away_pitcher_id: ID del lanzador visitante (opcional)
            game_date: Fecha del partido en formato 'YYYY-MM-DD' (opcional)
            
        Returns:
            Dict con el análisis de tendencias para el partido
        """
        if game_date is None:
            game_date = datetime.now().strftime('%Y-%m-%d')
        
        home_team_trend = self.calculate_team_trend(home_team_id, game_date, is_home=True)
        away_team_trend = self.calculate_team_trend(away_team_id, game_date, is_home=False)
        
        home_pitcher_trend = self.calculate_pitcher_trend(home_pitcher_id, game_date) if home_pitcher_id else None
        away_pitcher_trend = self.calculate_pitcher_trend(away_pitcher_id, game_date) if away_pitcher_id else None
        
        # Calcular tendencia general del partido (valor entre 0 y 1)
        # Ponderaciones:
        # - 30% tendencia del equipo local
        # - 30% tendencia del equipo visitante
        # - 20% tendencia del lanzador local (si está disponible)
        # - 20% tendencia del lanzador visitante (si está disponible)
        
        total_weight = 0.6  # Peso base (30% + 30%)
        game_trend = (
            home_team_trend['trend'] * 0.3 +
            away_team_trend['trend'] * 0.3
        )
        
        if home_pitcher_trend:
            game_trend += home_pitcher_trend['trend'] * 0.2
            total_weight += 0.2
            
        if away_pitcher_trend:
            game_trend += away_pitcher_trend['trend'] * 0.2
            total_weight += 0.2
        
        # Normalizar al rango [0, 1]
        game_trend = game_trend / total_weight if total_weight > 0 else 0.5
        
        return {
            'home_team': home_team_trend,
            'away_team': away_team_trend,
            'home_pitcher': home_pitcher_trend,
            'away_pitcher': away_pitcher_trend,
            'game_trend': game_trend,
            'game_date': game_date
        }
