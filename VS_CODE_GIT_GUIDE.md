# 🚀 VS Code & GitHub Push Guide for Fabric Defect Detection

This guide walks you step-by-step through opening the project in **VS Code**, ignoring sensitive environment files (`.env`), and pushing your code to the GitHub repository:

👉 **Target Repository URL:** [https://github.com/ramanathankamesh2006-lgtm/Fabric-defect-detection](https://github.com/ramanathankamesh2006-lgtm/Fabric-defect-detection)

---

## 📌 Prerequisites

1. **Visual Studio Code (VS Code)** installed on your machine.
2. **Git** installed (`C:\Program Files\Git\cmd\git.exe`).
3. Your local code directory:
   `C:\Users\Subash R\.gemini\antigravity\scratch\fabric_ai`

---

## 🔒 Step 1: Ensure `.env` is Ignored in `.gitignore`

The `.gitignore` file has been configured to automatically prevent any `.env` files, API keys, or secrets from being uploaded to GitHub.

Your `.gitignore` file contains:

```gitignore
# Environment Variables (Secrets & Credentials)
.env
.env.local
.env.development
.env.production
.env.*

# Byte-compiled files & Virtual Environments
__pycache__/
*.py[cod]
.venv/
venv/

# Temporary logs & datasets
*.log
.system_generated/
```

> [!IMPORTANT]
> Never remove `.env` from `.gitignore`. If you create a `.env` file for secret API keys or credentials, Git will automatically ignore it.

---

## 💻 Step 2: Open Project Folder in VS Code

1. Open **VS Code**.
2. Click **File** &rarr; **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Navigate to:
   `C:\Users\Subash R\.gemini\antigravity\scratch\fabric_ai`
4. Click **Select Folder**.
5. Open the integrated terminal in VS Code by pressing `` Ctrl + ` `` (backtick) or clicking **Terminal** &rarr; **New Terminal**.

---

## 🔗 Step 3: Connect Git Remote to GitHub

In your VS Code terminal, execute the following commands:

### 1. Check current Git status:
```bash
git status
```

### 2. Add the remote GitHub repository:
```bash
git remote add origin https://github.com/ramanathankamesh2006-lgtm/Fabric-defect-detection.git
```

*(If `origin` already exists, update it using: `git remote set-url origin https://github.com/ramanathankamesh2006-lgtm/Fabric-defect-detection.git`)*

### 3. Verify remote connection:
```bash
git remote -v
```

---

## 📤 Step 4: Stage, Commit & Push Code to GitHub

### 1. Stage all project files:
```bash
git add .
```

### 2. Create a commit message:
```bash
git commit -m "Initial release: Complete AI Fabric Defect Detection System"
```

### 3. Rename branch to `main`:
```bash
git branch -M main
```

### 4. Push code to GitHub:
```bash
git push -u origin main --force
```

---

## 🏃 Step 5: How to Run the Application in VS Code

Whenever you open the project in VS Code, you can launch the app directly from the terminal:

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501) to view your live AI Fabric Defect Detection system!
