# 🚀 Database Query Optimizer - Autoresearch PoC

An **autonomous AI-powered database query optimization system** for Singapore banking, demonstrating the autoresearch pattern from Andrej Karpathy's project.

## 🎯 Project Overview

This PoC showcases how **Claude AI agents** can autonomously:
- 🔍 Analyze slow database queries
- 💡 Generate multiple optimization hypotheses
- 🧪 Test each hypothesis iteratively
- 📊 Track progress in real-time
- 📈 Recommend the best optimization strategy

**Target Use Case:** Optimize slow banking queries (fund transfers, loan processing, fraud detection) running on PostgreSQL.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Web Dashboard (React-like)                 │
│                   - Query selection                         │
│                   - Live progress tracking                  │
│                   - Real-time optimization logs             │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│              Flask Backend (Python)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ AI Query Optimizer Agent (Claude API)                 │ │
│  │  • Analyzes EXPLAIN PLAN                             │ │
│  │  • Generates optimization hypotheses                 │ │
│  │  • Suggests indexes and query rewrites               │ │
│  │  • Multi-turn conversation for refinement            │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Database Operations                                    │ │
│  │  • Query execution & profiling                       │ │
│  │  • Index creation/testing                            │ │
│  │  • Performance metrics collection                    │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ psycopg2
┌──────────────────────▼──────────────────────────────────────┐
│          PostgreSQL (Docker Container)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Banking Database (Synthetic Data)                     │ │
│  │  • customers, accounts, transactions                 │ │
│  │  • loans, loan_payments                              │ │
│  │  • fraud_alerts                                       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ |
| **Framework** | Flask 3.0 |
| **Database** | PostgreSQL 15 (Docker) |
| **AI Engine** | Anthropic Claude 3.5 Sonnet |
| **Frontend** | Vanilla HTML/CSS/JS |
| **ORM/Query** | psycopg2 + SQLAlchemy |

---

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** - [Install here](https://docs.docker.com/get-docker/)
- **Python 3.8+** - [Install here](https://www.python.org/downloads/)
- **Anthropic API Key** - Get from [console.anthropic.com](https://console.anthropic.com)

### 1️⃣ Clone & Setup

```bash
# Navigate to project
cd C:\code\autoresearch

# Windows: Run startup script
run.bat

# Or macOS/Linux:
chmod +x run.sh
./run.sh
```

### 2️⃣ Configure API Key

Edit `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banking_db
DB_USER=banking_user
DB_PASSWORD=banking_pass
```

### 3️⃣ Start Services

```bash
# Terminal 1: Start PostgreSQL
docker-compose up

# Terminal 2: Start Flask backend
cd backend
pip install -r requirements.txt
python app.py
```

### 4️⃣ Open Dashboard

Navigate to: **http://localhost:5000**

---

## 📋 Project Structure

```
autoresearch/
├── docker-compose.yml          # PostgreSQL container config
├── backend/
│   ├── app.py                  # Flask main application
│   ├── db_utils.py            # Database connection & operations
│   ├── ai_optimizer.py        # Claude AI optimization logic
│   ├── requirements.txt        # Python dependencies
│   └── .env                   # Configuration (API keys)
├── dashboard/
│   └── index.html             # Interactive web dashboard
├── data/
│   └── init.sql               # Banking schema + synthetic data
├── logs/
│   └── (optimization logs)
├── run.sh                      # Startup script (Linux/macOS)
├── run.bat                     # Startup script (Windows)
└── README.md                   # This file
```

---

## 🎮 How to Use the Dashboard

### Step 1: Connect to Database
Click **🔗 Connect DB** button to establish connection to PostgreSQL.

### Step 2: View Slow Queries
The dashboard loads 4 pre-configured slow banking queries:
- **Customer Transfer History** - Multi-table join without proper indexes
- **Loan Payment Summary** - Aggregation across related tables
- **Fraud Detection** - Complex filtering with high-risk conditions
- **Account Balance Verification** - Large LEFT JOIN with conditions

### Step 3: Analyze a Query
Click on any query to select it, then:
- **Quick Analysis**: Automatic analysis with AI-generated optimization hypotheses
- **Custom Query**: Paste any SQL query and analyze

### Step 4: Run Autonomous Optimization
Click **🤖 Start Autonomous Optimization** to run the autoresearch-style loop:

1. **📊 Baseline Metrics** - Captures current execution time
2. **🤖 AI Analysis** - Claude analyzes the query plan
3. **💡 Hypothesis Generation** - 3 optimization strategies proposed
4. **🧪 Testing** - Each hypothesis is tested iteratively
5. **📈 Results** - Best optimization with % improvement shown

### Step 5: View Results
The dashboard displays:
- Baseline vs. optimized execution times
- AI's analysis and root cause identification
- Recommended indexes to create
- SQL statements ready for DBA implementation

---

## 🔬 Key Features

### ✨ Autonomous Optimization Loop
- Mimics Karpathy's autoresearch pattern
- Generates multiple hypotheses automatically
- Tests and ranks them by effectiveness
- Iterates until optimal solution found

### 🧠 Claude AI Integration
- **Multi-turn conversations** for iterative refinement
- **SQL expertise** - Understands PostgreSQL optimization
- **Index strategy generation** - Proposes specific CREATE INDEX statements
- **Query rewriting** - Suggests improved query structures

### 📊 Real-Time Progress Tracking
- Live progress bar (0-100%)
- Structured logging with timestamps
- Status badges (analyzing, testing, completed)
- Color-coded logs (info, success, error)

### 🗄️ Banking Scenarios
Synthetic data includes:
- **Customers** - 20 customer records (Singapore + Malaysia)
- **Accounts** - SAVINGS and CHECKING accounts
- **Transactions** - 500 fund transfer records
- **Loans** - 50 active/closed loans with payments
- **Fraud Alerts** - 100 fraud detection flags

---

## 🔧 API Endpoints

### Database
- `GET /api/health` - System health check
- `POST /api/db/connect` - Connect to database
- `POST /api/db/disconnect` - Disconnect from database
- `GET /api/db/tables` - Get table information

### Queries
- `GET /api/queries/slow` - Get list of slow queries
- `POST /api/analyze/query` - Analyze single query with AI

### Optimization
- `POST /api/optimize/autonomous` - Run autonomous optimization
- `GET /api/optimization/status` - Get current optimization status
- `GET /api/optimizations` - Get all completed optimizations
- `GET /api/optimizations/<query_id>` - Get specific optimization result

---

## 📊 Expected Results

After running autonomous optimization, you'll see:

```
✅ Optimization Results:
├─ Query: Customer Transfer History
├─ Baseline: 1250.45 ms
├─ Best Optimization: 312.61 ms (75% improvement)
├─ Hypothesis Tested: 3
└─ Recommendation: CREATE INDEX idx_transactions_customer_created ON transactions(customer_id, created_at);
```

---

## 🔍 Understanding the AI Analysis

Claude's analysis includes:

### Root Cause Analysis
Identifies what's making the query slow:
- Missing indexes on frequently filtered columns
- Inefficient join ordering
- Full table scans that could be avoided
- Suboptimal execution plans

### Optimization Hypotheses
Proposes 3 strategies:
1. **Single Column Indexes** - On frequently filtered columns
2. **Composite Indexes** - Multi-column indexes for complex queries
3. **Query Rewriting** - Restructuring query for better plans

### Implementation Recommendations
Provides:
- Exact CREATE INDEX statements
- Expected performance improvements
- Risk assessment
- Implementation steps for DBAs

---

## 🛠️ Customization

### Add Your Own Queries
Edit `backend/db_utils.py`, function `get_slow_queries()`:

```python
def get_slow_queries(self) -> List[Dict]:
    queries = [
        {
            'id': 'your_query_id',
            'name': 'Your Query Name',
            'description': 'What it does',
            'query': 'SELECT * FROM ... WHERE ...',
            'optimization_opportunity': 'What Claude should focus on'
        },
        # ... more queries
    ]
```

### Adjust AI Model
Edit `backend/ai_optimizer.py`:

```python
response = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Change this
    max_tokens=2000,
    system="You are a PostgreSQL expert...",
    messages=[...]
)
```

### Customize Dashboard
Edit `dashboard/index.html` to:
- Change colors and branding
- Add more visualization charts
- Integrate with your monitoring tools

---

## 🐛 Troubleshooting

### Docker Connection Failed
```bash
# Check Docker is running
docker ps

# Restart Docker Compose
docker-compose down
docker-compose up -d
```

### Database Connection Timeout
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Verify credentials in backend/.env
# Default: user=banking_user, password=banking_pass
```

### Claude API Errors
```
Error: "ANTHROPIC_API_KEY not configured"
→ Add API key to backend/.env

Error: "Rate limit exceeded"
→ Wait 60 seconds before retrying
→ Check your Claude API quota
```

### Port Already in Use
```bash
# Flask uses port 5000, PostgreSQL uses 5432
# If ports are occupied, update docker-compose.yml or change Flask port in app.py
```

---

## 📈 Performance Expectations

On a modern machine with synthetic data:

| Operation | Time |
|-----------|------|
| Database startup | ~5 seconds |
| Query analysis | ~15-30 seconds |
| Single hypothesis test | ~2-5 seconds |
| Full optimization (3 hypotheses) | ~60-90 seconds |
| Dashboard load | <1 second |

---

## 🔐 Security Notes

### For Production:
⚠️ **This is a PoC, not production-ready. For production use:**

- Use environment-specific credentials
- Implement query validation/sanitization
- Add authentication to the Flask API
- Use HTTPS/TLS for API communication
- Audit and test all AI-generated SQL before execution
- Implement rate limiting and API keys
- Never expose database credentials in code

---

## 🎓 Learning Resources

### Understanding Autoresearch Pattern
- [Andrej Karpathy's Autoresearch](https://github.com/karpathy/autoresearch)
- Pattern: Generate hypotheses → Test → Refine → Iterate

### PostgreSQL Optimization
- [EXPLAIN PLAN Guide](https://www.postgresql.org/docs/current/sql-explain.html)
- [Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- [Query Planning](https://www.postgresql.org/docs/current/query-path.html)

### Claude API
- [Claude API Documentation](https://docs.anthropic.com)
- [Prompt Caching](https://docs.anthropic.com/en/docs/build-a-python-chatbot-with-a-system-prompt-and-preamble)
- [Vision Capabilities](https://docs.anthropic.com/en/docs/vision)

---

## 📞 Support & Feedback

For questions or issues:
1. Check **Troubleshooting** section above
2. Review Flask app logs in terminal
3. Check Docker container logs: `docker-compose logs postgres`
4. Verify `.env` configuration

---

## 📝 License

This PoC is provided as-is for demonstration purposes in Singapore banking context.

---

## 🙏 Credits

- **Inspired by:** Andrej Karpathy's [Autoresearch](https://github.com/karpathy/autoresearch)
- **AI Engine:** Anthropic Claude 3.5 Sonnet
- **Use Case:** Singapore banking database optimization
- **Built for:** Group Operations & Technology team

---

## 🎯 Next Steps

After exploring this PoC:

1. **Integrate with your actual databases** - Modify connection strings and schemas
2. **Add real slow query logs** - Load from your production query logs
3. **Implement index creation** - Add safe index creation with rollback support
4. **Connect to monitoring** - Integrate with Grafana/DataDog for continuous optimization
5. **Build compliance layer** - Add audit logging for regulatory requirements

---

**Happy optimizing! 🚀**
