# How This GitHub Profile is Built & Deployed

This repository powers your GitHub profile (`github.com/ravishu5`). It is built using the same architecture and aesthetic standards as [maziyarpanahi/maziyarpanahi](https://github.com/maziyarpanahi/maziyarpanahi).

---

## 🏗️ Architecture Overview

| File / Path | Generated? | Description |
| :--- | :---: | :--- |
| `README.md` | Partly | Hand-crafted profile, with the dynamic table auto-synced |
| `assets/header.svg` | Yes | Self-hosted dark-mode banner rebuilt with live metrics |
| `assets/github.svg` | Yes | Self-hosted GitHub stats card (immune to third-party rate limits) |
| `metrics/github.json` | Yes | Cached JSON metrics pulled via GitHub GraphQL API |
| `scripts/make_github_card.py` | No | Fetches GraphQL stats → generates `assets/github.svg` |
| `scripts/make_header.py` | No | Generates `assets/header.svg` with matching typography & warm palette |
| `scripts/render_readme.py` | No | Injects latest numbers into `README.md` |
| `.github/workflows/profile.yml`| No | GitHub Actions workflow that runs daily and generates the snake |

---

## 🚀 Quick Start: Deploying to Your GitHub Profile

Since your profile repository is `ravishu5/ravishu5`, here are the steps to push and activate it:

### Step 1: Create the Special Repository on GitHub
If you haven't created the repository `ravishu5` yet:
1. Open GitHub and create a new repository named **`ravishu5`** (matching your username).
2. Set it to **Public**.
3. Do **NOT** initialize with a README, .gitignore, or license (we already have everything here).

*(Alternatively, use GitHub CLI: `gh repo create ravishu5 --public --source=. --remote=origin`)*

### Step 2: Initialize Git and Push
In this project folder:
```bash
git init
git add .
git commit -m "feat: initial profile setup with dynamic banners and cards"
git branch -M main
git remote add origin https://github.com/ravishu5/ravishu5.git
git push -u origin main
```

### Step 3: Enable GitHub Actions Workflow Permissions
For the daily cron and contribution snake to commit and push changes back:
1. Go to your repo on GitHub: `https://github.com/ravishu5/ravishu5/settings/actions`
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"**.
5. Click **Save**.

### Step 4: Run the Workflow Once
1. Go to **Actions** → click **Profile** on the left menu.
2. Click **Run workflow** → select branch `main` → click **Run workflow**.
3. Once completed:
   - Your statistics card and header will refresh.
   - An `output` branch will be automatically created containing the snake animation SVGs (`github-snake.svg` and `github-snake-dark.svg`).
   - The snake image on your profile will instantly light up!

---

## 🎨 How to Customize

### 1. Header Banner Text & Appearance
Open `scripts/make_header.py` and modify the constants at the top:
```python
NAME = "Ravi Shankar"
ROLE = "Senior AI Engineer"
TAGLINE = "React · Kotlin · Node · AI Architectures"

# Color Palette:
INK = "#f5ece1"    # Main text & high-contrast numbers
MUTED = "#cbbdad"  # Subtitle / labels
GOLD = "#f7ddb4"   # Accent underlines & glows
RULE = "#4a3c31"   # Card borders
```
Then re-run:
```bash
python3 scripts/make_header.py
```

### 2. Social Badges & Links
In `README.md`, update any badge links (LinkedIn username, website, email, Twitter/X) in the `<p align="center">` badge block.

### 3. Dynamic Stats Block
Everything between:
```markdown
<!-- DYNAMIC-STATS:START -->
<!-- DYNAMIC-STATS:END -->
```
is refreshed automatically by `scripts/render_readme.py`. Everything outside these markers is completely preserved.

---

## ⚙️ Running Locally

The scripts use Python's **standard library only** (`urllib`, `json`, `datetime`, `xml.sax.saxutils`). No `pip install` required!

```bash
# If running locally, make sure you have GitHub CLI auth or export GITHUB_TOKEN
export GITHUB_TOKEN=$(gh auth token)

python3 scripts/make_github_card.py && python3 scripts/make_header.py && python3 scripts/render_readme.py
```
