"""
Módulo para analizar estadísticas de carreras en el primer inning (YRFI - Yes Run First Inning).
"""
from typing import Dict, List, Tuple, Any, Optional, Set
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import os
from .mlb_client import MLBClient
from .yrfi_visualizer import YRFIVisualizer

class AlertSystem:
    """Sistema de alertas para YRFI."""
    
    def __init__(self, config_path: str = 'alerts_config.json'):
        """Inicializa el sistema de alertas con configuración."""
        self.config_path = config_path
        self.config = self._load_config()
        self.alerts = []
    
    def _load_config(self) -> Dict:
        """Carga la configuración de alertas desde un archivo JSON."""
        default_config = {
            'min_games': 5,  # Mínimo de juegos para considerar tendencias
            'yrfi_threshold': 0.5,  # Umbral para alertas de YRFI alto
            'streak_length': 3,  # Longitud mínima de racha
            'teams_to_watch': [],  # Equipos para monitorear específicamente
            'pitchers_to_watch': []  # Lanzadores para monitorear específicamente
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return {**default_config, **json.load(f)}
        except Exception as e:
            print(f"Error cargando configuración de alertas: {e}")
        
        return default_config
    
    def check_team_streaks(self, team_stats: Dict) -> List[Dict]:
        """Verifica rachas interesantes de equipos."""
        alerts = []
        min_games = self.config['min_games']
        
        for team_id, stats in team_stats.items():
            if stats['total_games'] < min_games:
                continue
                
            # Verificar si el equipo está en la lista de monitoreo o cumple umbrales
            team_name = stats.get('name', f'Equipo {team_id}')
            if (team_id in self.config['teams_to_watch'] or 
                not self.config['teams_to_watch']):
                
                # Alerta para equipos con alto YRFI a favor
                yrfi_for_pct = stats.get('yrfi_for', 0) / max(1, stats['total_games'])
                if yrfi_for_pct >= self.config['yrfi_threshold']:
                    alerts.append({
                        'type': 'high_yrfi_team',
                        'team_id': team_id,
                        'team_name': team_name,
                        'value': yrfi_for_pct,
                        'games': stats['total_games'],
                        'message': f"{team_name} tiene un YRFI a favor del {yrfi_for_pct:.1%} en los últimos {stats['total_games']} juegos"
                    })
                
                # Alerta para equipos con bajo YRFI en contra (buenos lanzadores)
                yrfi_against_pct = stats.get('yrfi_against', 0) / max(1, stats['total_games'])
                if yrfi_against_pct <= (1 - self.config['yrfi_threshold']):
                    alerts.append({
                        'type': 'low_yrfi_against_team',
                        'team_id': team_id,
                        'team_name': team_name,
                        'value': yrfi_against_pct,
                        'games': stats['total_games'],
                        'message': f"{team_name} tiene solo un {yrfi_against_pct:.1%} de YRFI en contra en los últimos {stats['total_games']} juegos"
                    })
        
        return alerts
    
    def check_pitcher_trends(self, pitcher_stats: Dict) -> List[Dict]:
        """Verifica tendencias interesantes de lanzadores."""
        alerts = []
        min_starts = self.config.get('min_games', 3)  # Menos aperturas para lanzadores
        
        for pid, stats in pitcher_stats.items():
            if stats['total_starts'] < min_starts:
                continue
                
            pitcher_name = stats.get('name', f'Lanzador {pid}')
            team_name = stats.get('team_name', 'Desconocido')
            
            # Verificar si el lanzador está en la lista de monitoreo o cumple umbrales
            if (pid in self.config['pitchers_to_watch'] or 
                not self.config['pitchers_to_watch']):
                
                yrfi_pct = stats.get('yrfi_allowed', 0) / max(1, stats['total_starts'])
                
                # Alerta para lanzadores con alto YRFI permitido
                if yrfi_pct >= self.config['yrfi_threshold']:
                    alerts.append({
                        'type': 'high_yrfi_pitcher',
                        'pitcher_id': pid,
                        'pitcher_name': pitcher_name,
                        'team_name': team_name,
                        'value': yrfi_pct,
                        'starts': stats['total_starts'],
                        'message': f"{pitcher_name} ({team_name}) ha permitido YRFI en {yrfi_pct:.1%} de sus últimas {stats['total_starts']} aperturas"
                    })
                
                # Alerta para lanzadores con bajo YRFI permitido
                elif yrfi_pct <= 0.2:  # 20% o menos es considerado bueno
                    alerts.append({
                        'type': 'low_yrfi_pitcher',
                        'pitcher_id': pid,
                        'pitcher_name': pitcher_name,
                        'team_name': team_name,
                        'value': yrfi_pct,
                        'starts': stats['total_starts'],
                        'message': f"{pitcher_name} ({team_name}) ha sido efectivo, permitiendo YRFI solo en {yrfi_pct:.1%} de sus últimas {stats['total_starts']} aperturas"
                    })
        
        return alerts
    
    def generate_alerts(self, team_stats: Dict, pitcher_stats: Dict) -> List[Dict]:
        """Genera todas las alertas basadas en las estadísticas."""
        self.alerts = []
        
        # Verificar alertas de equipos
        self.alerts.extend(self.check_team_streaks(team_stats))
        
        # Verificar alertas de lanzadores
        self.alerts.extend(self.check_pitcher_trends(pitcher_stats))
        
        # Ordenar alertas por importancia
        self.alerts.sort(key=lambda x: abs(x.get('value', 0) - 0.5), reverse=True)
        
        return self.alerts
    
    def save_alerts_report(self, output_file: str = 'alerts_report.txt') -> str:
        """Guarda un informe con todas las alertas generadas."""
        if not self.alerts:
            return ""
            
        report = ["=" * 50]
        report.append("ALERTAS DE YRFI")
        report.append("=" * 50)
        report.append(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de alertas: {len(self.alerts)}")
        report.append("-" * 50 + "\n")
        
        # Agrupar alertas por tipo
        alerts_by_type = {}
        for alert in self.alerts:
            alert_type = alert.get('type', 'other')
            if alert_type not in alerts_by_type:
                alerts_by_type[alert_type] = []
            alerts_by_type[alert_type].append(alert)
        
        # Secciones por tipo de alerta
        type_titles = {
            'high_yrfi_team': "EQUIPOS CON ALTO YRFI A FAVOR",
            'low_yrfi_against_team': "EQUIPOS CON BAJO YRFI EN CONTRA",
            'high_yrfi_pitcher': "LANZADORES CON ALTO YRFI PERMITIDO",
            'low_yrfi_pitcher': "LANZADORES EFICACES (BAJO YRFI)"
        }
        
        for alert_type, alerts in alerts_by_type.items():
            report.append(f"\n{type_titles.get(alert_type, 'OTRAS ALERTAS').upper()}")
            report.append("-" * 50)
            
            for alert in alerts:
                report.append(f"• {alert['message']}")
        
        # Guardar en archivo
        report_text = "\n".join(report)
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
            
        return output_file

class YRFIAnalyzer:
    """Analizador de estadísticas de carreras en el primer inning."""
    
    def __init__(self, client: Optional[MLBClient] = None, cache_dir: str = '.cache'):
        """Inicializa el analizador con un cliente de MLB.
        
        Args:
            client: Cliente de MLB a utilizar. Si es None, se crea uno nuevo.
            cache_dir: Directorio para almacenar datos en caché.
        """
        self.client = client or MLBClient()
        self.team_cache: Dict[int, Dict] = {}
        self.player_cache: Dict[int, Dict] = {}
        self.pitcher_game_logs: Dict[int, List[Dict]] = {}
        self.cache_dir = cache_dir
        self.visualizer = YRFIVisualizer(output_dir=os.path.join(cache_dir, 'reports'))
        self.alert_system = AlertSystem()
        
        # Crear directorio de caché si no existe
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(os.path.join(self.cache_dir, 'reports'), exist_ok=True)
    
    def get_team_info(self, team_id: int) -> Dict:
        """Obtiene información de un equipo, usando caché para evitar peticiones repetidas.
        
        Args:
            team_id: ID del equipo en la API de MLB
            
        Returns:
            Dict con información del equipo o un diccionario vacío si hay error
        """
        if team_id not in self.team_cache:
            try:
                team_data = self.client.get_team(team_id)
                self.team_cache[team_id] = team_data['teams'][0] if team_data.get('teams') else {}
            except Exception as e:
                print(f"Error obteniendo información del equipo {team_id}: {e}")
                self.team_cache[team_id] = {'id': team_id, 'name': f'Equipo {team_id}'}
        return self.team_cache[team_id]
    
    def get_player_info(self, player_id: int) -> Dict:
        """Obtiene información de un jugador, usando caché para evitar peticiones repetidas.
        
        Args:
            player_id: ID del jugador en la API de MLB
            
        Returns:
            Dict con información del jugador o un diccionario con valores por defecto si hay error
        """
        if player_id not in self.player_cache:
            try:
                player_data = self.client.get_player(player_id)
                if not player_data:
                    player_data = {'id': player_id, 'fullName': f'Jugador {player_id}'}
                self.player_cache[player_id] = player_data
            except Exception as e:
                print(f"Error obteniendo información del jugador {player_id}: {e}")
                self.player_cache[player_id] = {'id': player_id, 'fullName': f'Jugador {player_id}'}
        return self.player_cache[player_id]
    
    def get_games_for_dates(self, start_date: str, end_date: str, use_cache: bool = True) -> List[Dict]:
        """Obtiene todos los juegos entre dos fechas, con soporte para caché.
        
        Args:
            start_date: Fecha de inicio en formato 'YYYY-MM-DD'
            end_date: Fecha de fin en formato 'YYYY-MM-DD'
            use_cache: Si es True, intenta cargar desde caché primero
            
        Returns:
            Lista de diccionarios con información de los juegos
        """
        cache_file = os.path.join(self.cache_dir, f'games_{start_date}_{end_date}.json')
        
        # Intentar cargar desde caché si está habilitado
        if use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    games = json.load(f)
                    print(f"Cargados {len(games)} juegos desde caché ({start_date} a {end_date})")
                    return games
            except Exception as e:
                print(f"Error al cargar juegos desde caché: {e}")
        
        try:
            # Usar el endpoint de schedule con rango de fechas
            params = {
                'sportId': 1,  # MLB
                'startDate': start_date,
                'endDate': end_date,
                'hydrate': 'probablePitcher,linescore,team,venue,game.venue,teams,team.league,team.division,team.sport',
                'fields': 'dates,games,gamePk,gameDate,teams,away,home,team,id,name,score,isWinner,probablePitcher,id,fullName,currentTeam,id,name,gameType,season,seriesDescription,status,detailedState,abstractGameState,venue,id,name,locationName,leagueRecord,wins,losses,pct,league,id,name,division,id,name,sport,id,name',
            }
            
            # Hacer la petición a la API
            schedule = self.client._make_request('schedule', params=params)
            
            # Extraer todos los juegos de las fechas
            all_games = []
            if schedule.get('dates'):
                for date_data in schedule['dates']:
                    games = date_data.get('games', [])
                    for game in games:
                        if 'gamePk' in game:
                            # Asegurarse de que el juego tenga la estructura esperada
                            if 'teams' not in game:
                                game['teams'] = {'home': {}, 'away': {}}
                            all_games.append(game)
            
            # Guardar en caché
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(all_games, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error al guardar en caché: {e}")
            
            print(f"Se encontraron {len(all_games)} juegos entre {start_date} y {end_date}")
            return all_games
            
        except Exception as e:
            print(f"Error al obtener juegos: {e}")
            return []
    
    def analyze_yrfi(self, games: List[Dict]) -> Dict:
        """
        Analiza los juegos para determinar cuáles tuvieron carreras en el primer inning.
        
        Args:
            games: Lista de diccionarios con información de los juegos
            
        Returns:
            Dict con estadísticas YRFI, incluyendo análisis por equipo, lanzador y tendencias
        """
        results = {
            'total_games': len(games),
            'yrfi_games': 0,
            'yrfi_by_team': {},
            'yrfi_by_pitcher': {},
            'yrfi_home_vs_away': {'home': 0, 'away': 0, 'total_home': 0, 'total_away': 0},
            'games': [],
            'date_range': {'start': None, 'end': None},
            'runs_data': {
                'home_avg': 0.0,
                'away_avg': 0.0,
                'total_avg': 0.0,
                'home_runs': 0,
                'away_runs': 0,
                'total_runs': 0,
                'games_with_data': 0
            },
            'trends': {
                'by_day': {},
                'by_team': {},
                'by_pitcher': {}
            }
        }
        
        # Variables para seguimiento de tendencias
        dates_seen = set()
        team_games = {}
        pitcher_games = {}
        
        for game in games:
            try:
                game_data = self._analyze_single_game(game)
                if game_data:
                    results['games'].append(game_data)

                    # Actualizar rango de fechas
                    game_date = game_data.get('date')
                    if game_date:
                        game_date = pd.to_datetime(game_date).date()
                        dates_seen.add(game_date)

                        if not results['date_range']['start'] or game_date < results['date_range']['start']:
                            results['date_range']['start'] = game_date
                        if not results['date_range']['end'] or game_date > results['date_range']['end']:
                            results['date_range']['end'] = game_date

                    # Actualizar estadísticas de carreras
                    home_runs = game_data.get('home_runs_1st', 0) or 0
                    away_runs = game_data.get('away_runs_1st', 0) or 0

                    if home_runs is not None and away_runs is not None:
                        results['runs_data']['home_runs'] += home_runs
                        results['runs_data']['away_runs'] += away_runs
                        results['runs_data']['total_runs'] += (home_runs + away_runs)
                        results['runs_data']['games_with_data'] += 1

                        # Actualizar promedios
                        if results['runs_data']['games_with_data'] > 0:
                            games_count = results['runs_data']['games_with_data']
                            results['runs_data']['home_avg'] = results['runs_data']['home_runs'] / games_count
                            results['runs_data']['away_avg'] = results['runs_data']['away_runs'] / games_count
                            results['runs_data']['total_avg'] = results['runs_data']['total_runs'] / games_count

                    # Actualizar estadísticas generales
                    if game_data['yrfi']:
                        results['yrfi_games'] += 1

                        # Estadísticas por equipo
                        for team_type in ['home', 'away']:
                            team_id = game_data[f'{team_type}_team_id']
                            team_name = game_data[f'{team_type}_team_name']

                            # Inicializar datos del equipo si no existen
                            if team_id not in results['yrfi_by_team']:
                                results['yrfi_by_team'][team_id] = {
                                    'name': team_name,
                                    'yrfi_for': 0,        # Veces que anotó en 1er inning
                                    'yrfi_against': 0,     # Veces que le anotaron en 1er inning
                                    'total_games': 0,
                                    'runs_scored_1st': 0,  # Carreras anotadas en 1er inning
                                    'runs_allowed_1st': 0, # Carreras permitidas en 1er inning
                                    'games_as_home': 0,
                                    'games_as_away': 0,
                                    'yrfi_home': 0,
                                    'yrfi_away': 0,
                                    'streak': {
                                        'current': 0,
                                        'max': 0,
                                        'type': None  # 'for' o 'against'
                                    },
                                    'last_yrfi': None
                                }

                            # Actualizar estadísticas de carreras
                            if team_type == 'home':
                                runs_scored = game_data.get('home_runs_1st', 0) or 0
                                runs_allowed = game_data.get('away_runs_1st', 0) or 0
                                results['yrfi_by_team'][team_id]['games_as_home'] += 1
                                if runs_scored > 0:
                                    results['yrfi_by_team'][team_id]['yrfi_home'] += 1
                            else:  # away
                                runs_scored = game_data.get('away_runs_1st', 0) or 0
                                runs_allowed = game_data.get('home_runs_1st', 0) or 0
                                results['yrfi_by_team'][team_id]['games_as_away'] += 1
                                if runs_scored > 0:
                                    results['yrfi_by_team'][team_id]['yrfi_away'] += 1

                            # Actualizar conteos de YRFI
                            if runs_scored > 0:
                                results['yrfi_by_team'][team_id]['yrfi_for'] += 1

                                # Actualizar racha a favor
                                if results['yrfi_by_team'][team_id]['streak']['type'] != 'for':
                                    results['yrfi_by_team'][team_id]['streak']['current'] = 0
                                results['yrfi_by_team'][team_id]['streak']['current'] += 1
                                results['yrfi_by_team'][team_id]['streak']['type'] = 'for'

                                # Actualizar máxima racha
                                if results['yrfi_by_team'][team_id]['streak']['current'] > results['yrfi_by_team'][team_id]['streak']['max']:
                                    results['yrfi_by_team'][team_id]['streak']['max'] = results['yrfi_by_team'][team_id]['streak']['current']

                                results['yrfi_by_team'][team_id]['last_yrfi'] = 'for'

                            if runs_allowed > 0:
                                results['yrfi_by_team'][team_id]['yrfi_against'] += 1

                                # Actualizar racha en contra
                                if results['yrfi_by_team'][team_id]['streak']['type'] != 'against':
                                    results['yrfi_by_team'][team_id]['streak']['current'] = 0
                                results['yrfi_by_team'][team_id]['streak']['current'] += 1
                                results['yrfi_by_team'][team_id]['streak']['type'] = 'against'

                                # Actualizar máxima racha
                                if results['yrfi_by_team'][team_id]['streak']['current'] > results['yrfi_by_team'][team_id]['streak']['max']:
                                    results['yrfi_by_team'][team_id]['streak']['max'] = results['yrfi_by_team'][team_id]['streak']['current']

                                results['yrfi_by_team'][team_id]['last_yrfi'] = 'against'

                            # Actualizar totales de carreras
                            results['yrfi_by_team'][team_id]['runs_scored_1st'] += runs_scored
                            results['yrfi_by_team'][team_id]['runs_allowed_1st'] += runs_allowed
                            results['yrfi_by_team'][team_id]['total_games'] += 1

                        # Estadísticas home vs away
                        if game_data['home_runs_1st'] > 0:
                            results['yrfi_home_vs_away']['home'] += 1
                        if game_data['away_runs_1st'] > 0:
                            results['yrfi_home_vs_away']['away'] += 1

                    # Actualizar totales home/away para el porcentaje
                    results['yrfi_home_vs_away']['total_home'] += 1
                    results['yrfi_home_vs_away']['total_away'] += 1

                    # Estadísticas por pitcher
                    for pitcher_type in ['home', 'away']:
                        pitcher_id = game_data.get(f'{pitcher_type}_starter_id')
                        if not pitcher_id:
                            continue

                        # Obtener ID del equipo contrario
                        opp_team_type = 'away' if pitcher_type == 'home' else 'home'
                        opp_team_id = game_data[f'{opp_team_type}_team_id']
                        opp_team_name = game_data[f'{opp_team_type}_team_name']

                        if pitcher_id not in results['yrfi_by_pitcher']:
                            pitcher_info = self.get_player_info(pitcher_id)
                            results['yrfi_by_pitcher'][pitcher_id] = {
                                'name': pitcher_info.get('fullName', 'Desconocido'),
                                'yrfi_allowed': 0,
                                'total_starts': 0,
                                'team_id': game_data[f'{pitcher_type}_team_id'],
                                'team_name': game_data[f'{pitcher_type}_team_name'],
                                'opponents': {},
                                'runs_allowed_1st': 0,
                                'strikeouts_1st': 0,  # Podría obtenerse de datos más detallados
                                'pitches_1st': 0,     # Podría obtenerse de datos más detallados
                                'last_5_starts': []
                            }

                        # Incrementar estadísticas del pitcher
                        runs_allowed = game_data[f'away_runs_1st'] if pitcher_type == 'home' else game_data[f'home_runs_1st']
                        if runs_allowed > 0:
                            results['yrfi_by_pitcher'][pitcher_id]['yrfi_allowed'] += 1

                        results['yrfi_by_pitcher'][pitcher_id]['total_starts'] += 1
                        results['yrfi_by_pitcher'][pitcher_id]['runs_allowed_1st'] += runs_allowed

                        # Mantener registro de los últimos 5 juegos
                        last_5 = results['yrfi_by_pitcher'][pitcher_id]['last_5_starts']
                        last_5.append({
                            'date': game_date,
                            'opponent_id': opp_team_id,
                            'opponent_name': opp_team_name,
                            'runs_allowed': runs_allowed,
                            'yrfi_allowed': runs_allowed > 0,
                            'is_home': pitcher_type == 'home'
                        })

                        # Mantener solo los últimos 5 juegos
                        if len(last_5) > 5:
                            last_5.pop(0)

                        # Actualizar estadísticas contra equipos oponentes
                        if opp_team_id not in results['yrfi_by_pitcher'][pitcher_id]['opponents']:
                            results['yrfi_by_pitcher'][pitcher_id]['opponents'][opp_team_id] = {
                                'name': opp_team_name,
                                'games': 0,
                                'yrfi_allowed': 0,
                                'runs_allowed': 0
                            }

                        results['yrfi_by_pitcher'][pitcher_id]['opponents'][opp_team_id]['games'] += 1
                        results['yrfi_by_pitcher'][pitcher_id]['opponents'][opp_team_id]['runs_allowed'] += runs_allowed
                        if runs_allowed > 0:
                            results['yrfi_by_pitcher'][pitcher_id]['opponents'][opp_team_id]['yrfi_allowed'] += 1

            except Exception as e:
                print(f"Error analizando juego {game.get('gamePk')}: {e}")

        return results

    def _analyze_single_game(self, game: Dict) -> Optional[Dict]:
        """Analiza un solo juego para determinar si hubo carreras en el primer inning."""
        try:
            game_pk = game['gamePk']
            game_date = game['gameDate']
            
            # Obtener información de los equipos
            home_team = game['teams']['home']['team']
            away_team = game['teams']['away']['team']
            
            # Obtener lanzadores abridores si están disponibles
            home_starter = next((p for p in game.get('probablePitchers', []) 
                               if p.get('team', {}).get('id') == home_team['id']), {})
            away_starter = next((p for p in game.get('probablePitchers', []) 
                               if p.get('team', {}).get('id') == away_team['id']), {})
            
            # Obtener el boxscore para ver las carreras por inning
            # Usar el endpoint de líneas de anotación (linescore) que es más confiable
            linescore = self.client._make_request(f"game/{game_pk}/linescore")
            
            # Inicializar contadores de carreras
            home_runs_1st = 0
            away_runs_1st = 0
            
            # Procesar las entradas (innings)
            innings = linescore.get('innings', [])
            if innings and len(innings) > 0:
                first_inning = innings[0]
                home_runs_1st = first_inning.get('home', {}).get('runs', 0) or 0
                away_runs_1st = first_inning.get('away', {}).get('runs', 0) or 0
            
            # Determinar si hubo carreras en el primer inning
            yrfi = home_runs_1st > 0 or away_runs_1st > 0
            
            # Obtener el marcador final
            home_score = linescore.get('teams', {}).get('home', {}).get('runs', 0) or 0
            away_score = linescore.get('teams', {}).get('away', {}).get('runs', 0) or 0
            
            return {
                'game_id': game_pk,
                'date': game_date,
                'home_team_id': home_team['id'],
                'home_team_name': home_team.get('name', 'Desconocido'),
                'away_team_id': away_team['id'],
                'away_team_name': away_team.get('name', 'Desconocido'),
                'home_runs_1st': home_runs_1st,
                'away_runs_1st': away_runs_1st,
                'yrfi': yrfi,
                'home_starter_id': home_starter.get('id'),
                'home_starter_name': home_starter.get('fullName', 'Desconocido'),
                'away_starter_id': away_starter.get('id'),
                'away_starter_name': away_starter.get('fullName', 'Desconocido'),
                'final_score': f"{away_score}-{home_score}"
            }
            
        except Exception as e:
            print(f"Error en _analyze_single_game: {e}")
            return None
    
    def generate_report(self, results: Dict, output_file: Optional[str] = None) -> str:
        """Genera un informe con los resultados del análisis YRFI."""
        report = []
        
        # Resumen general
        report.append("=" * 50)
        report.append("ANÁLISIS DE CARRERAS EN EL PRIMER INNING (YRFI)")
        report.append("=" * 50)
        report.append(f"Total de juegos analizados: {results['total_games']}")
        report.append(f"Juegos con carreras en el 1er inning (YRFI): {results['yrfi_games']} ({results['yrfi_games']/results['total_games']*100:.1f}%)")
        
        # Estadísticas por equipo
        report.append("\n" + "=" * 50)
        report.append("ESTADÍSTICAS POR EQUIPO")
        report.append("=" * 50)
        
        # Convertir a lista para ordenar
        teams_data = []
        for team_id, data in results['yrfi_by_team'].items():
            yrfi_for_pct = (data['yrfi_for'] / data['total_games']) * 100 if data['total_games'] > 0 else 0
            yrfi_against_pct = (data['yrfi_against'] / data['total_games']) * 100 if data['total_games'] > 0 else 0
            teams_data.append({
                'team_id': team_id,
                'name': data['name'],
                'yrfi_for': data['yrfi_for'],
                'yrfi_for_pct': yrfi_for_pct,
                'yrfi_against': data['yrfi_against'],
                'yrfi_against_pct': yrfi_against_pct,
                'total_games': data['total_games']
            })
        
        # Ordenar por mayor porcentaje de YRFI a favor
        teams_data.sort(key=lambda x: x['yrfi_for_pct'], reverse=True)
        
        report.append("\nEQUIPOS CON MÁS CARRERAS EN EL 1ER INNING (YRFI A FAVOR):")
        report.append("-" * 50)
        report.append(f"{'Equipo':<25} {'Juegos':>8} {'YRFI':>8} {'%':>8} {'YRFI En Contra':>15} {'%':>8}")
        report.append("-" * 50)
        for team in teams_data[:10]:  # Mostrar top 10
            report.append(f"{team['name']:<25} {team['total_games']:>8} {team['yrfi_for']:>8} {team['yrfi_for_pct']:>7.1f}% {team['yrfi_against']:>15} {team['yrfi_against_pct']:>7.1f}%")
        
        # Estadísticas de lanzadores
        report.append("\n" + "=" * 50)
        report.append("ESTADÍSTICAS DE LANZADORES (YRFI PERMITIDO)")
        report.append("=" * 50)
        
        # Convertir a lista para ordenar
        pitchers_data = []
        for pitcher_id, data in results['yrfi_by_pitcher'].items():
            if data['total_starts'] < 5:  # Mínimo 5 aperturas para estadísticas significativas
                continue
                
            yrfi_pct = (data['yrfi_allowed'] / data['total_starts']) * 100 if data['total_starts'] > 0 else 0
            pitchers_data.append({
                'pitcher_id': pitcher_id,
                'name': data['name'],
                'team': data['team_name'],
                'yrfi_allowed': data['yrfi_allowed'],
                'total_starts': data['total_starts'],
                'yrfi_pct': yrfi_pct
            })
        
        # Ordenar por mayor porcentaje de YRFI permitido
        pitchers_data.sort(key=lambda x: x['yrfi_pct'], reverse=True)
        
        report.append(f"\n{'Lanzador':<25} {'Equipo':<20} {'Aperturas':>10} {'YRFI Permitido':>15} {'%':>8}")
        report.append("-" * 50)
        for pitcher in pitchers_data[:15]:  # Mostrar top 15
            report.append(f"{pitcher['name']:<25} {pitcher['team'][:19]:<20} {pitcher['total_starts']:>10} {pitcher['yrfi_allowed']:>15} {pitcher['yrfi_pct']:>7.1f}%")
        
        # Estadísticas home vs away
        home_pct = (results['yrfi_home_vs_away']['home'] / results['yrfi_home_vs_away']['total_home'] * 100) if results['yrfi_home_vs_away']['total_home'] > 0 else 0
        away_pct = (results['yrfi_home_vs_away']['away'] / results['yrfi_home_vs_away']['total_away'] * 100) if results['yrfi_home_vs_away']['total_away'] > 0 else 0
        
        report.append("\n" + "=" * 50)
        report.append("ESTADÍSTICAS HOME VS AWAY")
        report.append("=" * 50)
        report.append(f"Equipos locales que anotan en el 1er inning: {results['yrfi_home_vs_away']['home']}/{results['yrfi_home_vs_away']['total_home']} ({home_pct:.1f}%)")
        report.append(f"Equipos visitantes que anotan en el 1er inning: {results['yrfi_home_vs_away']['away']}/{results['yrfi_home_vs_away']['total_away']} ({away_pct:.1f}%)")
        
        # Juegos recientes con YRFI
        yrfi_games = [g for g in results['games'] if g['yrfi']]
        if yrfi_games:
            report.append("\n" + "=" * 50)
            report.append(f"ÚLTIMOS {min(10, len(yrfi_games))} JUEGOS CON YRFI")
            report.append("=" * 50)
            report.append(f"{'Fecha':<12} {'Visitante':<20} {'Marcador':>10} {'Local':<20} {'1er Inning'}")
            report.append("-" * 50)
            
            for game in yrfi_games[-10:]:  # Últimos 10 juegos con YRFI
                date = game['date'].split('T')[0] if 'T' in game['date'] else game['date']
                home_score = f"{game['home_runs_1st']}R" if game['home_runs_1st'] > 0 else "0"
                away_score = f"{game['away_runs_1st']}R" if game['away_runs_1st'] > 0 else "0"
                first_inning = f"{away_score}-{home_score}"
                report.append(f"{date:<12} {game['away_team_name'][:19]:<20} {game['final_score']:>10} {game['home_team_name'][:19]:<20} {first_inning}")
        
        report_str = "\n".join(report)
        
        # Guardar en archivo si se especificó
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_str)
            print(f"Informe guardado en {output_file}")
        
        return report_str

# Ejemplo de uso
if __name__ == "__main__":
    analyzer = YRFIAnalyzer()
    
    # Obtener juegos de los últimos 7 días
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    print(f"Obteniendo juegos desde {start_date} hasta {end_date}...")
    games = analyzer.get_games_for_dates(start_date, end_date)
    print(f"Se encontraron {len(games)} juegos.")
    
    if games:
        print("Analizando carreras en el primer inning...")
        results = analyzer.analyze_yrfi(games)
        
        # Generar y mostrar el informe
        report = analyzer.generate_report(results, "yrfi_report.txt")
        print("\n" + "=" * 50)
        print("RESUMEN DEL ANÁLISIS YRFI")
        print("=" * 50)
        print(f"Juegos analizados: {results['total_games']}")
        print(f"Juegos con YRFI: {results['yrfi_games']} ({results['yrfi_games']/results['total_games']*100:.1f}%)")
        print("\nRevisa el archivo 'yrfi_report.txt' para ver el informe completo.")
    else:
        print("No se encontraron juegos para analizar en el rango de fechas especificado.")
