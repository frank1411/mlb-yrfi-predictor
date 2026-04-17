#!/usr/bin/env python3
"""
Script de evaluación del modelo YRFI — Feedback Loop
======================================================
Diseñado con apoyo de Ollama (gemma4:31b).

Compara predicciones históricas contra resultados reales del season_data.json
para calcular métricas de precisión, calibración y tendencias temporales.

Genera reportes en formato JSON y Markdown en el directorio reports/.

Uso:
    venv/bin/python3 scripts/evaluate_predictions.py
    venv/bin/python3 scripts/evaluate_predictions.py --date 2026-04-17
    venv/bin/python3 scripts/evaluate_predictions.py --umbral 0.65
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
PREDICTIONS_DIR = ROOT / "predictions"
SEASON_DATA_FILE = ROOT / "data" / "season_data.json"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLDS = [0.50, 0.60, 0.70, 0.80, 0.90]
DEFAULT_DECISION_THRESHOLD = 0.50
PERFORMANCE_GATE = 0.55  # Mínimo aceptable de accuracy


# ─────────────────────────────────────────────
# 1. CARGA DE DATOS
# ─────────────────────────────────────────────

def load_predictions(predictions_dir: Path = PREDICTIONS_DIR) -> List[Dict]:
    """
    Carga todas las predicciones JSON desde la carpeta predictions/.
    Retorna lista de dicts con campos normalizados.
    """
    preds = []
    json_files = sorted(predictions_dir.glob("yrfi_*.json"))

    if not json_files:
        print(f"  [WARN] No se encontraron archivos de predicción en {predictions_dir}")
        return []

    print(f"  Archivos de predicción encontrados: {len(json_files)}")
    errors = 0

    for fpath in json_files:
        try:
            with open(fpath, encoding="utf-8") as f:
                raw = json.load(f)

            # Extraer probabilidad YRFI
            yrfi_prob = raw.get("prediction", {}).get("yrfi_probability")
            if yrfi_prob is None:
                # Fallback al campo anidado
                yrfi_prob = raw.get("prediction", {}).get(
                    "calculation", {}
                ).get("game_yrfi_probability")

            if yrfi_prob is None:
                errors += 1
                continue

            game_pk = str(raw.get("game_pk", ""))
            game_date = raw.get("game_date", "")
            generated_at = raw.get("metadata", {}).get("generated_at", "")

            preds.append({
                "game_id": game_pk,
                "game_date": game_date,
                "home_team_id": raw.get("home_team", {}).get("id", ""),
                "home_team_name": raw.get("home_team", {}).get("name", ""),
                "away_team_id": raw.get("away_team", {}).get("id", ""),
                "away_team_name": raw.get("away_team", {}).get("name", ""),
                "yrfi_probability": float(yrfi_prob) / 100.0,  # Normalizar 0-1
                "home_pitcher": raw.get("home_team", {}).get("pitcher", {}).get("name", "N/D"),
                "away_pitcher": raw.get("away_team", {}).get("pitcher", {}).get("name", "N/D"),
                "generated_at": generated_at,
                "_source": fpath.name,
            })

        except Exception as e:
            print(f"  [ERROR] {fpath.name}: {e}")
            errors += 1

    if errors:
        print(f"  [WARN] {errors} archivo(s) ignorado(s) por errores")

    return preds


def load_season_results(path: Path = SEASON_DATA_FILE) -> Dict[str, Dict]:
    """
    Carga los juegos finalizados del season_data.json.
    Retorna dict indexado por game_id (str).
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  [ERROR] No se pudo cargar season_data.json: {e}")
        return {}

    results = {}
    for game in data.get("games", []):
        # Solo juegos finalizados
        status = game.get("status", {})
        if status.get("abstractGameCode") != "F":
            continue

        gid = str(game.get("game_id", ""))
        if not gid:
            continue

        results[gid] = {
            "game_id": gid,
            "date": game.get("date", ""),
            "game_yrfi": bool(game.get("game_yrfi", False)),
            "home_yrfi": bool(game.get("home_yrfi", False)),
            "away_yrfi": bool(game.get("away_yrfi", False)),
            "home_team_name": game.get("home_team_name", ""),
            "away_team_name": game.get("away_team_name", ""),
        }

    return results


# ─────────────────────────────────────────────
# 2. MERGE Y ENRIQUECIMIENTO
# ─────────────────────────────────────────────

def merge_predictions_results(
    predictions: List[Dict],
    results: Dict[str, Dict],
    decision_threshold: float = DEFAULT_DECISION_THRESHOLD,
) -> List[Dict]:
    """
    Cruza predicciones con resultados reales.
    - Solo incluye predicciones cuyo game_id tiene resultado final.
    - Si hay múltiples predicciones para el mismo juego, usa la más reciente.
    - Añade columnas: predicted_yrfi, actual_yrfi, correct, error_type.
    """
    # Deduplicar: última predicción por game_id
    latest: Dict[str, Dict] = {}
    for p in predictions:
        gid = p["game_id"]
        existing = latest.get(gid)
        if existing is None or p["generated_at"] > existing["generated_at"]:
            latest[gid] = p

    merged = []
    for gid, pred in latest.items():
        result = results.get(gid)
        if result is None:
            continue  # Sin resultado real todavía

        prob = pred["yrfi_probability"]
        predicted_yrfi = prob >= decision_threshold
        actual_yrfi = result["game_yrfi"]
        correct = predicted_yrfi == actual_yrfi

        # Clasificar error
        if correct:
            error_type = "-"
        elif predicted_yrfi and not actual_yrfi:
            error_type = "FP"  # Falso Positivo
        else:
            error_type = "FN"  # Falso Negativo

        # Bucket de confianza
        if prob >= 0.90:
            bucket = "90%+"
        elif prob >= 0.80:
            bucket = "80-89%"
        elif prob >= 0.70:
            bucket = "70-79%"
        elif prob >= 0.60:
            bucket = "60-69%"
        else:
            bucket = "50-59%"

        merged.append({
            **pred,
            "actual_yrfi": actual_yrfi,
            "actual_home_yrfi": result["home_yrfi"],
            "actual_away_yrfi": result["away_yrfi"],
            "predicted_yrfi": predicted_yrfi,
            "correct": correct,
            "error_type": error_type,
            "confidence_bucket": bucket,
        })

    # Ordenar por fecha
    merged.sort(key=lambda x: (x["game_date"], x["game_id"]))
    return merged


# ─────────────────────────────────────────────
# 3. CÁLCULO DE MÉTRICAS
# ─────────────────────────────────────────────

def calculate_global_metrics(merged: List[Dict]) -> Dict:
    """Métricas globales de precisión."""
    n = len(merged)
    if n == 0:
        return {"error": "Sin datos para evaluar"}

    correct = sum(1 for r in merged if r["correct"])
    tp = sum(1 for r in merged if r["predicted_yrfi"] and r["actual_yrfi"])
    fp = sum(1 for r in merged if r["predicted_yrfi"] and not r["actual_yrfi"])
    fn = sum(1 for r in merged if not r["predicted_yrfi"] and r["actual_yrfi"])
    tn = sum(1 for r in merged if not r["predicted_yrfi"] and not r["actual_yrfi"])

    accuracy = correct / n
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    base_yrfi_rate = sum(1 for r in merged if r["actual_yrfi"]) / n
    baseline = max(base_yrfi_rate, 1 - base_yrfi_rate)

    dates = [r["game_date"] for r in merged if r["game_date"]]
    date_range = {
        "start": min(dates) if dates else "",
        "end": max(dates) if dates else "",
    }

    return {
        "total_games": n,
        "date_range": date_range,
        "accuracy": round(accuracy, 4),
        "baseline_accuracy": round(baseline, 4),
        "improvement_over_baseline": round(accuracy - baseline, 4),
        "precision_yrfi": round(precision, 4),
        "recall_yrfi": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {"TP": tp, "FP": fp, "FN": fn, "TN": tn},
        "base_yrfi_rate": round(base_yrfi_rate, 4),
        "passes_gate": accuracy >= PERFORMANCE_GATE,
    }


def calculate_threshold_metrics(merged: List[Dict]) -> List[Dict]:
    """
    Métricas de precisión por umbral de confianza.
    Muestra como se comporta el modelo cuando es más/menos seguro.
    """
    results = []
    for t in THRESHOLDS:
        subset = [r for r in merged if r["yrfi_probability"] >= t]
        n = len(subset)
        if n == 0:
            results.append({
                "threshold": t,
                "label": f">={int(t*100)}%",
                "n_predictions": 0,
                "actual_yrfi_rate": None,
                "accuracy": None,
                "avg_predicted_prob": None,
                "calibration_gap": None,
            })
            continue

        actual_rate = sum(1 for r in subset if r["actual_yrfi"]) / n
        accuracy = sum(1 for r in subset if r["correct"]) / n
        avg_prob = sum(r["yrfi_probability"] for r in subset) / n
        calibration_gap = avg_prob - actual_rate  # + = sobreconfianza, - = subconfianza

        results.append({
            "threshold": t,
            "label": f">={int(t*100)}%",
            "n_predictions": n,
            "actual_yrfi_rate": round(actual_rate, 4),
            "accuracy": round(accuracy, 4),
            "avg_predicted_prob": round(avg_prob, 4),
            "calibration_gap": round(calibration_gap, 4),
        })

    return results


def calculate_brier_score(merged: List[Dict]) -> Dict:
    """
    Brier Score = media de (prob_predicha - resultado_real)^2
    Rango: 0 (perfecto) a 1 (pésimo). Referencia: 0.25 es "no information".
    """
    n = len(merged)
    if n == 0:
        return {}

    bs = sum((r["yrfi_probability"] - (1.0 if r["actual_yrfi"] else 0.0)) ** 2 for r in merged) / n

    # Brier Score de referencia (siempre predecir la tasa base)
    base_rate = sum(1 for r in merged if r["actual_yrfi"]) / n
    bs_baseline = sum((base_rate - (1.0 if r["actual_yrfi"] else 0.0)) ** 2 for r in merged) / n

    return {
        "brier_score": round(bs, 4),
        "brier_baseline": round(bs_baseline, 4),
        "brier_skill": round(1 - bs / bs_baseline, 4) if bs_baseline > 0 else 0.0,
        "alert": bs > 0.30,
    }


def calculate_temporal_trends(merged: List[Dict], window: int = 7) -> List[Dict]:
    """
    Agrupa los resultados por fecha y calcula accuracy acumulada y rolling.
    """
    # Agrupar por fecha
    by_date: Dict[str, List] = defaultdict(list)
    for r in merged:
        by_date[r["game_date"]].append(r)

    sorted_dates = sorted(by_date.keys())
    trends = []
    cumulative_correct = 0
    cumulative_total = 0

    for date in sorted_dates:
        day_games = by_date[date]
        n = len(day_games)
        correct = sum(1 for g in day_games if g["correct"])
        cumulative_correct += correct
        cumulative_total += n

        trends.append({
            "date": date,
            "n_games": n,
            "correct": correct,
            "daily_accuracy": round(correct / n, 4) if n > 0 else None,
            "cumulative_accuracy": round(cumulative_correct / cumulative_total, 4),
        })

    # Rolling window
    for i, entry in enumerate(trends):
        window_start = max(0, i - window + 1)
        window_entries = trends[window_start : i + 1]
        tot = sum(e["n_games"] for e in window_entries)
        cor = sum(e["correct"] for e in window_entries)
        entry[f"rolling_{window}d_accuracy"] = round(cor / tot, 4) if tot > 0 else None

    return trends


def generate_game_level_report(merged: List[Dict]) -> List[Dict]:
    """Tabla partido por partido con resultado de predicción."""
    rows = []
    for r in merged:
        rows.append({
            "game_id": r["game_id"],
            "date": r["game_date"],
            "matchup": f"{r['away_team_name']} @ {r['home_team_name']}",
            "home_pitcher": r.get("home_pitcher", "N/D"),
            "away_pitcher": r.get("away_pitcher", "N/D"),
            "yrfi_prob_%": round(r["yrfi_probability"] * 100, 1),
            "predicted": "YRFI" if r["predicted_yrfi"] else "NRFI",
            "actual": "YRFI" if r["actual_yrfi"] else "NRFI",
            "result": "✓ HIT" if r["correct"] else "✗ MISS",
            "error_type": r["error_type"],
            "confidence_bucket": r["confidence_bucket"],
        })
    return rows


def generate_recommendations(global_metrics: Dict, threshold_metrics: List[Dict], brier: Dict) -> List[str]:
    """Genera recomendaciones automáticas basadas en las métricas."""
    recs = []

    acc = global_metrics.get("accuracy", 0)
    baseline = global_metrics.get("baseline_accuracy", 0)

    if acc < PERFORMANCE_GATE:
        recs.append(
            f"⚠️  Accuracy actual ({acc:.1%}) está por debajo del umbral mínimo ({PERFORMANCE_GATE:.1%}). "
            "Revisar pesos del modelo (base/tendencia/lanzador)."
        )
    elif acc <= baseline + 0.02:
        recs.append(
            "📊 El modelo apenas supera el baseline. Considerar agregar variables: OBP top-of-order, "
            "WHIP del lanzador o factores de estadio (Park Factors)."
        )
    else:
        recs.append(f"✅ Accuracy ({acc:.1%}) supera el baseline ({baseline:.1%}) en {acc-baseline:.1%}.")

    # Calibración por umbrales
    for t in threshold_metrics:
        if t["n_predictions"] < 5:
            continue
        gap = t.get("calibration_gap", 0) or 0
        if gap > 0.10:
            recs.append(
                f"🔴 Sobreconfianza en umbral {t['label']}: el modelo predice {t['avg_predicted_prob']:.1%} "
                f"pero la tasa real es {t['actual_yrfi_rate']:.1%}. "
                "Evaluar reducir el peso del impacto de lanzadores."
            )
        elif gap < -0.10:
            recs.append(
                f"🔵 Subconfianza en umbral {t['label']}: el modelo es más conservador de lo necesario."
            )

    # Brier score
    bs = brier.get("brier_score", 0)
    if bs > 0.30:
        recs.append(
            f"📉 Brier Score alto ({bs:.3f}): las probabilidades están mal calibradas. "
            "El modelo tiende a ser demasiado extremo en sus predicciones."
        )
    elif brier.get("brier_skill", 0) > 0.1:
        recs.append(
            f"🎯 Brier Skill Score positivo ({brier['brier_skill']:.2f}): el modelo supera la predicción naive."
        )

    # FP vs FN
    cm = global_metrics.get("confusion_matrix", {})
    fp = cm.get("FP", 0)
    fn = cm.get("FN", 0)
    if fp > fn * 1.5:
        recs.append(
            f"⚠️  Alta tasa de Falsos Positivos ({fp} FP vs {fn} FN): "
            "el modelo tiende a predecir YRFI con demasiada frecuencia. "
            "Considera elevar el umbral de decisión a 0.60+."
        )
    elif fn > fp * 1.5:
        recs.append(
            f"⚠️  Alta tasa de Falsos Negativos ({fn} FN vs {fp} FP): "
            "el modelo pierde demasiados YRFI reales. "
            "Considera bajar el umbral de decisión."
        )

    return recs


# ─────────────────────────────────────────────
# 4. EXPORTACIÓN DE REPORTES
# ─────────────────────────────────────────────

def export_json_report(report: Dict, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    print(f"  JSON guardado: {output_path.name}")


def export_markdown_report(
    global_metrics: Dict,
    threshold_metrics: List[Dict],
    brier: Dict,
    trends: List[Dict],
    game_rows: List[Dict],
    recommendations: List[str],
    output_path: Path,
) -> None:
    """Genera reporte en Markdown legible."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_range = global_metrics.get("date_range", {})
    acc = global_metrics.get("accuracy", 0)
    n = global_metrics.get("total_games", 0)
    bs = brier.get("brier_score", "N/D")

    md = []
    md.append(f"# ⚾ Reporte de Evaluación YRFI — Feedback Loop")
    md.append(f"\n**Generado:** {now}  ")
    md.append(f"**Período:** {date_range.get('start', '?')} → {date_range.get('end', '?')}  ")
    md.append(f"**Partidos evaluados:** {n}\n")

    # Executive Summary
    gate_icon = "✅" if global_metrics.get("passes_gate") else "❌"
    md.append("## 📊 Resumen Ejecutivo\n")
    md.append("| Métrica | Valor | Estado |")
    md.append("|---------|-------|--------|")
    md.append(f"| Accuracy Global | **{acc:.1%}** | {gate_icon} |")
    md.append(f"| Baseline (naive) | {global_metrics.get('baseline_accuracy', 0):.1%} | - |")
    md.append(f"| Mejora vs Baseline | {global_metrics.get('improvement_over_baseline', 0):+.1%} | - |")
    md.append(f"| Precision (YRFI) | {global_metrics.get('precision_yrfi', 0):.1%} | - |")
    md.append(f"| Recall (YRFI) | {global_metrics.get('recall_yrfi', 0):.1%} | - |")
    md.append(f"| F1-Score | {global_metrics.get('f1_score', 0):.3f} | - |")
    md.append(f"| Brier Score | {bs:.4f} | {'⚠️' if isinstance(bs, float) and bs > 0.30 else '✅'} |")

    cm = global_metrics.get("confusion_matrix", {})
    md.append(f"\n**Matriz de Confusión:** TP={cm.get('TP',0)} | FP={cm.get('FP',0)} | FN={cm.get('FN',0)} | TN={cm.get('TN',0)}\n")

    # Análisis por umbral
    md.append("## 🎯 Precisión por Umbral de Confianza\n")
    md.append("| Umbral | N Predicciones | Accuracy | Tasa YRFI Real | Prob Avg | Calibración |")
    md.append("|--------|----------------|----------|----------------|----------|-------------|")
    for t in threshold_metrics:
        if t["n_predictions"] == 0:
            md.append(f"| {t['label']} | 0 | - | - | - | - |")
            continue
        gap = t.get("calibration_gap", 0) or 0
        cal_icon = "🟢" if abs(gap) <= 0.05 else ("🔴" if gap > 0.10 else "🟡")
        md.append(
            f"| {t['label']} | {t['n_predictions']} | {t['accuracy']:.1%} | "
            f"{t['actual_yrfi_rate']:.1%} | {t['avg_predicted_prob']:.1%} | "
            f"{cal_icon} {gap:+.1%} |"
        )

    # Tendencia reciente (últimos 7 días)
    md.append("\n## 📈 Tendencia Reciente (Últimos 7 días)\n")
    recent = trends[-7:] if len(trends) >= 7 else trends
    md.append("| Fecha | Juegos | Aciertos | Accuracy Diaria | Acum. |")
    md.append("|-------|--------|----------|-----------------|-------|")
    for t in recent:
        daily = f"{t['daily_accuracy']:.1%}" if t.get("daily_accuracy") is not None else "-"
        md.append(
            f"| {t['date']} | {t['n_games']} | {t['correct']} | {daily} | {t['cumulative_accuracy']:.1%} |"
        )

    # Top misses (FP con alta confianza)
    fp_high = sorted(
        [r for r in game_rows if r["error_type"] == "FP"],
        key=lambda x: -x["yrfi_prob_%"]
    )[:5]
    fn_high = sorted(
        [r for r in game_rows if r["error_type"] == "FN"],
        key=lambda x: -x["yrfi_prob_%"]
    )[:5]

    if fp_high:
        md.append("\n## 🔴 Top Falsos Positivos (predije YRFI, fue NRFI)\n")
        md.append("| Fecha | Partido | Prob Predicha | Lanzadores |")
        md.append("|-------|---------|---------------|------------|")
        for r in fp_high:
            md.append(f"| {r['date']} | {r['matchup']} | {r['yrfi_prob_%']}% | {r['away_pitcher']} vs {r['home_pitcher']} |")

    if fn_high:
        md.append("\n## 🔵 Top Falsos Negativos (predije NRFI, fue YRFI)\n")
        md.append("| Fecha | Partido | Prob Predicha | Lanzadores |")
        md.append("|-------|---------|---------------|------------|")
        for r in fn_high:
            md.append(f"| {r['date']} | {r['matchup']} | {r['yrfi_prob_%']}% | {r['away_pitcher']} vs {r['home_pitcher']} |")

    # Recomendaciones
    md.append("\n## 💡 Recomendaciones del Modelo\n")
    for rec in recommendations:
        md.append(f"- {rec}")

    # Tabla detallada
    md.append("\n## 📋 Detalle por Partido\n")
    md.append("| Fecha | Partido | Prob% | Pred | Real | Resultado |")
    md.append("|-------|---------|-------|------|------|-----------|")
    for r in game_rows:
        md.append(
            f"| {r['date']} | {r['matchup']} | {r['yrfi_prob_%']}% | "
            f"{r['predicted']} | {r['actual']} | {r['result']} |"
        )

    md.append(f"\n---\n*Generado automáticamente por evaluate_predictions.py · {now}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"  Markdown guardado: {output_path.name}")


# ─────────────────────────────────────────────
# 5. MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Evalúa la precisión del modelo YRFI")
    parser.add_argument("--umbral", type=float, default=DEFAULT_DECISION_THRESHOLD,
                        help="Umbral de decisión YRFI (default: 0.50)")
    parser.add_argument("--fecha", type=str, default=None,
                        help="Evaluar solo hasta esta fecha YYYY-MM-DD")
    args = parser.parse_args()

    print("=" * 55)
    print("  EVALUATE PREDICTIONS — Feedback Loop YRFI")
    print("=" * 55)

    # 1. Cargar datos
    print("\n[1] Cargando predicciones...")
    predictions = load_predictions()
    if not predictions:
        print("  ❌ Sin predicciones disponibles. Ejecuta generar_pronosticos_jornada.py primero.")
        sys.exit(1)
    print(f"  Predicciones cargadas: {len(predictions)}")

    print("\n[2] Cargando resultados reales del season_data.json...")
    results = load_season_results()
    print(f"  Juegos finalizados disponibles: {len(results)}")

    # Filtrar por fecha si se especificó
    if args.fecha:
        predictions = [p for p in predictions if p["game_date"] <= args.fecha]
        print(f"  Filtrado hasta {args.fecha}: {len(predictions)} predicciones")

    # 3. Merge
    print(f"\n[3] Cruzando predicciones con resultados (umbral={args.umbral:.0%})...")
    merged = merge_predictions_results(predictions, results, decision_threshold=args.umbral)
    print(f"  Predicciones con resultado real: {len(merged)}")

    if len(merged) == 0:
        print("\n  ⚠️  No hay predicciones evaluables aún.")
        print("  Los juegos predichos quizás no han finalizado todavía.")
        sys.exit(0)

    # 4. Calcular métricas
    print("\n[4] Calculando métricas...")
    global_metrics = calculate_global_metrics(merged)
    threshold_metrics = calculate_threshold_metrics(merged)
    brier = calculate_brier_score(merged)
    trends = calculate_temporal_trends(merged)
    game_rows = generate_game_level_report(merged)
    recommendations = generate_recommendations(global_metrics, threshold_metrics, brier)

    # 5. Ensamblar reporte JSON
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report = {
        "generated_at": datetime.now().isoformat(),
        "config": {
            "decision_threshold": args.umbral,
            "performance_gate": PERFORMANCE_GATE,
        },
        "summary": global_metrics,
        "brier_score": brier,
        "threshold_analysis": threshold_metrics,
        "temporal_trends": trends,
        "recommendations": recommendations,
        "game_details": game_rows,
    }

    # 6. Exportar
    print("\n[5] Generando reportes...")
    json_path = REPORTS_DIR / f"evaluation_{timestamp}.json"
    md_path = REPORTS_DIR / f"evaluation_{timestamp}.md"

    export_json_report(report, json_path)
    export_markdown_report(
        global_metrics, threshold_metrics, brier, trends,
        game_rows, recommendations, md_path
    )

    # 7. Resumen en consola
    acc = global_metrics.get("accuracy", 0)
    n = global_metrics.get("total_games", 0)
    baseline = global_metrics.get("baseline_accuracy", 0)
    passes = global_metrics.get("passes_gate", False)
    cm = global_metrics.get("confusion_matrix", {})

    print("\n" + "=" * 55)
    print(f"  {'✅' if passes else '❌'} EVALUACIÓN COMPLETADA")
    print("=" * 55)
    print(f"  Partidos evaluados : {n}")
    print(f"  Accuracy global    : {acc:.1%}")
    print(f"  Baseline (naive)   : {baseline:.1%}")
    print(f"  Mejora             : {acc - baseline:+.1%}")
    print(f"  Brier Score        : {brier.get('brier_score', 'N/D'):.4f}")
    print(f"  TP={cm.get('TP',0)} | FP={cm.get('FP',0)} | FN={cm.get('FN',0)} | TN={cm.get('TN',0)}")
    print("\n  💡 Recomendaciones:")
    for r in recommendations:
        print(f"     {r}")
    print(f"\n  📁 Reportes en: reports/")

    # Exit code para CI/CD
    sys.exit(0 if passes else 1)


if __name__ == "__main__":
    main()
