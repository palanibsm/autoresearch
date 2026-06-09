# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 🎯 Project Overview

**Database Query Optimizer PoC** - An autonomous AI-powered system that optimizes slow database queries using autoresearch pattern.

- **Tech Stack:** Python (Flask) + PostgreSQL (Docker) + Claude AI + HTML/JS Dashboard
- **Purpose:** Demonstrate AI-driven database optimization for Singapore banking
- **Scope:** Synthetic banking data with 4 pre-configured slow queries
- **Key Pattern:** Autoresearch-style autonomous hypothesis generation, testing, and refinement

---

## 🏗️ Architecture & Key Files

### Backend Services (`backend/`)

| File | Purpose |
|------|---------|
| `app.py` | Flask REST API server (port 5000) |
| `db_utils.py` | PostgreSQL connection, query execution, metrics collection |
| `ai_optimizer.py` | Claude AI integration for query analysis & optimization |
| `.env` | Configuration (DB credentials, API keys) |
| `requirements.txt` | Python dependencies |

### Database & Frontend

| File | Purpose |
|------|---------|
| `docker-compose.yml` | PostgreSQL 15 container definition |
| `data/init.sql` | Banking schema + 1000+ synthetic records |
| `dashboard/index.html` | Interactive web UI with real-time progress |

### Setup & Documentation

| File | Purpose |
|------|---------|
| `run.bat` / `run.sh` | Automated startup scripts |
| `setup.py` | Interactive setup wizard |
| `README.md` | Comprehensive documentation |
| `QUICKSTART.md` | 5-minute getting started guide |

---

## 🚀 Common Development Tasks

### Start the System
```bash
# Windows:
run.bat

# macOS/Linux:
chmod +x run.sh && ./run.sh

# Or manually:
docker-compose up              # Terminal 1: PostgreSQL
cd backend && python app.py    # Terminal 2: Flask
# Visit: http://localhost:5000
```

### Run Tests (Currently None)
Currently no automated tests. To add:
- Create `backend/test_*.py` files
- Use pytest framework
- Mock database with fixtures

### Database Operations
```bash
# Connect to running database
docker-compose exec postgres psql -U banking_user -d banking_db

# View logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up
```

### Check System Health
```bash
# Test Flask API
curl http://localhost:5000/api/health

# Test database connection
curl http://localhost:5000/api/db/connect -X POST
```

---

## 🔑 Key Components & Their Interactions

### 1. Query Analysis Flow
```
User selects query
    ↓
Flask API: /analyze/query
    ↓
db_utils.py: get_query_stats() → captures execution time
    ↓
ai_optimizer.py: QueryOptimizer.analyze_query()
    ↓
Claude API: Analyzes EXPLAIN PLAN, generates hypotheses
    ↓
Dashboard: Displays analysis + proposed indexes
```

### 2. Autonomous Optimization Flow
```
/optimize/autonomous endpoint
    ↓
Baseline metrics collected (db_utils.get_query_stats)
    ↓
Claude analyzes: QueryOptimizer.analyze_query()
    ↓
For each hypothesis:
    - Simulate index creation
    - Measure improvement
    - Rank by effectiveness
    ↓
Best optimization recommended
    ↓
Results stored in optimization_state dict
    ↓
WebSocket updates dashboard in real-time
```

### 3. Claude AI Integration
**File:** `ai_optimizer.py` - `QueryOptimizer` class

Key methods:
- `analyze_query()` - First analysis with hypotheses generation
- `refine_optimization()` - Multi-turn refinement (demonstrates conversation)
- `generate_optimization_report()` - Executive summary
- `generate_query_rewrite()` - Alternative query suggestions

**Pattern:** Conversation history maintained for iterative refinement (autoresearch approach)

---

## 📊 Database Schema

### Banking Tables (auto-created in init.sql)

```sql
customers (customer_id, name, email, phone, country_code)
accounts (account_id, customer_id, account_type, balance, currency, status)
transactions (transaction_id, from_account_id, to_account_id, amount, currency, status, created_at)
loans (loan_id, customer_id, principal_amount, interest_rate, term_months, status, maturity_date)
loan_payments (payment_id, loan_id, amount, payment_date, status)
fraud_alerts (alert_id, transaction_id, customer_id, alert_type, risk_score, status)
```

**Pre-loaded Data:**
- 20 customers
- 15 accounts
- 500 transactions
- 50 loans
- 200 loan payments
- 100 fraud alerts

---

## 🔌 API Endpoints

### Database Operations
- `POST /api/db/connect` - Establish connection
- `POST /api/db/disconnect` - Close connection
- `GET /api/health` - Health check
- `GET /api/db/tables` - Table information

### Query Management
- `GET /api/queries/slow` - List slow queries
- `POST /api/analyze/query` - Analyze single query

### Optimization
- `POST /api/optimize/autonomous` - Start optimization (async)
- `GET /api/optimization/status` - Check progress
- `GET /api/optimizations` - Get all results
- `GET /api/optimizations/<id>` - Get specific result

---

## 🧠 How AI Optimization Works

### The Autoresearch Pattern
This PoC mimics Karpathy's autoresearch:
1. **Hypothesis Generation** - AI generates 3 index strategies
2. **Testing** - Each strategy is tested (simulated in PoC)
3. **Ranking** - Results ranked by improvement %
4. **Iteration** - Best result identified, can refine further
5. **Reporting** - Executive summary generated

### Claude Model Details
- **Model:** claude-3-5-sonnet-20241022
- **Max Tokens:** 2000
- **System Prompt:** "PostgreSQL query optimization expert"
- **Context:** Multi-turn conversations maintained in `conversation_history`

---

## 🔧 Configuration & Customization

### Add New Slow Queries
Edit `backend/db_utils.py`, method `get_slow_queries()`:
```python
{
    'id': 'unique_id',
    'name': 'Query Name',
    'description': 'What it does',
    'query': 'SELECT ...',
    'optimization_opportunity': 'What to focus on'
}
```

### Change AI Model
Edit `backend/ai_optimizer.py`, search for `model="claude-3-5-sonnet-20241022"`:
```python
response = self.client.messages.create(
    model="claude-opus-4-8",  # Switch to Opus for more powerful analysis
    max_tokens=2000,
    ...
)
```

### Modify Dashboard
`dashboard/index.html` - Vanilla JS, no build process needed
- Colors/branding: Search for `#667eea` (primary color)
- Endpoints: All API calls in JavaScript at bottom
- Progress tracking: Uses polling (every 500ms via `updateOptimizationStatus()`)

---

## ⚠️ Important Notes

### Security (Development Only)
- 🔓 No authentication implemented
- 🔓 Database credentials in .env
- 🔓 Claude API key in plaintext
- ✅ Use environment variables in production

### Limitations
- Optimization improvements are **simulated** (not real)
- Indexes are **not actually created** (safe for demo)
- Works with **synthetic data only**
- Single-threaded optimization (no parallel testing)

### For Production Use
1. Add authentication & authorization
2. Implement actual index creation with rollback
3. Use transaction isolation levels
4. Add comprehensive logging & auditing
5. Implement query validation & sanitization
6. Add database connection pooling
7. Rate limiting on API endpoints

---

## 🐛 Debugging Tips

### Check Flask Logs
Terminal running Flask will show:
- Request/response details
- Error tracebacks
- Database connection issues

### Monitor Database
```bash
# Check active connections
docker-compose exec postgres psql -U banking_user -d banking_db \
  -c "SELECT * FROM pg_stat_activity;"

# View query logs
docker-compose logs -f postgres
```

### Test API Directly
```bash
# Test analysis endpoint
curl -X POST http://localhost:5000/api/analyze/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM customers LIMIT 1;"}'

# Check status
curl http://localhost:5000/api/optimization/status
```

### Frontend Debugging
Open browser DevTools (F12):
- **Console** - See JavaScript errors
- **Network** - Monitor API calls
- **Application** - Check localStorage (if added)

---

## 📈 Performance Expectations

| Operation | Time |
|-----------|------|
| DB startup | ~5s |
| Query analysis | ~20-30s |
| Single hypothesis test | ~2-5s |
| Full optimization (3 hyp) | ~60-90s |
| Dashboard response | <100ms |

---

## 🔄 Workflow Recommendations

### For Feature Additions
1. Add new endpoint in `app.py`
2. Implement logic in `db_utils.py` or `ai_optimizer.py`
3. Update `dashboard/index.html` with UI
4. Test via API first, then dashboard
5. Verify in browser

### For AI Improvements
1. Modify system prompts in `ai_optimizer.py`
2. Adjust conversation flow in multi-turn methods
3. Test with different queries
4. Compare output quality
5. Document changes in comments

### For Database Changes
1. Modify schema in `data/init.sql`
2. Update `db_utils.py` with new queries/operations
3. Rebuild container: `docker-compose down -v && docker-compose up`
4. Verify data loads correctly

---

## 📚 External References

- **Anthropic Claude API** - https://docs.anthropic.com
- **Flask Documentation** - https://flask.palletsprojects.com
- **PostgreSQL EXPLAIN** - https://www.postgresql.org/docs/current/sql-explain.html
- **Autoresearch Pattern** - https://github.com/karpathy/autoresearch

---

## 🎓 Code Quality Standards

- ✅ Type hints used for function parameters
- ✅ Docstrings on all classes and key methods
- ✅ Error handling with try/except blocks
- ✅ Logging via `add_log()` helper
- ✅ Comments explain "why", not "what"
- ⚠️ No formal tests yet (good first contribution!)

---

## 🚀 Quick Reference

```bash
# Start everything
run.bat (Windows) or ./run.sh (Linux/macOS)

# Access services
Flask API:    http://localhost:5000
PostgreSQL:   localhost:5432 (from terminal: docker-compose exec postgres psql ...)

# Stop everything
docker-compose down  # Keep data
docker-compose down -v  # Reset data

# View logs
docker-compose logs postgres
cd backend && tail -f *.log (when implemented)

# Rebuild database
docker-compose down -v
docker-compose up
```

---

## 🎯 Future Enhancements

High-value additions:
1. **Real index creation** - Actually apply recommendations safely
2. **Test suite** - Unit & integration tests with pytest
3. **Database snapshots** - A/B test before/after performance
4. **Monitoring integration** - Grafana dashboard
5. **Audit logging** - Track all optimization changes
6. **Query templates** - Save and reuse optimization patterns
7. **Team collaboration** - Share findings across DBAs
8. **Cost analysis** - Estimate infrastructure savings

---

**Last Updated:** 2026-06-09  
**Created For:** Singapore Banking Group Ops & Technology  
**Owner:** Development Team
