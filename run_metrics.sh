#!/bin/bash
set -e

# Evidence-backed metrics system - one-command entry point
# Usage:
#   ./run_metrics.sh --range last_30_days
#   ./run_metrics.sh --range all_2024
#   ./run_metrics.sh --range custom --from 2026-01-01 --to 2026-01-31
#   ./run_metrics.sh --range custom --from 2026-01-01 --to 2026-01-31 --open

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 0: Setup projects from projects.json
echo "📁 Setting up projects from projects.json..."
python3 scripts/setup_projects.py || exit 1
echo ""

# Default values
RANGE="last_30_days"
FROM_DATE=""
TO_DATE=""
OPEN_REPORT=0

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --range)
      RANGE="$2"
      shift 2
      ;;
    --from)
      FROM_DATE="$2"
      shift 2
      ;;
    --to)
      TO_DATE="$2"
      shift 2
      ;;
    --open)
      OPEN_REPORT=1
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

echo "========================================="
echo "  Evidence-Backed Metrics System"
echo "========================================="
echo ""
echo "Range:     $RANGE"
[ -n "$FROM_DATE" ] && echo "From:      $FROM_DATE"
[ -n "$TO_DATE" ] && echo "To:        $TO_DATE"
echo ""

# Ensure Python is available
if ! command -v python3 &> /dev/null; then
  echo "❌ Python 3 not found"
  exit 1
fi

# Install dependencies if needed
if [ ! -f venv/bin/activate ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -q pyyaml 2>/dev/null || true

# Step 1a: Collect test and epic artifacts
echo "📦 Collecting test and epic artifacts..."
echo ""

python3 scripts/run_tests.py

if [ $? -ne 0 ]; then
  echo ""
  echo "⚠️  Test artifact collection had issues (may continue if some tests not available)"
fi

echo ""

# Step 1a-bis: Parse epic/US coverage from test files
echo "📊 Parsing epic and user story coverage..."
echo ""

python3 scripts/parse_epic_coverage.py

echo ""

# Step 1b: Run collection
echo "🔍 Running metrics collection..."
echo ""

python3 scripts/collect_metrics.py \
  --range "$RANGE" \
  --from "$FROM_DATE" \
  --to "$TO_DATE" \
  --config config/repos.yaml

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Metrics collection failed"
  exit 1
fi

echo ""
echo "========================================="
echo "  ✅ Metrics Collection Complete"
echo "========================================="
echo ""

# Step 2: Compute derived metrics
echo "📊 Computing derived metrics..."
echo ""

python3 scripts/compute_derived.py artifacts/

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Derived metrics computation failed"
  exit 1
fi

echo ""
echo "========================================="
echo "  Running Quality Gates..."
echo "========================================="
echo ""

python3 tools/quality_gate.py --artifacts artifacts --config config/repos.yaml

if [ $? -ne 0 ]; then
  echo ""
  echo "⚠️  Quality gates flagged issues"
  echo "    Review artifacts/manifest.json for details"
  exit 1
fi

echo ""
echo "========================================="
echo "  ✅ Pipeline Complete"
echo "========================================="
echo ""
echo "📊 Artifacts location:"
echo "   Raw data:       artifacts/raw/"
echo "   Derived data:   artifacts/derived/"
echo "   Manifest:       artifacts/manifest.json"
echo ""
echo "📖 Next steps:"
echo "   1. Review artifacts/manifest.json for full evidence trail"
echo "   2. Check artifacts/derived/ for computed metrics"
echo "   3. Build dashboard: ./build_dashboard.sh (coming soon)"
echo ""
