#!/bin/bash
set -e

# Test runner with coverage reporting
# Ensures test suite maintains 80% coverage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  Running Test Suite"
echo "========================================="
echo ""

# Ensure Python virtual environment
if [ ! -f venv/bin/activate ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -q pytest pytest-cov coverage 2>/dev/null || true

echo ""
echo "🧪 Running tests with coverage..."
echo ""

# Run tests with coverage
python -m pytest tests/ \
  --cov=scripts \
  --cov=tools \
  --cov-report=term-missing \
  --cov-report=html:artifacts/coverage_html \
  --cov-report=json:artifacts/coverage.json \
  -v

TEST_EXIT=$?

echo ""
echo "========================================="

if [ $TEST_EXIT -eq 0 ]; then
  echo "  ✅ Tests Passed"
else
  echo "  ❌ Tests Failed"
fi

echo "========================================="
echo ""

# Extract coverage percentage
if [ -f "artifacts/coverage.json" ]; then
  COVERAGE=$(python3 << 'EOF'
import json
with open("artifacts/coverage.json") as f:
    data = json.load(f)
    total_pct = data.get("totals", {}).get("percent_covered", 0)
    print(f"{total_pct:.1f}")
EOF
)

  echo "📊 Coverage: $COVERAGE%"

  if (( $(echo "$COVERAGE >= 80" | bc -l) )); then
    echo "✅ Coverage meets 80% minimum"
  else
    echo "⚠️  Coverage below 80% target ($COVERAGE%)"
    if [ $TEST_EXIT -eq 0 ]; then
      TEST_EXIT=1
    fi
  fi

  echo ""
  echo "📈 Full coverage report: artifacts/coverage_html/index.html"
fi

echo ""

exit $TEST_EXIT
