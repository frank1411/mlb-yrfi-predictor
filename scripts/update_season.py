#!/usr/bin/env python3
"""
Script de actualización incremental de season_data.json.

A diferencia de initialize_season_data.py (que reconstruye todo desde cero),
este script detecta el último juego guardado en el JSON y solo descarga y
procesa los partidos nuevos a partir de esa fecha.

Flujo:
  1. Carga el JSON existente.
  2. Detecta la fecha del último juego guardado.
  3. Descarga únicamente los juegos finalizados desde esa fecha hasta hoy.
  4. Filtra duplicados (por game_id).
  5. Recalcula las estadísticas de equipos con TODOS los juegos (viejos + nuevos).
  6. Actualiza los lanzadores de los partidos nuevos.
  7. Guarda el JSON actualizado.
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from src.mlb_client import MLBClient
from src.data.data_manager import (
    save_season_data,
    load_season_data,
    get_first_inning_yrfi,
    get_game_id,
    update_team_stats,
    SEASON_DATA_FILE
)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def get_last_game_date(games: List[Dict]) -> Optional[str]:
    """
    Devuelve la fecha (YYYY-MM-DD) del juego más reciente guardado en el JSON.
    Retorna None si la lista está vacía.
    """
    if not games:
        return None
    dates = [g.get('date', '') for g in games if g.get('date')]
    return max(dates) if dates else None


def fetch_games_from_api(start_date: str, end_date: str) -> List[Dict]:
    """
    Descarga de la API de MLB todos los juegos entre start_date y end_date
    (ambos inclusive) filtrando solo temporada regular (gameType == 'R').
    """
    client = MLBClient()
    all_games = []

    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    print(f"\nDescargando juegos del {start_date} al {end_date}...")

    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        try:
            schedule = client.get_schedule(date=date_str)
            day_games = []
            if 'dates' in schedule and schedule['dates']:
                day_games = schedule['dates'][0].get('games', [])
                day_games = [g for g in day_games if g.get('gameType') == 'R']
            if day_games:
                all_games.extend(day_games)
            print(f"  {date_str}: {len(day_games)} juegos regulares encontrados")
        except Exception as e:
            print(f"  [ERROR] {date_str}: {e}")

        current += timedelta(days=1)

    print(f"Total descargados de la API: {len(all_games)} juegos")
    return all_games


def process_game(game: Dict) -> Optional[Dict]:
    """
    Transforma el formato crudo de la API al formato interno del JSON.
    Retorna None si el juego no está finalizado o no tiene datos suficientes.
    """
    status = game.get('status', {})
    abstract_code = str(status.get('abstractGameCode', ''))
    status_code = str(status.get('statusCode', ''))
    detailed_state = str(status.get('detailedState', '')).lower()

    # Solo procesar juegos finalizados
    is_final = (
        abstract_code == 'F' and
        status_code in ['F', 'O', 'D', 'C', 'CE', 'FR'] and
        (detailed_state in ['final', 'game over'] or 'completed early' in detailed_state)
    )

    if not is_final:
        return None

    # Extraer fecha
    game_date = game.get('officialDate') or game.get('gameDate', '')
    if 'T' in game_date:
        game_date = game_date.split('T')[0]

    if not game_date:
        return None

    # Datos YRFI del primer inning
    yrfi_data = get_first_inning_yrfi(game)

    # Equipos
    teams = game.get('teams', {})
    if 'home' not in teams or 'away' not in teams:
        return None

    home_team_id = str(teams['home']['team']['id'])
    away_team_id = str(teams['away']['team']['id'])
    home_team_name = teams['home']['team'].get('name', 'Desconocido')
    away_team_name = teams['away']['team'].get('name', 'Desconocido')

    # Lanzadores (inicio probable o de boxscore)
    def extract_pitcher(side: str) -> Optional[Dict]:
        pitcher = teams.get(side, {}).get('probablePitcher')
        if pitcher and pitcher.get('id'):
            return {'id': pitcher['id'], 'name': pitcher.get('fullName', 'Desconocido')}
        return None

    processed = {
        'game_id': get_game_id(game),
        'date': game_date,
        'home_yrfi': yrfi_data['home_yrfi'],
        'away_yrfi': yrfi_data['away_yrfi'],
        'game_yrfi': yrfi_data['game_yrfi'],
        'status': {
            'abstractGameCode': abstract_code,
            'statusCode': status_code,
            'detailedState': detailed_state
        },
        'home_team': home_team_id,
        'home_team_name': home_team_name,
        'away_team': away_team_id,
        'away_team_name': away_team_name,
        'gamePk': game.get('gamePk'),
        'pitchers': {
            'home': extract_pitcher('home'),
            'away': extract_pitcher('away')
        }
    }

    return processed


def update_pitchers_from_api(games: List[Dict], start_date: str, end_date: str) -> List[Dict]:
    """
    Para los juegos nuevos sin lanzadores confirmados, intenta obtenerlos
    haciendo una consulta de horario con hidratación de lanzadores probables.
    Respeta lanzadores ya guardados manualmente.
    """
    client = MLBClient()
    try:
        params = {
            'sportId': 1,
            'startDate': start_date,
            'endDate': end_date,
            'hydrate': 'probablePitcher',
            'gameType': 'R'
        }
        response = client._make_request('schedule', params=params)

        # Construir diccionario gamePk → lanzadores
        pitcher_map: Dict[str, Dict] = {}
        for date_data in response.get('dates', []):
            for g in date_data.get('games', []):
                pk = str(g.get('gamePk', ''))
                if not pk:
                    continue
                home_p = g.get('teams', {}).get('home', {}).get('probablePitcher')
                away_p = g.get('teams', {}).get('away', {}).get('probablePitcher')
                pitcher_map[pk] = {
                    'home': {'id': home_p['id'], 'name': home_p.get('fullName', '')} if home_p else None,
                    'away': {'id': away_p['id'], 'name': away_p.get('fullName', '')} if away_p else None,
                }

        # Aplicar al listado de juegos
        updated = []
        for game in games:
            pk = str(game.get('gamePk', ''))
            if pk in pitcher_map:
                api_pitchers = pitcher_map[pk]
                existing = game.get('pitchers', {})

                # Preservar lanzadores manuales si la API no devuelve nada
                merged = {
                    'home': api_pitchers['home'] or existing.get('home'),
                    'away': api_pitchers['away'] or existing.get('away'),
                }
                game['pitchers'] = merged
            updated.append(game)
        return updated

    except Exception as e:
        print(f"  [WARN] No se pudieron actualizar lanzadores desde la API: {e}")
        return games


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  UPDATE SEASON — Actualización incremental de datos")
    print("=" * 55)

    # 1. Cargar JSON existente
    print("\n[1] Cargando datos existentes...")
    current_data = load_season_data()
    existing_games: List[Dict] = current_data.get('games', [])
    existing_teams: Dict = current_data.get('teams', {})
    existing_pitchers: Dict = current_data.get('pitchers', {})

    print(f"    Juegos existentes en el JSON: {len(existing_games)}")

    # Construir set de IDs ya existentes para detección rápida de duplicados
    existing_ids: set = {str(g.get('game_id', '')) for g in existing_games if g.get('game_id')}
    print(f"    IDs únicos registrados: {len(existing_ids)}")

    # 2. Detectar fecha del último juego guardado
    last_date = get_last_game_date(existing_games)
    today = datetime.now().strftime('%Y-%m-%d')

    if last_date:
        # Empezar desde el mismo día del último registro para no perder
        # juegos que pudieron completarse tarde (re-procesamos ese día).
        start_date = last_date
        print(f"\n[2] Último juego guardado: {last_date}")
        print(f"    Descargando desde {start_date} hasta hoy ({today})")
    else:
        # JSON vacío: inicio de temporada regular 2026
        start_date = '2026-03-25'
        print(f"\n[2] JSON vacío. Descargando desde el inicio de temporada: {start_date}")

    # Sin datos nuevos posibles
    if start_date > today:
        print("\n✅ El JSON ya está al día. No hay fechas nuevas que procesar.")
        return

    # 3. Descargar juegos del rango
    print(f"\n[3] Consultando la API de MLB...")
    raw_games = fetch_games_from_api(start_date, today)

    # 4. Procesar y filtrar solo juegos finalizados y no duplicados
    print(f"\n[4] Procesando juegos descargados...")
    new_games: List[Dict] = []
    skipped_dup = 0
    skipped_not_final = 0

    for raw in raw_games:
        processed = process_game(raw)
        if processed is None:
            skipped_not_final += 1
            continue
        gid = str(processed.get('game_id', ''))
        if gid in existing_ids:
            skipped_dup += 1
            continue
        new_games.append(processed)
        existing_ids.add(gid)  # Prevenir duplicados dentro del mismo batch

    print(f"    Juegos finalizados nuevos encontrados: {len(new_games)}")
    print(f"    Omitidos por duplicado: {skipped_dup}")
    print(f"    Omitidos por no finalizados: {skipped_not_final}")

    if not new_games:
        print("\n✅ No hay juegos nuevos para agregar. El JSON ya está al día.")
        return

    # 5. Actualizar lanzadores de los juegos nuevos
    print(f"\n[5] Actualizando lanzadores para los {len(new_games)} juegos nuevos...")
    new_games = update_pitchers_from_api(new_games, start_date, today)

    # 6. Combinar (viejos + nuevos) y recalcular estadísticas de equipos
    print(f"\n[6] Combinando juegos y recalculando estadísticas de equipos...")
    all_games = existing_games + new_games

    # Ordenar por fecha (más antiguo primero)
    all_games.sort(key=lambda g: g.get('date', ''))

    # Recalcular estadísticas de equipos desde cero con todos los juegos
    teams = update_team_stats({}, all_games)

    # Parchar nombres reales de equipos (update_team_stats usa 'Equipo {id}' como placeholder)
    for game in all_games:
        ht_id = game.get('home_team')
        at_id = game.get('away_team')
        ht_name = game.get('home_team_name')
        at_name = game.get('away_team_name')
        if ht_id and ht_name and ht_id in teams:
            teams[ht_id]['name'] = ht_name
        if at_id and at_name and at_id in teams:
            teams[at_id]['name'] = at_name

    print(f"    Total de juegos en el JSON: {len(all_games)}")
    print(f"    Equipos registrados: {len(teams)}")

    # 7. Guardar
    print(f"\n[7] Guardando JSON actualizado...")
    updated_data = {
        'last_updated': datetime.now().isoformat(),
        'teams': teams,
        'pitchers': existing_pitchers,  # Preservar lanzadores manuales existentes
        'games': all_games
    }
    save_season_data(updated_data)

    # ─── Resumen final ───
    total_yrfi = sum(1 for g in all_games if g.get('game_yrfi'))
    yrfi_pct = (total_yrfi / len(all_games) * 100) if all_games else 0

    print("\n" + "=" * 55)
    print("  ✅ Actualización completada exitosamente")
    print("=" * 55)
    print(f"  Juegos nuevos agregados : {len(new_games)}")
    print(f"  Total de juegos en JSON : {len(all_games)}")
    print(f"  YRFI global             : {total_yrfi}/{len(all_games)} ({yrfi_pct:.1f}%)")

    # Top 3 equipos con más YRFI
    teams_sorted = sorted(
        [(td.get('name', tid), td.get('total_yrfi', 0), td.get('total_games', 0))
         for tid, td in teams.items()],
        key=lambda x: x[1], reverse=True
    )
    print("\n  Top 3 equipos YRFI:")
    for name, yrfi, total in teams_sorted[:3]:
        pct = (yrfi / total * 100) if total else 0
        print(f"    {name}: {yrfi}/{total} ({pct:.1f}%)")

    print("\n  Últimos 3 juegos nuevos:")
    for g in new_games[-3:]:
        result = '✅ YRFI' if g.get('game_yrfi') else '❌ NRFI'
        print(f"    {g['date']} | {g['away_team_name']} @ {g['home_team_name']} | {result}")


if __name__ == "__main__":
    main()
