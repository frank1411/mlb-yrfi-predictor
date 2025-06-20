import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

class MLBClient:
    """
    Cliente para interactuar con la API de MLB (Major League Baseball).
    """
    
    BASE_URL = "https://statsapi.mlb.com/api/v1/"
    
    def __init__(self, timeout: int = 10):
        """
        Inicializa el cliente de MLB.
        
        Args:
            timeout: Tiempo máximo de espera para las peticiones HTTP.
        """
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({
            'User-Agent': 'MLB-API-Client/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API de MLB.
        
        Args:
            endpoint: Endpoint de la API a consultar.
            params: Parámetros de la consulta.
            
        Returns:
            Diccionario con la respuesta de la API.
            
        Raises:
            requests.exceptions.HTTPError: Si la petición falla.
        """
        url = urljoin(self.BASE_URL, endpoint)
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_game(self, game_pk: int) -> Dict[str, Any]:
        """
        Obtiene información detallada de un juego por su ID.
        
        Args:
            game_pk: ID único del juego.
            
        Returns:
            Diccionario con la información detallada del juego.
        """
        return self._make_request(f"game/{game_pk}/feed/live")
    
    def get_starting_pitchers(self, game_pk: int) -> Dict[str, Dict]:
        """
        Obtiene los lanzadores iniciales de un juego.
        
        Args:
            game_pk: ID único del juego.
            
        Returns:
            Diccionario con los IDs y nombres de los lanzadores iniciales:
            {
                'home': {'id': '123', 'name': 'Pitcher Name'},
                'away': {'id': '456', 'name': 'Pitcher Name'}
            }
            
            Si no se pueden obtener los lanzadores, devuelve un diccionario vacío.
        """
        try:
            game_data = self.get_game(game_pk)
            
            # Obtener los lanzadores iniciales
            home_pitcher = {}
            away_pitcher = {}
            
            # Buscar en los jugadores del juego
            players = game_data.get('gameData', {}).get('players', {})
            
            # Buscar en las alineaciones iniciales
            for team in ['home', 'away']:
                lineup = game_data.get('liveData', {}).get('linescore', {}).get('teams', {}).get(team, {})
                
                # Buscar el lanzador inicial en el boxscore
                pitcher_id = None
                for player in lineup.get('players', {}).values():
                    if player.get('position', {}).get('code') == '1':  # Código 1 es lanzador
                        pitcher_id = str(player.get('person', {}).get('id'))
                        break
                
                # Si encontramos el lanzador, obtener su nombre
                if pitcher_id and pitcher_id in players:
                    player_info = players[pitcher_id]
                    pitcher_data = {
                        'id': pitcher_id,
                        'name': f"{player_info.get('nameFirst', '')} {player_info.get('nameLast', '')}".strip()
                    }
                    
                    if team == 'home':
                        home_pitcher = pitcher_data
                    else:
                        away_pitcher = pitcher_data
            
            return {
                'home': home_pitcher,
                'away': away_pitcher
            }
            
        except Exception as e:
            print(f"Error al obtener lanzadores para el juego {game_pk}: {str(e)}")
            return {}
    
    def get_team(self, team_id: int) -> Dict[str, Any]:
        """
        Obtiene información de un equipo por su ID.
        
        Args:
            team_id: ID del equipo.
            
        Returns:
            Diccionario con la información del equipo.
        """
        endpoint = f"teams/{team_id}"
        return self._make_request(endpoint)
    
    def get_team_roster(self, team_id: int, roster_type: str = 'active') -> Dict[str, Any]:
        """
        Obtiene la plantilla de un equipo.
        
        Args:
            team_id: ID del equipo.
            roster_type: Tipo de plantilla ('active', 'coach', 'fullRoster', etc.).
            
        Returns:
            Diccionario con la plantilla del equipo.
        """
        endpoint = f"teams/{team_id}/roster/{roster_type}"
        return self._make_request(endpoint)
    
    def get_player(self, player_id: int) -> Dict[str, Any]:
        """
        Obtiene información de un jugador por su ID.
        
        Args:
            player_id: ID del jugador.
            
        Returns:
            Diccionario con la información del jugador.
        """
        endpoint = f"people/{player_id}"
        return self._make_request(endpoint)
    
    def get_schedule(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene el calendario de partidos.
        
        Args:
            date: Fecha en formato 'YYYY-MM-DD'. Si es None, usa la fecha actual.
            
        Returns:
            Diccionario con los partidos programados.
        """
        endpoint = "schedule"
        params = {
            'sportId': 1,  # 1 es el ID para MLB
            'hydrate': 'team,linescore,game(content(summary))'
        }
        
        if date:
            params['date'] = date
            
        return self._make_request(endpoint, params=params)
    
    def get_standings(self, league_id: str = '103,104') -> Dict[str, Any]:
        """
        Obtiene la tabla de posiciones de las ligas especificadas.
        
        Args:
            league_id: IDs de las ligas separados por comas (103: AL, 104: NL).
            
        Returns:
            Diccionario con la tabla de posiciones.
        """
        return self._make_request(f"standings?leagueId={league_id}")
        
    def get_games_for_team_and_date(self, team_id: int, date: datetime) -> List[Dict]:
        """
        Obtiene los juegos de un equipo en una fecha específica.
        
        Args:
            team_id: ID del equipo.
            date: Fecha para la cual buscar los juegos.
            
        Returns:
            Lista de juegos del equipo en la fecha especificada.
        """
        date_str = date.strftime('%Y-%m-%d')
        params = {
            'sportId': 1,  # MLB
            'teamId': team_id,
            'date': date_str
        }
        response = self._make_request("schedule", params=params)
        
        if 'dates' in response and response['dates']:
            return response['dates'][0].get('games', [])
        return []

# Ejemplo de uso
if __name__ == "__main__":
    client = MLBClient()
    
    # Obtener información de los Yankees (ID: 147)
    yankees = client.get_team(147)
    print(f"Equipo: {yankees['teams'][0]['name']}")
    
    # Obtener el calendario de hoy
    schedule = client.get_schedule()
    print("\nPartidos de hoy:")
    for game in schedule.get('dates', [{}])[0].get('games', []):
        print(f"{game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']}")
