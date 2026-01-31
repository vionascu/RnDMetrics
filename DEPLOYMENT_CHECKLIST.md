# RnDMetrics - Deployment Checklist

Use this checklist to verify all components are properly configured and ready for production.

## Pre-Deployment Verification

### ✅ Code Changes
- [x] Dashboard tabs added (Metrics Work & Methodology)
- [x] All GitLab references updated to GitHub (50+ URLs)
- [x] GITLAB_TOKEN → GITHUB_TOKEN in all files
- [x] GitLab CI/CD → GitHub Actions workflows
- [x] Documentation updated and complete

### ✅ GitHub Actions Workflows
- [ ] `.github/workflows/metrics.yml` exists and is valid
- [ ] `.github/workflows/pages-build-deployment.yml` exists and is valid
- [ ] Both workflows show in GitHub **Actions** tab
- [ ] Workflows are enabled (green checkmarks)

### ✅ Configuration Files
- [ ] `.github/CODEOWNERS` created
- [ ] `.github/pages-config.yml` created
- [ ] `.github/README.md` created
- [ ] All files are in correct directories

### ✅ Documentation
- [ ] `GITHUB_PAGES_SETUP.md` created
- [ ] `CI_CD_DEPLOYMENT_SUMMARY.md` created
- [ ] `.github/README.md` created
- [ ] `README.md` updated with GitHub Pages section

## Initial Setup Steps

### Step 1: Repository Preparation
- [ ] Commit all changes to main branch
```bash
git add .
git commit -m "Add CI/CD and GitHub Pages configuration"
git push origin main
```

### Step 2: Enable GitHub Pages
1. Go to **GitHub** → **Repository Settings**
2. Scroll to **Pages** section (left sidebar)
3. Under "Build and deployment":
   - [ ] Select **Source**: "GitHub Actions"
   - [ ] Click **Save**
4. Wait 30-60 seconds for settings to apply

### Step 3: Verify GitHub Actions
1. Go to **Actions** tab
2. [ ] Verify 2 workflows are listed:
   - "Collect Metrics & Deploy Dashboard"
   - "Build and deploy to GitHub Pages"
3. [ ] Both show as "Enabled" (green status)

### Step 4: Check Secrets (if needed)
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. [ ] GITHUB_TOKEN should auto-exist (provided by GitHub)
3. [ ] No additional secrets needed for basic setup

## Triggering First Deployment

### Option A: Automatic (Recommended for testing)
1. Go to **Actions** tab
2. [ ] Click "Collect Metrics & Deploy Dashboard"
3. [ ] Click **"Run workflow"** button
4. [ ] Observe workflow execution:
   - Checkout step should complete ✓
   - Python setup should complete ✓
   - Metrics collection should complete ✓
   - Dashboard build should complete ✓
   - GitHub Pages deployment should complete ✓

### Option B: Wait for Scheduled Run
- [ ] Wait until 2 AM UTC (next scheduled run)
- [ ] Check **Actions** tab for automatic execution
- [ ] Verify successful completion

## Verification After Deployment

### ✅ GitHub Pages Active
- [ ] Go to **Settings** → **Pages**
- [ ] Verify **Source** shows "GitHub Actions"
- [ ] Verify **Status** shows "Your site is live at..."
- [ ] Copy the provided URL

### ✅ Dashboard Accessible
1. [ ] Main Dashboard loads: `https://vionascu.github.io/RnDMetrics/`
2. [ ] Executive Dashboard loads: `.../executive.html`
3. [ ] Sitemap loads: `.../sitemap.html`
4. [ ] All tabs accessible on dashboards
5. [ ] No 404 errors

### ✅ Dashboard Content
- [ ] Main metrics visible
- [ ] Project selector works
- [ ] "How Metrics Work" tab displays correctly
- [ ] "Methodology" tab displays correctly
- [ ] Documentation links work
- [ ] All data displays properly

## Performance Validation

### Workflow Execution
- [ ] Total workflow time: 5-10 minutes
- [ ] No failed steps
- [ ] Artifacts created successfully
- [ ] Deployment completed without errors

### Dashboard Performance
- [ ] Page loads in <3 seconds
- [ ] Navigation between tabs smooth
- [ ] Charts and graphs render correctly
- [ ] No console errors (check F12)

## Post-Deployment

### ✅ Team Communication
- [ ] Share dashboard URL with team
- [ ] Send access instructions
- [ ] Explain update frequency (daily at 2 AM UTC)
- [ ] Document how to request manual updates

### ✅ Monitoring Setup
- [ ] [ ] Set reminder to check metrics weekly
- [ ] [ ] Monitor GitHub Actions for failures
- [ ] [ ] Track metrics trends over time
- [ ] [ ] Plan quarterly metric reviews

### ✅ Documentation
- [ ] [ ] Keep GITHUB_PAGES_SETUP.md updated
- [ ] [ ] Document any custom changes
- [ ] [ ] Update dashboard as needed
- [ ] [ ] Archive old documentation versions

## Troubleshooting Checklist

### If Dashboard Shows 404
- [ ] Verify GitHub Pages enabled (Settings → Pages)
- [ ] Wait 2-3 minutes and refresh browser
- [ ] Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- [ ] Check for typos in URL
- [ ] View GitHub Pages source branch

### If Workflow Fails
- [ ] Go to **Actions** → Click failed workflow
- [ ] Expand each job to view logs
- [ ] Look for red error messages
- [ ] Check for:
   - File path errors
   - Missing dependencies
   - Permission issues
- [ ] Re-run workflow after fixing
- [ ] Check `.github/workflows/*.yml` syntax

### If Metrics Not Updating
- [ ] Verify workflow ran successfully (Actions tab)
- [ ] Check GitHub API rate limits
- [ ] Verify `output/latest.json` was generated
- [ ] Manually trigger workflow to test
- [ ] Review workflow logs for errors

## Rollback Procedure

If deployment causes issues:

1. [ ] Disable workflows (Settings → Actions → Disable all)
2. [ ] Revert to previous commit:
```bash
git revert HEAD
git push origin main
```
3. [ ] Delete `.github/workflows/` if needed
4. [ ] Re-enable after fixes applied

## Schedule Configuration

### Default Schedule
- Time: **2 AM UTC** daily
- Cron: `0 2 * * *`

### If Need to Change
1. Edit `.github/workflows/metrics.yml`
2. Find line with cron expression
3. Update to desired schedule:
   - Every 6 hours: `0 */6 * * *`
   - Every 4 hours: `0 */4 * * *`
   - Twice daily: `0 2,14 * * *`
4. Commit and push changes
5. [ ] Verify new schedule in workflow logs

## Final Verification

### All Systems Ready
- [ ] GitHub Pages enabled
- [ ] Workflows active
- [ ] Dashboard accessible
- [ ] Content displays correctly
- [ ] Updates working (manual or scheduled)
- [ ] Documentation complete
- [ ] Team notified

### Production Ready Checklist
- [ ] ✅ All tasks completed
- [ ] ✅ No 404 errors
- [ ] ✅ Dashboards loading properly
- [ ] ✅ Metrics displaying correctly
- [ ] ✅ Workflows executing successfully
- [ ] ✅ Documentation comprehensive
- [ ] ✅ Team has access

---

## Sign-Off

- **Deployment Date:** _________________
- **Deployed By:** _________________
- **Verified By:** _________________

**Status:**
- [ ] All checks passed - READY FOR PRODUCTION
- [ ] Minor issues fixed - READY FOR PRODUCTION
- [ ] Critical issues - HALT DEPLOYMENT

**Notes:**
```




```

---

## Quick Reference

### Important URLs
- **Dashboard:** https://vionascu.github.io/RnDMetrics/
- **GitHub Settings:** https://github.com/vionascu/RnDMetrics/settings
- **Actions:** https://github.com/vionascu/RnDMetrics/actions
- **Pages Settings:** https://github.com/vionascu/RnDMetrics/settings/pages

### Key Files
- Workflows: `.github/workflows/*.yml`
- Setup: `GITHUB_PAGES_SETUP.md`
- Reference: `.github/README.md`
- Summary: `CI_CD_DEPLOYMENT_SUMMARY.md`

### Support Resources
- GitHub Pages Docs: https://docs.github.com/pages
- GitHub Actions Docs: https://docs.github.com/actions
- Workflow Syntax: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions

---

**Created:** January 31, 2026
**Updated:** January 31, 2026
**Status:** Ready for Deployment
