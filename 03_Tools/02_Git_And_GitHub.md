# 02 — Git & GitHub

> **Save your work. Show your work. Share your work.**

---

## Why Use Git?

✅ Never lose your code
✅ Track every change
✅ Work with others
✅ Show employers what you can do
✅ Required in every research project

---

## The 5 Most Important Commands

```bash
git init          # Start a new project
git add .         # Stage all changes
git commit -m ""  # Save a snapshot
git push          # Upload to GitHub
git pull          # Download latest version
```

---

## First Time Setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
```

---

## Your Daily Workflow

```bash
# 1. Make changes to files
# 2. Save them
git add .
git commit -m "Add data cleaning script"

# 3. Upload
git push
```

**Do this 3-5 times a day.** Make small, clear commits.

---

## Branching (When You're Ready)

```bash
git branch new-feature   # create branch
git checkout new-feature # switch to it
# ... do work ...
git merge new-feature    # merge back
```

---

## GitHub Profile

Your GitHub is your **research CV**.

Things to do:
- [ ] Add a profile picture
- [ ] Write a profile README
- [ ] Pin your best 6 repos
- [ ] Add a contribution graph (commit often!)

---

## ✏️ Practice Exercises

### Exercise 1: Install Git (Easy)
**Time:** 15 minutes
**Task:** Install Git and set up your identity.
**Why:** You need Git to do anything.

**How to do it:**

**Windows:** Download from git-scm.com
**Mac:** `brew install git` or download from git-scm.com
**Linux:** `sudo apt install git`

**Configure:**
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
git config --global init.default branch main
```

**Verify:**
```bash
git --version
git config --list
```

---

### Exercise 2: Create Your First Repo (Easy)
**Time:** 30 minutes
**Task:** Make a local repo, add a file, commit.
**Why:** Learn the basic workflow.

**Steps:**
```bash
# 1. Create a folder
mkdir my-first-repo
cd my-first-repo

# 2. Initialize
git init

# 3. Create a file
echo "# My First Repo" > README.md

# 4. Check status
git status

# 5. Stage the file
git add README.md

# 6. Commit
git commit -m "First commit: add README"

# 7. See history
git log
```

**You just made your first commit!** 🎉

---

### Exercise 3: Push To GitHub (Medium)
**Time:** 30 minutes
**Task:** Upload your local repo to GitHub.
**Why:** This is what you'll do for every project.

**Steps:**

1. Go to github.com, sign up (free)
2. Click "+" → "New repository"
3. Name: `my-first-repo`
4. **Don't** check "Initialize with README" (we have one)
5. Click "Create repository"
6. Copy the URL (e.g., https://github.com/username/my-first-repo)

**Then in terminal:**
```bash
git remote add origin https://github.com/username/my-first-repo.git
git branch -M main
git push -u origin main
```

**Refresh GitHub page** — you should see your README!

**To update later:**
```bash
# Make changes to files
git add .
git commit -m "Describe what you changed"
git push
```

---

### Exercise 4: Add A .gitignore (Medium)
**Time:** 30 minutes
**Task:** Don't track useless files.
**Why:** Don't commit junk like `__pycache__` or `node_modules`.

**Step 1:** Create `.gitignore` in your repo
**Step 2:** Add common Python ignores:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
*.egg-info/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Data (large files)
*.csv
!small_data.csv
data/raw/
data/processed/
```

**Step 3:** Commit:
```bash
git add .gitignore
git commit -m "Add gitignore for Python"
git push
```

**Try:** Add a `venv/` folder. It should NOT be tracked.

---

### Exercise 5: Use Branches (Medium)
**Time:** 1 hour
**Task:** Create a branch, make changes, merge back.
**Why:** This is how teams work. You need it for collaboration.

**Steps:**
```bash
# 1. Create branch
git branch feature-readme

# 2. Switch to it
git checkout feature-readme

# 3. Edit README.md (add more content)
echo "## New section" >> README.md

# 4. Commit
git add README.md
git commit -m "Expand README with new section"

# 5. Push branch to GitHub
git push -u origin feature-readme

# 6. Go to GitHub, click "Compare & pull request", merge it
# (Or merge locally:)
git checkout main
git merge feature-readme

# 7. Delete branch
git branch -d feature-readme
```

---

### Exercise 6: Polish Your GitHub Profile (Hard)
**Time:** 2-3 hours
**Task:** Make your GitHub look professional.
**Why:** This is your CV. Make it shine.

**Steps:**

**1. Profile README** (shows at top of profile)
- Create a new repo named: `your-username/your-username`
- Add a `README.md`:

```markdown
# Hi, I'm [Your Name] 👋

## 👨‍💻 About Me
- MSc Data Science student at [University]
- Interested in [your area]
- Currently working on [your thesis topic]

## 🔧 Skills
Python, PyTorch, scikit-learn, SQL, Git, LaTeX

## 📊 GitHub Stats
![Your GitHub stats](https://github-readme-stats.vercel.app/api?username=your-username)

## 📫 Contact
- LinkedIn: [link]
- Email: [email]
```

**2. Pin 6 repos**
- Go to your profile
- Click "Customize your pins"
- Pick your best 6 repositories

**3. Add topics to each repo**
- Click on a repo → settings → topics
- Add: machine-learning, python, data-science, etc.

**4. Write good READMEs**
Every repo should have a README with:
- Title
- What it does
- How to install
- How to use
- License

---

## ✅ Done When

- [ ] You set up a GitHub account
- [ ] You pushed your first commit
- [ ] You have a profile README
- [ ] Your thesis code is on GitHub
- [ ] You used branches at least once
- [ ] You completed all 6 exercises
