#!/bin/bash
set -e

# Dashboard builder - copies dashboard files and prepares data for public
# Usage: ./build_dashboard.sh [--artifacts artifacts] [--output public]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default values
ARTIFACTS_DIR="artifacts"
OUTPUT_DIR="public"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --artifacts)
      ARTIFACTS_DIR="$2"
      shift 2
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

echo "========================================="
echo "  Building Dashboard"
echo "========================================="
echo ""
echo "Input:  $ARTIFACTS_DIR/"
echo "Output: $OUTPUT_DIR/"
echo ""

# Ensure output directory
mkdir -p "$OUTPUT_DIR"

# Check for required files
if [ ! -f "$ARTIFACTS_DIR/manifest.json" ]; then
  echo "❌ Manifest not found: $ARTIFACTS_DIR/manifest.json"
  echo "   Run ./run_metrics.sh first"
  exit 1
fi

if [ ! -d "$ARTIFACTS_DIR/derived" ]; then
  echo "❌ Derived metrics directory not found: $ARTIFACTS_DIR/derived/"
  exit 1
fi

echo "📊 Preparing dashboard data..."

# Copy manifest
cp "$ARTIFACTS_DIR/manifest.json" "$OUTPUT_DIR/"

# Copy epic coverage
if [ -f "$ARTIFACTS_DIR/raw/epic_coverage.json" ]; then
  cp "$ARTIFACTS_DIR/raw/epic_coverage.json" "$OUTPUT_DIR/"
fi

# Copy history if available
if [ -f "output/history.json" ]; then
  cp output/history.json "$OUTPUT_DIR/"
fi

# Generate derived metrics JSON
python3 << 'METRICS_EOF'
import json
from pathlib import Path
import sys

artifacts_path = Path(sys.argv[1] if len(sys.argv) > 1 else "artifacts")
output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "public")

all_metrics = {}
for derived_file in (artifacts_path / "derived").glob("*_derived.json"):
    try:
        with open(derived_file) as f:
            data = json.load(f)
            dimension = data.get("dimension", "unknown")
            metrics = data.get("metrics", {})
            for metric_id, metric_data in metrics.items():
                # Preserve all fields from the metric
                all_metrics[metric_id] = {
                    "dimension": dimension,
                    **metric_data  # Include all original fields
                }
    except Exception as e:
        print(f"Warning: Could not process {derived_file}: {e}", file=sys.stderr)

output_file = output_path / "derived-metrics.json"
with open(output_file, 'w') as f:
    json.dump(all_metrics, f, indent=2)

print(f"Generated {output_file}")

METRICS_EOF

echo ""
echo "========================================="
echo "  ✅ Dashboard Ready"
echo "========================================="
echo ""
echo "📍 Output:"
echo "   Location: $OUTPUT_DIR/index.html"
echo "   Data files:"
echo "   • $OUTPUT_DIR/manifest.json"
echo "   • $OUTPUT_DIR/history.json"
echo "   • $OUTPUT_DIR/derived-metrics.json"
echo ""
