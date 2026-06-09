# 🐍 Virtual Environment Setup Guide

## ✅ Your `.venv` is Ready!

Your Python virtual environment (`.venv`) is fully set up with all dependencies installed locally.

---

## 🚀 How to Run Using Your `.venv`

### Option 1: Windows Command Prompt (Easiest)

**Terminal 1 - Start Database:**
```bash
cd C:\code\autoresearch
docker-compose up
```

**Terminal 2 - Start Flask (using .venv):**
```bash
cd C:\code\autoresearch\backend
C:\code\autoresearch\.venv\Scripts\python.exe app.py
```

**Or shorter (if you add .venv to PATH):**
```bash
cd C:\code\autoresearch\backend
.venv\Scripts\python.exe app.py
```

---

### Option 2: Windows PowerShell

**Terminal 1 - Start Database:**
```powershell
cd "C:\code\autoresearch"
docker-compose up
```

**Terminal 2 - Start Flask:**
```powershell
cd "C:\code\autoresearch\backend"
& "C:\code\autoresearch\.venv\Scripts\python.exe" app.py
```

---

### Option 3: Activate venv First (Most Conventional)

**Terminal 1 - Start Database:**
```bash
cd C:\code\autoresearch
docker-compose up
```

**Terminal 2 - Activate venv and start Flask:**
```bash
cd C:\code\autoresearch\backend

# Activate virtual environment
.venv\Scripts\activate.bat

# Now python will use the venv automatically
python app.py
```

After activation, your terminal should show:
```
(.venv) C:\code\autoresearch\backend>
```

---

## 🔑 What's Installed in Your `.venv`

All these packages are now isolated in your `.venv` folder:

- ✅ Flask 3.0.0 - Web framework
- ✅ Flask-CORS 4.0.0 - CORS support
- ✅ psycopg2-binary 2.9.12 - PostgreSQL driver
- ✅ SQLAlchemy 2.0.23 - ORM
- ✅ anthropic 0.39.0 - Claude API
- ✅ python-dotenv 1.0.0 - Environment variables
- ✅ requests 2.31.0 - HTTP library
- ✅ Werkzeug 3.0.1 - WSGI utilities

**Total: 33 packages installed**

---

## ✅ Your `.venv` Benefits

| Benefit | Reason |
|---------|--------|
| **Isolation** | Packages don't affect system Python |
| **Portability** | Can share `.venv` with team |
| **Cleanliness** | No system Python pollution |
| **Reproducibility** | Everyone gets same versions |
| **Easy cleanup** | Just delete `.venv` folder to reset |

---

## 🔄 If You Need to Reinstall Dependencies

```bash
# Activate venv
cd C:\code\autoresearch\backend
C:\code\autoresearch\.venv\Scripts\activate.bat

# Reinstall from requirements.txt
pip install -r requirements.txt
```

---

## 📦 Add New Packages

If you need to add more packages:

```bash
# With venv activated
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🐛 Troubleshooting

### Issue: "python command not found"
**Solution:** Use full path to venv Python:
```bash
C:\code\autoresearch\.venv\Scripts\python.exe app.py
```

### Issue: "Module not found"
**Solution:** Make sure you're in the backend directory:
```bash
cd C:\code\autoresearch\backend
C:\code\autoresearch\.venv\Scripts\python.exe app.py
```

### Issue: "activate.bat not found"
**Solution:** Use the full path:
```bash
C:\code\autoresearch\.venv\Scripts\activate.bat
```

### Issue: "Port 5000 already in use"
**Solution:** Check what's using it:
```bash
netstat -ano | findstr :5000
```

---

## 📊 Running the Complete Application

### All Three Components:

**Terminal 1 (Docker/Database):**
```bash
cd C:\code\autoresearch
docker-compose up
```
Keep this running. You'll see database logs here.

**Terminal 2 (Flask Backend):**
```bash
cd C:\code\autoresearch\backend
C:\code\autoresearch\.venv\Scripts\python.exe app.py
```
Keep this running. You'll see API logs here.

**Terminal 3 (Browser):**
```
Open: http://localhost:5000
```

---

## 🎯 Quick Commands Reference

| Action | Command |
|--------|---------|
| **Activate venv** | `.venv\Scripts\activate.bat` |
| **Deactivate venv** | `deactivate` |
| **Check venv active** | Look for `(.venv)` in terminal |
| **Install packages** | `pip install package_name` |
| **List installed** | `pip list` |
| **Start app** | `.venv\Scripts\python.exe app.py` |
| **Delete venv** | `rmdir /s /q .venv` |

---

## 🔒 `.venv` in `.gitignore`

Good news! Your `.venv` is already excluded from Git:
```
.venv/
venv/
ENV/
env/
```

This means:
- ✅ `.venv` folder won't be pushed to GitHub
- ✅ Everyone clones just the code
- ✅ They install their own `.venv` with `pip install -r requirements.txt`

---

## 📖 Next Steps

1. **Start Database:**
   ```bash
   cd C:\code\autoresearch
   docker-compose up
   ```

2. **Start Flask (in another terminal):**
   ```bash
   cd C:\code\autoresearch\backend
   C:\code\autoresearch\.venv\Scripts\python.exe app.py
   ```

3. **Open Dashboard:**
   ```
   http://localhost:5000
   ```

4. **Try a query optimization:**
   - Click "Connect DB"
   - Select a query
   - Click "Start Autonomous Optimization"

---

## ✨ You're All Set!

Your `.venv` is ready. No other setup needed. Just run the commands above! 🚀
