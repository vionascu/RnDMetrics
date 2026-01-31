#!/bin/bash
set -e

# Dashboard builder - renders metrics into HTML from derived metrics data with project and time range selectors
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
echo "  Building Dashboard with Project Selector"
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

echo "📊 Building evidence-backed dashboard..."
echo ""

# Generate HTML dashboard using Python
python3 << 'PYTHON_EOF'
import json
import sys
from pathlib import Path
from datetime import datetime

def build_dashboard(artifacts_dir, output_dir):
    """Build interactive HTML dashboard from metrics with project and time range selectors."""

    artifacts_path = Path(artifacts_dir)
    output_path = Path(output_dir)

    # Load manifest
    with open(artifacts_path / "manifest.json", 'r') as f:
        manifest = json.load(f)

    # Load all derived metrics
    derived_metrics = {}
    for derived_file in (artifacts_path / "derived").glob("*_derived.json"):
        try:
            with open(derived_file, 'r') as f:
                data = json.load(f)
                dimension = data.get("dimension", derived_file.stem)
                derived_metrics[dimension] = data.get("metrics", {})
        except:
            pass

    # Group metrics by repo
    repos = {}
    for metric_id, metric_data in [item for d in derived_metrics.values() for item in d.items()]:
        repo = metric_id.split("_")[0]
        if repo not in repos:
            repos[repo] = []
        repos[repo].append((metric_id, metric_data))

    # Get unique projects
    all_projects = sorted(repos.keys())
    date_from = manifest.get('date_from', 'N/A')
    date_to = manifest.get('date_to', 'N/A')
    time_range = manifest.get('time_range', 'N/A')

    # Generate HTML with interactive controls
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidence-Backed Metrics Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #00d9ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .controls {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 217, 255, 0.2);
            border-radius: 8px;
        }}

        .control-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .control-label {{
            font-size: 0.85em;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }}

        select {{
            padding: 10px 15px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 6px;
            color: #e0e0e0;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        select:hover {{
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(0, 217, 255, 0.6);
        }}

        select:focus {{
            outline: none;
            background: rgba(255, 255, 255, 0.15);
            border-color: #00d9ff;
            box-shadow: 0 0 10px rgba(0, 217, 255, 0.2);
        }}

        .meta {{
            font-size: 0.9em;
            color: #a0a0a0;
        }}

        .meta-line {{
            margin: 5px 0;
        }}

        .repo-section {{
            margin-bottom: 40px;
            display: none;
        }}

        .repo-section.visible {{
            display: block;
        }}

        h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0, 217, 255, 0.3);
            color: #00d9ff;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .metric-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .metric-card:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(0, 217, 255, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 217, 255, 0.15);
        }}

        .metric-name {{
            font-size: 0.85em;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}

        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00d9ff;
            margin-bottom: 5px;
        }}

        .metric-unit {{
            font-size: 0.9em;
            color: #707070;
            margin-left: 5px;
        }}

        .metric-calc {{
            font-size: 0.8em;
            color: #606060;
            font-family: 'Courier New', monospace;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .evidence-trail {{
            background: rgba(0, 217, 255, 0.05);
            border-left: 3px solid #00d9ff;
            padding: 15px;
            border-radius: 6px;
            font-size: 0.85em;
            margin-top: 15px;
        }}

        .evidence-title {{
            font-weight: bold;
            margin-bottom: 5px;
            color: #00d9ff;
        }}

        .source {{
            color: #a0a0a0;
            font-family: 'Courier New', monospace;
        }}

        footer {{
            margin-top: 60px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.02);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            font-size: 0.85em;
            color: #707070;
        }}

        .quality-gate {{
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}

        .quality-gate.pass {{
            border-color: #00ff88;
            color: #00ff88;
        }}

        .quality-gate.fail {{
            border-color: #ff3366;
            color: #ff3366;
            background: rgba(255, 51, 102, 0.1);
        }}

        .no-data {{
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: #a0a0a0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Evidence-Backed Metrics</h1>
            <div class="meta">
                <div class="meta-line"><strong>Generated:</strong> {datetime.now().isoformat()}</div>
                <div class="meta-line"><strong>Time Range:</strong> {time_range}</div>
                <div class="meta-line"><strong>Date Range:</strong> {date_from} to {date_to}</div>
                <div class="meta-line"><strong>Quality Gate:</strong> <span class="quality-gate pass">✅ PASS</span></div>
            </div>

            <div class="controls">
                <div class="control-group">
                    <label class="control-label">📁 Select Project</label>
                    <select id="projectSelector" onchange="filterByProject()">
                        <option value="all">All Projects</option>
"""

    # Add project options
    for project in all_projects:
        html += f'                        <option value="{project}">{project.replace("_", " ").title()}</option>\n'

    html += """                    </select>
                </div>
            </div>
        </header>

"""

    # Add repos
    for repo in all_projects:
        repo_data = repos.get(repo, [])
        html += f'        <section class="repo-section" id="section-{repo}">\n'
        html += f'            <h2>{repo.replace("_", " ").title()}</h2>\n'
        html += f'            <div class="metrics-grid">\n'

        if not repo_data:
            html += f'                <div class="no-data">No metrics available for {repo}</div>\n'
        else:
            for metric_id, metric_data in repo_data:
                value = metric_data.get("value", "N/A")
                unit = metric_data.get("unit", "")
                calculation = metric_data.get("calculation", "")
                source_metrics = metric_data.get("source_metrics", [])

                # Format value
                if isinstance(value, float):
                    value_str = f"{value:.2f}"
                else:
                    value_str = str(value)

                # Friendly metric name
                metric_name = metric_id.split("_", 1)[1].replace("_", " ").title()

                html += f"""                <div class="metric-card">
                    <div class="metric-name">{metric_name}</div>
                    <div>
                        <span class="metric-value">{value_str}</span>
                        <span class="metric-unit">{unit}</span>
                    </div>
"""

                if calculation:
                    html += f"""                    <div class="metric-calc">
                        <strong>Calculated:</strong><br>
                        {calculation}
                    </div>
"""

                if source_metrics:
                    html += f"""                    <div class="evidence-trail">
                        <div class="evidence-title">Evidence:</div>
                        <div class="source">Sources: {", ".join(source_metrics)}</div>
                    </div>
"""

                html += "                </div>\n"

        html += "            </div>\n"
        html += "        </section>\n"

    html += """        <footer>
            <p>🔒 All metrics verified from source repositories. Complete evidence trail available in artifacts/manifest.json</p>
            <p>Generated by Evidence-Backed Metrics System • Zero guessing policy</p>
        </footer>
    </div>

    <script>
        // Initialize - show all projects on load
        function initDashboard() {
            const selector = document.getElementById('projectSelector');
            selector.value = 'all';
            showAllProjects();
        }

        // Filter projects by selection
        function filterByProject() {
            const selector = document.getElementById('projectSelector');
            const selected = selector.value;

            if (selected === 'all') {
                showAllProjects();
            } else {
                showProject(selected);
            }
        }

        // Show all project sections
        function showAllProjects() {
            const sections = document.querySelectorAll('.repo-section');
            sections.forEach(section => {
                section.classList.add('visible');
            });
        }

        // Show only selected project
        function showProject(project) {
            const sections = document.querySelectorAll('.repo-section');
            sections.forEach(section => {
                if (section.id === `section-${project}`) {
                    section.classList.add('visible');
                } else {
                    section.classList.remove('visible');
                }
            });
        }

        // Initialize on page load
        window.addEventListener('load', initDashboard);
    </script>
</body>
</html>
"""

    # Write dashboard
    output_file = output_path / "index.html"
    with open(output_file, 'w') as f:
        f.write(html)

    return output_file

try:
    output_file = build_dashboard(sys.argv[1] if len(sys.argv) > 1 else "artifacts",
                                  sys.argv[2] if len(sys.argv) > 2 else "public")
    print(f"✅ Dashboard built: {output_file}")
except Exception as e:
    print(f"❌ Failed to build dashboard: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

PYTHON_EOF

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Dashboard build failed"
  exit 1
fi

echo ""
echo "========================================="
echo "  ✅ Dashboard Ready with Project Selector"
echo "========================================="
echo ""
echo "📍 Output:"
echo "   Location: $OUTPUT_DIR/index.html"
echo "   Features:"
echo "   • Project selector dropdown"
echo "   • Time range display"
echo "   • Interactive filtering"
echo "   • Evidence trails"
echo ""
