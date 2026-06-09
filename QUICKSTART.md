# ⚡ Quick Start Guide (5 Minutes)

## Step 1: Get Your API Key (1 minute)
1. Go to https://console.anthropic.com
2. Create account or login
3. Copy your API key (starts with `sk-ant-`)

## Step 2: Configure (2 minutes)

### Windows:
```bash
# Edit file: backend\.env
# Update this line:
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### macOS/Linux:
```bash
cd backend
nano .env  # or vim .env
# Update ANTHROPIC_API_KEY
```

## Step 3: Start Everything (1 minute)

### Windows:
Double-click `run.bat` (it will open a terminal)

### macOS/Linux:
```bash
chmod +x run.sh
./run.sh
```

## Step 4: Open Dashboard (1 minute)

Once you see in terminal:
```
✨ Starting Flask application...
📱 Dashboard will be available at: http://localhost:5000
```

Open in your browser: **http://localhost:5000**

---

## 🎯 Try It Now

1. **Click button:** "🔗 Connect DB"
2. **Click a query:** Select "Customer Transfer History"
3. **Click button:** "🤖 Start Autonomous Optimization"
4. **Watch the magic:** See AI analyze and optimize in real-time!

---

## ❓ Not Working?

### Docker not found?
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Restart your terminal after installing

### "Connection failed"?
- Wait 10 seconds and click "🔗 Connect DB" again
- Check: `docker-compose ps` (should show postgres running)

### "API Key Error"?
- Go to https://console.anthropic.com
- Get a new API key
- Update `backend/.env`

### Still stuck?
- Check README.md Troubleshooting section
- Look at terminal output for error messages

---

## 📊 What Happens Next?

The PoC will:
1. **📖 Read** your slow query
2. **🔍 Analyze** with AI (EXPLAIN PLAN)
3. **💡 Generate** 3 optimization ideas
4. **🧪 Test** each hypothesis
5. **📈 Show** results in dashboard

Expected: **50-75% improvement** in query speed with suggested indexes!

---

## 💡 Key Things to Know

- ✅ **All data is synthetic** (for safe demo)
- ✅ **No production databases harmed**
- ✅ **All changes are recommendations** (not auto-applied)
- ✅ **Works offline** (just needs your API key once)

---

## 🚀 You're Ready!

Next: Open http://localhost:5000 and explore! 🎉
