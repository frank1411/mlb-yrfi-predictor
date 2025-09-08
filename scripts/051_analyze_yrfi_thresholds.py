#!/usr/bin/env python3
"""
Script para analizar el rendimiento del modelo YRFI con diferentes umbrales.
Analiza por separado YRFI Local, Visitante y Partido.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / 'evaluation' / 'backtesting_results.csv'
OUTPUT_DIR = PROJECT_ROOT / 'evaluation'

# Umbrales a probar (buscando mayor precisión)
UMBRALES = [
    0.50, 0.52, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.60,  # Rango medio
    0.62, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.70,          # Rango alto
    0.72, 0.74, 0.75, 0.76, 0.78, 0.80, 0.82, 0.84, 0.85,    # Rango muy alto
    0.86, 0.88, 0.90, 0.92, 0.94, 0.95, 0.96, 0.98, 1.00     # Rango extremo
]

def load_data():
    """Carga los datos de backtesting."""
    print(f"Cargando datos desde {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    print(f"Datos cargados: {len(df)} partidos")
    return df

def analyze_yrfi_type(df, prob_col, target_col, yrfi_type):
    """Analiza el rendimiento para un tipo específico de YRFI."""
    print(f"\n{'='*60}")
    print(f"{'ANÁLISIS DE ' + yrfi_type.upper() + ' YRFI':^60}")
    print("="*60)
    
    resultados = []
    
    for umbral in UMBRALES:
        # Aplicar umbral
        pred_col = f'pred_{yrfi_type}_{umbral:.2f}'
        df[pred_col] = (df[prob_col] >= umbral).astype(int)
        
        # Calcular métricas
        total = len(df)
        preds = df[df[pred_col] == 1]
        total_preds = len(preds)
        aciertos = preds[preds[target_col] == 1]
        total_aciertos = len(aciertos)
        
        precision = total_aciertos / total_preds if total_preds > 0 else 0
        cobertura = total_preds / total
        rentabilidad = (precision * 1.9 - 1) * 100  # Asumiendo cuota de 1.90
        
        resultados.append({
            'Tipo': yrfi_type,
            'Umbral': umbral,
            'Total Partidos': total,
            'Predicciones': total_preds,
            'Aciertos': total_aciertos,
            'Precisión': precision * 100,
            'Cobertura': cobertura * 100,
            'Rentabilidad %': rentabilidad
        })
        
        print(f"\n{'='*30} UMBRAL: {umbral:.2f} {'='*30}")
        print(f"Predicciones {yrfi_type}: {total_preds} ({cobertura*100:.1f}% de los partidos)")
        print(f"Aciertos: {total_aciertos} (Precisión: {precision*100:.1f}%)")
        print(f"Rentabilidad estimada: {rentabilidad:.1f}%")
    
    return pd.DataFrame(resultados)

def plot_results(resultados, output_file):
    """Genera gráficos de los resultados."""
    plt.figure(figsize=(15, 10))
    
    # Gráfico de precisión por umbral
    plt.subplot(2, 2, 1)
    for tipo, grupo in resultados.groupby('Tipo'):
        plt.plot(grupo['Umbral'], grupo['Precisión'], 'o-', label=tipo)
    plt.axhline(y=52.63, color='r', linestyle='--', label='Punto de equilibrio (52.63%)')
    plt.title('Precisión por Umbral')
    plt.xlabel('Umbral de Probabilidad')
    plt.ylabel('Precisión (%)')
    plt.legend()
    plt.grid(True)
    
    # Gráfico de cobertura por umbral
    plt.subplot(2, 2, 2)
    for tipo, grupo in resultados.groupby('Tipo'):
        plt.plot(grupo['Umbral'], grupo['Cobertura'], 'o-', label=tipo)
    plt.title('Cobertura por Umbral')
    plt.xlabel('Umbral de Probabilidad')
    plt.ylabel('Cobertura (% de partidos)')
    plt.legend()
    plt.grid(True)
    
    # Gráfico de rentabilidad por umbral
    plt.subplot(2, 2, 3)
    for tipo, grupo in resultados.groupby('Tipo'):
        plt.plot(grupo['Umbral'], grupo['Rentabilidad %'], 'o-', label=tipo)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Rentabilidad por Umbral')
    plt.xlabel('Umbral de Probabilidad')
    plt.ylabel('Rentabilidad Esperada (%)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"\n📈 Gráficos guardados en: {output_file}")

def main():
    """Función principal."""
    # Cargar datos
    df = load_data()
    
    # Verificar columnas disponibles
    required_cols = [
        'prob_local_anota', 'prob_visitante_anota', 'prob_yrfi_predicha', 
        'game_yrfi_real', 'home_yrfi_target', 'away_yrfi_target'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Faltan columnas obligatorias en los datos: {missing_cols}")
        print("Columnas disponibles:", df.columns.tolist())
        return
    
    # Analizar cada tipo de YRFI
    resultados = []
    
    # YRFI Local (usando datos reales)
    res_local = analyze_yrfi_type(df, 'prob_local_anota', 'home_yrfi_target', 'Local')
    resultados.append(res_local)
    
    # YRFI Visitante (usando datos reales)
    res_visitante = analyze_yrfi_type(df, 'prob_visitante_anota', 'away_yrfi_target', 'Visitante')
    resultados.append(res_visitante)
    
    # YRFI Partido (datos reales)
    res_partido = analyze_yrfi_type(df, 'prob_yrfi_predicha', 'game_yrfi_real', 'Partido')
    resultados.append(res_partido)
    
    # Combinar resultados
    resultados_df = pd.concat(resultados)
    
    # Guardar resultados
    output_file = OUTPUT_DIR / 'analisis_yrfi_detallado.csv'
    resultados_df.to_csv(output_file, index=False)
    print(f"\n📊 Resultados detallados guardados en: {output_file}")
    
    # Generar gráficos
    plot_file = OUTPUT_DIR / 'graficos_analisis_yrfi.png'
    plot_results(resultados_df, plot_file)
    
    # Mostrar resumen del mejor umbral para cada tipo
    print("\n" + "="*60)
    print(f"{'MEJORES UMBRALES POR TIPO':^60}")
    print("="*60)
    
    for tipo in ['Local', 'Visitante', 'Partido']:
        df_tipo = resultados_df[resultados_df['Tipo'] == tipo]
        if not df_tipo.empty:
            # Mejor por precisión (mínimo 5% de cobertura para evitar umbrales muy restrictivos)
            df_cobertura = df_tipo[df_tipo['Cobertura'] >= 5]
            mejor_prec = df_cobertura.loc[df_cobertura['Precisión'].idxmax()] if not df_cobertura.empty else None
            
            # Mejor por rentabilidad (mínimo 5% de cobertura)
            mejor_rent = df_cobertura.loc[df_cobertura['Rentabilidad %'].idxmax()] if not df_cobertura.empty else None
            
            # Mejor precisión > 33% para individuales o > 54% para partidos
            if tipo in ['Local', 'Visitante']:
                df_alta_precision = df_tipo[df_tipo['Precisión'] > 33]
            else:
                df_alta_precision = df_tipo[df_tipo['Precisión'] > 54]
                
            mejor_alta_prec = df_alta_precision.loc[df_alta_precision['Precisión'].idxmax()] if not df_alta_precision.empty else None
            
            print(f"\n🏆 MEJOR PARA {tipo.upper()}:")
            
            if mejor_prec is not None:
                print(f"\n   Mejor precisión (cobertura > 5%):")
                print(f"   - Umbral: {mejor_prec['Umbral']:.2f}")
                print(f"   - Precisión: {mejor_prec['Precisión']:.1f}%")
                print(f"   - Cobertura: {mejor_prec['Cobertura']:.1f}%")
                print(f"   - Rentabilidad: {mejor_prec['Rentabilidad %']:.1f}%")
            
            if mejor_rent is not None and (mejor_prec is None or mejor_rent['Umbral'] != mejor_prec['Umbral']):
                print(f"\n   Mejor rentabilidad (cobertura > 5%):")
                print(f"   - Umbral: {mejor_rent['Umbral']:.2f}")
                print(f"   - Precisión: {mejor_rent['Precisión']:.1f}%")
                print(f"   - Cobertura: {mejor_rent['Cobertura']:.1f}%")
                print(f"   - Rentabilidad: {mejor_rent['Rentabilidad %']:.1f}%")
            
            if mejor_alta_prec is not None and (mejor_prec is None or mejor_alta_prec['Umbral'] != mejor_prec['Umbral']):
                print(f"\n   🔥 Alta precisión (>{'33' if tipo in ['Local', 'Visitante'] else '54'}%):")
                print(f"   - Umbral: {mejor_alta_prec['Umbral']:.2f}")
                print(f"   - Precisión: {mejor_alta_prec['Precisión']:.1f}%")
                print(f"   - Cobertura: {mejor_alta_prec['Cobertura']:.1f}%")
                print(f"   - Rentabilidad: {mejor_alta_prec['Rentabilidad %']:.1f}%")
            
            if mejor_prec is None and mejor_rent is None and mejor_alta_prec is None:
                print("   No se encontraron umbrales con cobertura suficiente.")
                
                # Mostrar el mejor sin filtro de cobertura
                mejor_sin_filtro = df_tipo.loc[df_tipo['Precisión'].idxmax()]
                print(f"\n   Mejor precisión (sin filtro de cobertura):")
                print(f"   - Umbral: {mejor_sin_filtro['Umbral']:.2f}")
                print(f"   - Precisión: {mejor_sin_filtro['Precisión']:.1f}%")
                print(f"   - Cobertura: {mejor_sin_filtro['Cobertura']:.1f}%")
                print(f"   - Rentabilidad: {mejor_sin_filtro['Rentabilidad %']:.1f}%")
    
    print("\n✅ Análisis completado")

if __name__ == "__main__":
    main()
