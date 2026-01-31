/**
 * Project Selector Component
 * Allows filtering and viewing metrics for single, multiple, or all projects
 *
 * Usage:
 * <div id="project-selector"></div>
 * <script src="project-selector.js"></script>
 * <script>
 *   const selector = new ProjectSelector('project-selector', {
 *     projects: [
 *       { id: 'trailequip', name: 'TrailEquip', color: '#007bff' },
 *       { id: 'trailwaze', name: 'TrailWaze', color: '#28a745' },
 *       { id: 'rndmetrics', name: 'RnDMetrics', color: '#6f42c1' }
 *     ],
 *     onSelectionChange: handleSelectionChange
 *   });
 * </script>
 */

class ProjectSelector {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.projects = options.projects || [];
    this.onSelectionChange = options.onSelectionChange || (() => {});
    this.selectedProjects = new Set(this.projects.map(p => p.id));
    this.viewMode = 'all'; // 'single', 'multiple', 'all'

    this.render();
    this.setupEventListeners();
  }

  render() {
    const html = `
      <div class="project-selector">
        <!-- Header -->
        <div class="ps-header">
          <h3 class="ps-title">
            <svg class="ps-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <circle cx="12" cy="12" r="3"></circle>
              <circle cx="12" cy="1" r="1.5" opacity="0.3"></circle>
              <circle cx="20.5" cy="12" r="1.5" opacity="0.3"></circle>
              <circle cx="12" cy="23" r="1.5" opacity="0.3"></circle>
              <circle cx="3.5" cy="12" r="1.5" opacity="0.3"></circle>
            </svg>
            Project Selector
          </h3>
          <p class="ps-description">Select projects to view and compare metrics</p>
        </div>

        <!-- View Mode Selector -->
        <div class="ps-view-modes">
          <label class="ps-mode-label">
            <input type="radio" name="view-mode" value="single" class="ps-mode-radio">
            <span class="ps-mode-text">Single Project</span>
          </label>
          <label class="ps-mode-label">
            <input type="radio" name="view-mode" value="multiple" class="ps-mode-radio">
            <span class="ps-mode-text">Multiple Projects</span>
          </label>
          <label class="ps-mode-label">
            <input type="radio" name="view-mode" value="all" class="ps-mode-radio" checked>
            <span class="ps-mode-text">All Projects</span>
          </label>
        </div>

        <!-- Project Checkboxes -->
        <div class="ps-projects">
          ${this.projects.map(project => `
            <label class="ps-project-item">
              <input
                type="checkbox"
                class="ps-project-checkbox"
                data-project-id="${project.id}"
                checked
              >
              <span class="ps-project-indicator" style="background-color: ${project.color}"></span>
              <span class="ps-project-name">${project.name}</span>
              <span class="ps-project-status">Active</span>
            </label>
          `).join('')}
        </div>

        <!-- Quick Selection -->
        <div class="ps-quick-actions">
          <button class="ps-btn ps-btn-primary" id="ps-select-all">
            Select All
          </button>
          <button class="ps-btn ps-btn-secondary" id="ps-deselect-all">
            Deselect All
          </button>
          <button class="ps-btn ps-btn-reset" id="ps-reset">
            Reset to Default
          </button>
        </div>

        <!-- Statistics -->
        <div class="ps-stats">
          <div class="ps-stat">
            <span class="ps-stat-label">Projects Selected:</span>
            <span class="ps-stat-value" id="ps-count">3 / 3</span>
          </div>
          <div class="ps-stat">
            <span class="ps-stat-label">View Mode:</span>
            <span class="ps-stat-value" id="ps-mode">All Projects</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="ps-actions">
          <button class="ps-btn ps-btn-success" id="ps-apply">
            <span class="ps-btn-icon">✓</span>
            Apply Selection
          </button>
          <button class="ps-btn ps-btn-outline" id="ps-cancel">
            Cancel
          </button>
        </div>

        <!-- Info Box -->
        <div class="ps-info">
          <strong>💡 Tip:</strong> Select projects to customize your metrics view.
          Compare metrics across projects to identify trends and optimize performance.
        </div>
      </div>
    `;

    this.container.innerHTML = html;
  }

  setupEventListeners() {
    // View mode selection
    document.querySelectorAll('input[name="view-mode"]').forEach(radio => {
      radio.addEventListener('change', (e) => this.handleViewModeChange(e.target.value));
    });

    // Project checkboxes
    document.querySelectorAll('.ps-project-checkbox').forEach(checkbox => {
      checkbox.addEventListener('change', () => this.handleProjectChange());
    });

    // Quick actions
    document.getElementById('ps-select-all').addEventListener('click', () => this.selectAll());
    document.getElementById('ps-deselect-all').addEventListener('click', () => this.deselectAll());
    document.getElementById('ps-reset').addEventListener('click', () => this.reset());

    // Main actions
    document.getElementById('ps-apply').addEventListener('click', () => this.apply());
    document.getElementById('ps-cancel').addEventListener('click', () => this.cancel());
  }

  handleViewModeChange(mode) {
    this.viewMode = mode;
    this.updateUI();

    // Update mode display
    const modeText = {
      single: 'Single Project',
      multiple: 'Multiple Projects',
      all: 'All Projects'
    };
    document.getElementById('ps-mode').textContent = modeText[mode];
  }

  handleProjectChange() {
    this.updateSelectedProjects();
    this.updateUI();
  }

  updateSelectedProjects() {
    this.selectedProjects.clear();
    document.querySelectorAll('.ps-project-checkbox:checked').forEach(checkbox => {
      this.selectedProjects.add(checkbox.dataset.projectId);
    });
  }

  updateUI() {
    const selected = this.selectedProjects.size;
    const total = this.projects.length;
    document.getElementById('ps-count').textContent = `${selected} / ${total}`;

    // Enforce single project mode
    if (this.viewMode === 'single' && this.selectedProjects.size > 1) {
      const firstSelected = Array.from(this.selectedProjects)[0];
      this.selectedProjects.clear();
      this.selectedProjects.add(firstSelected);
      this.updateCheckboxes();
    }
  }

  updateCheckboxes() {
    document.querySelectorAll('.ps-project-checkbox').forEach(checkbox => {
      checkbox.checked = this.selectedProjects.has(checkbox.dataset.projectId);
    });
  }

  selectAll() {
    this.projects.forEach(p => this.selectedProjects.add(p.id));
    this.updateCheckboxes();
    this.updateUI();
  }

  deselectAll() {
    this.selectedProjects.clear();
    this.updateCheckboxes();
    this.updateUI();
  }

  reset() {
    this.selectedProjects = new Set(this.projects.map(p => p.id));
    this.viewMode = 'all';
    document.querySelector('input[value="all"]').checked = true;
    this.updateCheckboxes();
    this.updateUI();
    document.getElementById('ps-mode').textContent = 'All Projects';
  }

  apply() {
    const selected = Array.from(this.selectedProjects);

    if (selected.length === 0) {
      alert('Please select at least one project');
      return;
    }

    this.onSelectionChange({
      projects: selected,
      mode: this.viewMode,
      selectedCount: selected.length,
      totalCount: this.projects.length
    });
  }

  cancel() {
    this.reset();
  }

  getSelectedProjects() {
    return Array.from(this.selectedProjects);
  }

  getViewMode() {
    return this.viewMode;
  }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProjectSelector;
}
