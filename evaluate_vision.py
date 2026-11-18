import argparse
import csv
import json
from pathlib import Path
import anthropic
import pandas as pd
from image_recognition import CONFIDENCE_RANK, build_vocabulary, detect_ingredients

TEST_DIR = Path("data/vision_test")
LABELS_FILE = TEST_DIR / "labels.csv"
RAW_FILE = TEST_DIR / "raw_results.json"
REPORT_FILE = TEST_DIR / "results_by_photo.csv"
CUTOFFS = ["high", "medium", "low"]

def safe_div(a, b):
    return a / b if b else 0.0

def load_labels(vocabulary):
    labels = {}
    with open(LABELS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            filename = row["filename"].strip()
            names = {n.strip().lower() for n in row["ingredients"].split(";") if n.strip()}
            unknown = names - set(vocabulary)
            if unknown:
                print(f"Warning: unknown ingredients in {filename}: {unknown}")
            labels[filename] = names
    return labels

def run_detection(labels, vocabulary):
    client = anthropic.Anthropic()
    raw = {}
    for filename in labels:
        path = TEST_DIR / filename
        if not path.exists():
            print(f"Warning: file not found: {path}")
            continue
        print(f"Detecting ingredients in {filename}...")
        try:
            found = detect_ingredients(path.read_bytes(), vocabulary, client=client, min_confidence="low")
        except anthropic.AnthropicError as e:
            print(f"  Failed: {e}")
            continue
        raw[filename] = [{"name": d.name, "confidence": d.confidence} for d in found]
    if raw:
        RAW_FILE.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        print(f"Raw results written to {RAW_FILE}")
    return raw

def score(labels, raw, cutoff):
    rows = []
    total_correct = total_detected = total_actual = 0
    for filename, detections in raw.items():
        if filename not in labels:
            continue
        actual = labels[filename]
        detected = {d["name"] for d in detections if CONFIDENCE_RANK[d["confidence"]] >= CONFIDENCE_RANK[cutoff]}
        correct = actual & detected
        rows.append({
            "filename": filename,
            "cutoff": cutoff,
            "precision": round(safe_div(len(correct), len(detected)), 2),
            "recall": round(safe_div(len(correct), len(actual)), 2),
            "correct": ";".join(sorted(correct)),
            "wrong": ";".join(sorted(detected - actual)),
            "missed": ";".join(sorted(actual - detected)),
        })
        total_correct += len(correct)
        total_detected += len(detected)
        total_actual += len(actual)

    precision = safe_div(total_correct, total_detected)
    recall = safe_div(total_correct, total_actual)
    f1 = safe_div(2 * precision * recall, precision + recall)
    return rows, precision, recall, f1

def main():
    parser = argparse.ArgumentParser(description="Evaluate ingredient detection accuracy")
    parser.add_argument("--rescore", action="store_true", help="score saved results without calling the API")
    args = parser.parse_args()
    recipes = pd.read_csv("data/recipes_cleaned.csv").fillna("")
    vocabulary = build_vocabulary(recipes)
    labels = load_labels(vocabulary)
    if args.rescore:
        if not RAW_FILE.exists():
            print(f"Error: raw results file not found: {RAW_FILE}")
            return
        raw = json.loads(RAW_FILE.read_text(encoding="utf-8"))
    else:
        raw = run_detection(labels, vocabulary)
    if not raw:
        print("No results to score.")
        return

    print(f"\nEvaluated {len(raw)} photos\n")
    print(f"{'Cutoff':<8}{'Precision':>10}{'Recall':>8}{'F1':>8}")
    all_rows = []
    for cutoff in CUTOFFS:
        rows, precision, recall, f1 = score(labels, raw, cutoff)
        all_rows.extend(rows)
        print(f"{cutoff:<8}{precision:>10.2f}{recall:>8.2f}{f1:>8.2f}")
    pd.DataFrame(all_rows).to_csv(REPORT_FILE, index=False)
    print(f"\nPer-photo results written to {REPORT_FILE}")

if __name__ == "__main__":
    main()