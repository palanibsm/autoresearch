# 🚀 Install & Run Guide

## ✅ Installation Status

- ✅ Python dependencies installed
- ✅ Flask app ready
- ✅ Database schema ready (SQL)
- ✅ Dashboard ready (HTML)
- ⏳ Docker PostgreSQL (needs to be started)

---

## 🐳 Step 1: Start Docker PostgreSQL

### Windows PowerShell or CMD

```bash
cd C:\code\autoresearch
docker-compose up -d
```

**Wait for it to start (5-10 seconds)**, then verify:

```bash
docker-compose ps
```

You should see:
```
banking_db_optimizer   postgres:15-alpine   Up
```

---

## 🚀 Step 2: Start Flask Backend

### In a NEW Terminal

```bash
cd C:\code\autoresearch\backend
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## 🌐 Step 3: Open Dashboard

Open your browser and go to:

**http://localhost:5000**

You should see the Database Query Optimizer dashboard!

---

## 🎮 Step 4: Run the Demo

1. **Click:** "🔗 Connect DB"
   - Should show "Connected"

2. **Click:** "Reload Queries"
   - Should load 4 banking queries

3. **Select:** Any query (e.g., "Customer Transfer History")

4. **Click:** "🤖 Start Autonomous Optimization"
   - Watch the progress bar
   - Watch the logs
   - Wait 60-90 seconds for results

---

## 📊 Expected Output

### In Terminal (Flask logs):
```
127.0.0.1 - - [09/Jun/2026 16:35:00] "POST /api/db/connect HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2026 16:35:02] "GET /api/queries/slow HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2026 16:35:05] "POST /api/optimize/autonomous HTTP/1.1" 200 -
```

### In Dashboard:
```
Status: analyzing → running_autonomous → completed

Progress: 0% → 50% → 100%

Results:
- Query: Customer Transfer History
- Baseline: 1250 ms
- Expected Improvement: 52-75%
- Recommendation: CREATE INDEX idx_transactions...
```

---

## 🔧 Configuration

Your API key is already configured in `backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banking_db
DB_USER=banking_user
DB_PASSWORD=banking_pass
```

---

## 🐛 Troubleshooting

### "Docker not found"
```bash
# Make sure Docker Desktop is running
# Windows: Open "Docker Desktop" application
# Check: docker --version
```

### "Port 5000 already in use"
```bash
# Kill the process on port 5000
# Windows: netstat -ano | findstr :5000
# Or change port in backend/app.py: app.run(port=5001)
```

### "Connection failed" on dashboard
```bash
# Wait 10 seconds for database to start
# Click "Connect DB" button again
# Check Docker: docker-compose ps
```

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

---

## 🎯 Keep It Running

**Terminal 1 (Docker):**
```bash
cd C:\code\autoresearch
docker-compose up
```
Keep running in background

**Terminal 2 (Flask):**
```bash
cd C:\code\autoresearch\backend
python app.py
```
Keep running in background

**Browser:**
```
http://localhost:5000
```

---

## ⏹️ Stop Everything

### Stop Flask
Press `Ctrl+C` in Terminal 2

### Stop Docker
```bash
docker-compose down
```
(Keeps data)

### Remove Everything
```bash
docker-compose down -v
```
(Deletes database)

---

## 📱 Access Points

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5000 |
| API Health | http://localhost:5000/api/health |
| Flask Debug | http://localhost:5000 (port 5000) |
| PostgreSQL | localhost:5432 |

---

## ✨ You're Ready!

1. **Terminal 1:** `docker-compose up`
2. **Terminal 2:** `cd backend && python app.py`
3. **Browser:** http://localhost:5000
4. **Click:** "Connect DB"
5. **Enjoy!** 🚀

---

## 📚 Next Steps

- See **START_HERE.md** for quick overview
- See **README.md** for full documentation
- See **QUICKSTART.md** for reference

Good luck with the demo! 🎉
