"""
Módulo para visualizar estadísticas de carreras en el primer inning (YRFI).
"""
from typing import Dict, List, Any, Optional
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

class YRFIVisualizer:
    """Clase para generar visualizaciones de estadísticas YRFI."""
    
    def __init__(self, output_dir: str = "reports"):
        """Inicializa el visualizador con el directorio de salida."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configurar el estilo de las gráficas
        plt.style.use('seaborn-v0_8')
        sns.set_theme(style="whitegrid")
        sns.set_palette("viridis")
    
    def _save_plot(self, filename: str) -> str:
        """Guarda el gráfico actual en un archivo."""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    
    def plot_team_yrfi_rates(self, team_stats: Dict, days: int = 30) -> str:
        """Genera un gráfico de barras con las tasas YRFI por equipo.
        
        Args:
            team_stats: Diccionario con estadísticas por equipo
            days: Número de días analizados (para el título)
            
        Returns:
            Ruta al archivo de la imagen generada
        """
        # Convertir a DataFrame para facilitar el manejo
        teams_data = []
        for team_id, data in team_stats.items():
            if data['total_games'] > 0:
                teams_data.append({
                    'Equipo': data['name'],
                    'YRFI a Favor (%)': (data['yrfi_for'] / data['total_games']) * 100,
                    'YRFI en Contra (%)': (data['yrfi_against'] / data['total_games']) * 100,
                    'Total Juegos': data['total_games']
                })
        
        if not teams_data:
            return ""
            
        df = pd.DataFrame(teams_data)
        
        # Ordenar por YRFI a favor
        df = df.sort_values('YRFI a Favor (%)', ascending=False).head(15)
        
        # Crear figura
        plt.figure(figsize=(12, 8))
        
        # Gráfico de barras apiladas
        df_melted = df.melt(id_vars=['Equipo', 'Total Juegos'], 
                           value_vars=['YRFI a Favor (%)', 'YRFI en Contra (%)'],
                           var_name='Tipo', value_name='Porcentaje')
        
        ax = sns.barplot(data=df_melted, x='Equipo', y='Porcentaje', 
                        hue='Tipo', alpha=0.8)
        
        # Añadir etiquetas
        plt.title(f'Porcentaje de carreras en el 1er inning por equipo (últimos {days} días)', 
                 fontsize=14, pad=20)
        plt.xlabel('Equipo', fontsize=12)
        plt.ylabel('Porcentaje de juegos', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 110)
        
        # Añadir etiquetas con el total de juegos
        for i, team in enumerate(df['Equipo']):
            total = df.loc[df['Equipo'] == team, 'Total Juegos'].values[0]
            plt.text(i, 105, f'n={total}', ha='center', fontsize=8)
        
        # Mover la leyenda
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        return self._save_plot(f'team_yrfi_rates_{days}d.png')
    
    def plot_pitcher_yrfi_rates(self, pitcher_stats: Dict, min_starts: int = 5) -> str:
        """Genera un gráfico de dispersión de lanzadores por YRFI permitido.
        
        Args:
            pitcher_stats: Diccionario con estadísticas por lanzador
            min_starts: Mínimo de aperturas para incluir a un lanzador
            
        Returns:
            Ruta al archivo de la imagen generada
        """
        # Filtrar lanzadores con mínimo de aperturas
        pitchers = []
        for pid, data in pitcher_stats.items():
            if data['total_starts'] >= min_starts:
                pitchers.append({
                    'Lanzador': data['name'],
                    'Equipo': data['team_name'],
                    'YRFI Permitido (%)': (data['yrfi_allowed'] / data['total_starts']) * 100,
                    'Aperturas': data['total_starts']
                })
        
        if not pitchers:
            return ""
            
        df = pd.DataFrame(pitchers)
        
        # Crear figura
        plt.figure(figsize=(14, 8))
        
        # Gráfico de dispersión
        scatter = sns.scatterplot(data=df, x='Aperturas', y='YRFI Permitido (%)', 
                                size='Aperturas', sizes=(50, 300), 
                                alpha=0.7, hue='Equipo')
        
        # Añadir etiquetas a los puntos más relevantes
        for i, row in df.iterrows():
            if row['Apertures'] >= df['Aperturas'].quantile(0.75) or \
               row['YRFI Permitido (%)'] >= df['YRFI Permitido (%)'].quantile(0.9):
                plt.text(row['Aperturas'] + 0.2, row['YRFI Permitido (%)'], 
                         row['Lanzador'].split()[-1], 
                         fontsize=8, ha='left', va='center')
        
        # Líneas de referencia
        plt.axhline(y=df['YRFI Permitido (%)'].median(), color='r', linestyle='--', alpha=0.5)
        plt.axvline(x=df['Aperturas'].median(), color='r', linestyle='--', alpha=0.5)
        
        # Añadir etiquetas
        plt.title('Rendimiento de lanzadores en el 1er inning', fontsize=14, pad=20)
        plt.xlabel('Número de aperturas', fontsize=12)
        plt.ylabel('Porcentaje de YRFI permitido', fontsize=12)
        
        # Mover la leyenda
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Equipo')
        
        return self._save_plot('pitcher_yrfi_scatter.png')
    
    def plot_yrfi_trend(self, games_data: List[Dict], window: int = 7) -> str:
        """Genera un gráfico de tendencia de YRFI a lo largo del tiempo.
        
        Args:
            games_data: Lista de diccionarios con datos de juegos
            window: Tamaño de la ventana móvil para el promedio
            
        Returns:
            Ruta al archivo de la imagen generada
        """
        if not games_data:
            return ""
            
        # Convertir a DataFrame
        df = pd.DataFrame(games_data)
        
        # Convertir fecha a datetime
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Agrupar por fecha
        daily = df.groupby('date').agg({
            'yrfi': ['sum', 'count'],
            'home_runs_1st': 'sum',
            'away_runs_1st': 'sum'
        })
        daily.columns = ['yrfi_count', 'total_games', 'home_runs', 'away_runs']
        daily = daily.reset_index()
        
        # Calcular porcentaje y media móvil
        daily['yrfi_pct'] = (daily['yrfi_count'] / daily['total_games']) * 100
        daily['yrfi_ma'] = daily['yrfi_pct'].rolling(window=window, min_periods=1).mean()
        
        # Crear figura
        plt.figure(figsize=(14, 7))
        
        # Gráfico de barras para el conteo diario
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        # Barras para juegos totales y con YRFI
        bar1 = ax1.bar(daily['date'], daily['total_games'], 
                      alpha=0.3, color='gray', label='Juegos totales')
        bar2 = ax1.bar(daily['date'], daily['yrfi_count'], 
                      alpha=0.7, color='salmon', label='Juegos con YRFI')
        
        # Línea para el porcentaje de YRFI
        line = ax2.plot(daily['date'], daily['yrfi_ma'], 
                       'r-', linewidth=2, 
                       label=f'YRFI % (media móvil {window}d)')
        
        # Añadir etiquetas
        plt.title('Tendencia de carreras en el 1er inning (YRFI)', fontsize=14, pad=20)
        ax1.set_xlabel('Fecha', fontsize=12)
        ax1.set_ylabel('Número de juegos', fontsize=12)
        ax2.set_ylabel('Porcentaje de YRFI', fontsize=12)
        
        # Combinar leyendas
        bars = [bar1, bar2, line[0]]
        labels = [b.get_label() for b in bars]
        ax1.legend(bars, labels, loc='upper left')
        
        # Formato de fechas
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._save_plot('yrfi_trend.png')
    
    def plot_team_comparison(self, team_stats: Dict, team_ids: List[int]) -> str:
        """Genera un gráfico comparativo entre equipos seleccionados.
        
        Args:
            team_stats: Diccionario con estadísticas por equipo
            team_ids: Lista de IDs de equipos a comparar
            
        Returns:
            Ruta al archivo de la imagen generada
        """
        # Filtrar equipos seleccionados
        teams_to_compare = []
        for tid in team_ids:
            if tid in team_stats and team_stats[tid]['total_games'] > 0:
                teams_to_compare.append({
                    'Equipo': team_stats[tid]['name'],
                    'YRFI a Favor': team_stats[tid]['yrfi_for'],
                    'YRFI en Contra': team_stats[tid]['yrfi_against'],
                    'Total Juegos': team_stats[tid]['total_games']
                })
        
        if not teams_to_compare:
            return ""
            
        df = pd.DataFrame(teams_to_compare)
        
        # Calcular porcentajes
        df['YRFI a Favor %'] = (df['YRFI a Favor'] / df['Total Juegos']) * 100
        df['YRFI en Contra %'] = (df['YRFI en Contra'] / df['Total Juegos']) * 100
        
        # Ordenar por YRFI a favor
        df = df.sort_values('YRFI a Favor %', ascending=False)
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Gráfico de barras para YRFI a favor
        sns.barplot(data=df, x='Equipo', y='YRFI a Favor %', 
                   ax=ax1, color='lightgreen', alpha=0.7,
                   label='YRFI a Favor')
        
        # Gráfico de barras para YRFI en contra
        sns.barplot(data=df, x='Equipo', y='YRFI en Contra %', 
                   ax=ax2, color='lightcoral', alpha=0.7,
                   label='YRFI en Contra')
        
        # Añadir etiquetas y títulos
        ax1.set_title('Comparativa de equipos: YRFI a Favor', fontsize=14, pad=10)
        ax2.set_title('Comparativa de equipos: YRFI en Contra', fontsize=14, pad=10)
        
        for ax in [ax1, ax2]:
            ax.set_xlabel('')
            ax.set_ylabel('Porcentaje de juegos', fontsize=10)
            ax.tick_params(axis='x', rotation=45)
            
            # Añadir etiquetas con el total de juegos
            for i, team in enumerate(df['Equipo']):
                total = df.loc[df['Equipo'] == team, 'Total Juegos'].values[0]
                ax.text(i, 5, f'n={total}', ha='center', fontsize=8, 
                       bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        plt.tight_layout()
        
        return self._save_plot('team_comparison.png')
