# GitHub Pages Setup Guide

This guide explains how to enable and configure GitHub Pages for RnDMetrics dashboard.

## Quick Start (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your RnDMetrics repository on GitHub
2. Click **Settings** (gear icon)
3. Scroll to **Pages** section (left sidebar)
4. Under "Build and deployment":
   - **Source:** Select **GitHub Actions**
   - This tells GitHub to use the workflows we've created

### Step 2: Verify Workflows

1. Click **Actions** tab
2. Look for **"Collect Metrics & Deploy Dashboard"** and **"Build and deploy to GitHub Pages"**
3. Both should show as enabled (green checkmark)

### Step 3: Trigger First Deployment

Option A - Automatic (Wait for 2 AM UTC):
- Workflows run automatically on schedule

Option B - Manual (Immediate):
1. Go to **Actions** tab
2. Click **"Collect Metrics & Deploy Dashboard"**
3. Click **"Run workflow"** button
4. Select branch: **main**
5. Click **"Run workflow"**

### Step 4: Monitor Deployment

1. Go to **Actions** tab
2. Watch the workflow run in real-time
3. When complete, check status:
   - ✅ Green = Success
   - ❌ Red = Failed

### Step 5: Access Dashboard

After successful deployment (1-2 minutes):

**Dashboard URLs:**
- Main Dashboard: `https://vionascu.github.io/RnDMetrics/`
- Executive Dashboard: `https://vionascu.github.io/RnDMetrics/executive.html`
- Sitemap: `https://vionascu.github.io/RnDMetrics/sitemap.html`

## Configuration

### Change Update Schedule

Edit `.github/workflows/metrics.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Change this line
```

**Common schedules:**
- Every 6 hours: `'0 */6 * * *'`
- Twice daily (2 AM & 2 PM): `'0 2,14 * * *'`
- Weekly Monday 9 AM: `'0 9 * * 1'`

[Cron help](https://crontab.guru/) - Visual cron editor

### Customize Dashboard URLs

The workflow creates a landing page at:
- `https://vionascu.github.io/RnDMetrics/`

To customize landing page content, edit:
- `.github/workflows/metrics.yml` - Search for `<body>` section
- Or replace `public/index.html` in workflow

## Troubleshooting

### Dashboard Shows "404 Not Found"

**Cause:** GitHub Pages not fully deployed yet

**Solution:**
1. Wait 2-3 minutes after workflow completes
2. Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
3. Check Actions tab for any errors

### Workflow Shows "Failed" Status

**Check these in order:**

1. **View logs:**
   - Click workflow run name
   - Expand job sections
   - Look for red error messages

2. **Common issues:**
   - Missing `.github/workflows/metrics.yml` - Ensure file exists
   - Python dependency issues - Check output logs
   - File permission errors - Check file paths in workflow

3. **Fix & retry:**
   - Go to Actions
   - Click **"Run workflow"** again

### Dashboard Files Not Updated

**Cause:** Workflow runs but doesn't update dashboard content

**Solutions:**
1. Manually push changes to trigger rebuild:
   ```bash
   git add docs/
   git commit -m "Update dashboard"
   git push origin main
   ```

2. Or trigger workflow manually:
   - Go to **Actions** → **Collect Metrics & Deploy Dashboard**
   - Click **"Run workflow"**

### Pages Not Configured

**Error:** "GitHub Pages is currently disabled"

**Fix:**
1. Go to **Settings** → **Pages**
2. Under "Build and deployment":
   - Set **Source** to **GitHub Actions**
   - Save

## Advanced Configuration

### Deploy from `docs/` Folder

If you prefer GitHub Pages to use the `docs/` folder instead of Actions:

1. Go to **Settings** → **Pages**
2. Set **Source** to: **Deploy from a branch**
3. Set **Branch** to: **main** and folder: **/(root)**
4. Note: This won't auto-update metrics

### Custom Domain

To use a custom domain (e.g., `metrics.example.com`):

1. Go to **Settings** → **Pages**
2. Under "Custom domain", enter your domain
3. Add DNS records to your domain provider
4. GitHub will verify and enable HTTPS

### Disable Workflows

To temporarily disable automated deployments:

1. Go to **Settings** → **Actions** → **General**
2. Under "Actions permissions":
   - Select: **Disable all**

## Performance & Monitoring

### View Workflow Duration

1. Go to **Actions** tab
2. Click workflow run name
3. See "Total duration" at top

**Expected times:**
- Metrics collection: 2-5 minutes
- Dashboard build: 1-2 minutes
- Deployment: <1 minute
- **Total: 5-10 minutes**

### Workflow Quota Usage

1. Go to **Settings** → **Billing and plans**
2. View "Actions usage"
3. Free tier: 2,000 minutes/month

**At daily collection (~8 min/run):**
- 30 runs/month × 8 min = 240 minutes/month ✅ (Well under limit)

## Next Steps

After successful deployment:

1. **Share dashboard URL** with team
2. **Monitor metrics** in Executive Dashboard
3. **Customize** dashboard templates in `docs/dashboard*.html`
4. **Integrate** with other workflows or tools
5. **Review** metrics weekly/monthly for trends

## Support & Help

- **View workflow errors:** Go to Actions → Click failed run → Expand logs
- **GitHub Pages docs:** https://docs.github.com/pages
- **GitHub Actions docs:** https://docs.github.com/actions
- **Cron syntax help:** https://crontab.guru/

---

**Dashboard Status:** ✅ Ready for deployment

**Quick Command:**
```bash
# After setup, manually trigger metrics collection anytime:
# Go to GitHub → Actions → "Collect Metrics & Deploy Dashboard" → Run workflow
```

**Last Updated:** January 31, 2026
