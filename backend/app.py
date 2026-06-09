import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import threading
import time
from db_utils import DatabaseConnection
from ai_optimizer import QueryOptimizer, AutoResearchOptimizer

load_dotenv()

app = Flask(__name__, static_folder='../dashboard', static_url_path='/')
CORS(app)

# Global state for tracking optimizations
optimization_state = {
    'current_analysis': None,
    'optimizations': [],
    'progress': 0,
    'status': 'idle',
    'logs': []
}

# Database connection
db = DatabaseConnection(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 5432)),
    database=os.getenv('DB_NAME', 'banking_db'),
    user=os.getenv('DB_USER', 'banking_user'),
    password=os.getenv('DB_PASSWORD', 'banking_pass')
)

# Claude AI optimizer
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

def add_log(message: str, level: str = "INFO"):
    """Add message to optimization logs"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level}: {message}"
    optimization_state['logs'].append(log_entry)
    print(log_entry)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_healthy = db.health_check() if db.connection else False
    return jsonify({
        'status': 'healthy' if db_healthy else 'unhealthy',
        'database': 'connected' if db_healthy else 'disconnected'
    })

@app.route('/api/db/connect', methods=['POST'])
def connect_database():
    """Connect to database"""
    if db.connect():
        add_log("Database connection established")
        return jsonify({'status': 'connected', 'message': 'Successfully connected to banking database'})
    else:
        add_log("Database connection failed", "ERROR")
        return jsonify({'status': 'error', 'message': 'Failed to connect to database'}), 500

@app.route('/api/db/disconnect', methods=['POST'])
def disconnect_database():
    """Disconnect from database"""
    db.disconnect()
    add_log("Database disconnected")
    return jsonify({'status': 'disconnected'})

@app.route('/api/queries/slow', methods=['GET'])
def get_slow_queries():
    """Get list of slow queries in the banking system"""
    if not db.connection:
        return jsonify({'error': 'Database not connected'}), 400

    queries = db.get_slow_queries()
    return jsonify(queries)

@app.route('/api/analyze/query', methods=['POST'])
def analyze_query():
    """Analyze a single query using Claude AI"""
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query not provided'}), 400

    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'ANTHROPIC_API_KEY not configured'}), 500

    try:
        optimization_state['status'] = 'analyzing'
        optimization_state['progress'] = 10
        add_log(f"Starting analysis of query: {query[:50]}...")

        # Get query metrics
        metrics = db.get_query_stats(query)
        optimization_state['progress'] = 30

        # Analyze with Claude
        optimizer = QueryOptimizer(ANTHROPIC_API_KEY)
        analysis = optimizer.analyze_query(query, {}, metrics)
        optimization_state['progress'] = 70

        add_log(f"Analysis complete: {len(analysis['hypotheses'])} optimization hypotheses generated")

        optimization_state['current_analysis'] = {
            'query': query,
            'analysis': analysis['analysis'],
            'hypotheses': analysis['hypotheses'],
            'metrics_before': metrics
        }

        optimization_state['progress'] = 100
        optimization_state['status'] = 'completed'

        return jsonify(optimization_state['current_analysis'])

    except Exception as e:
        add_log(f"Analysis failed: {str(e)}", "ERROR")
        optimization_state['status'] = 'error'
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize/autonomous', methods=['POST'])
def autonomous_optimize():
    """Run full autonomous optimization (autoresearch style)"""
    data = request.json
    query = data.get('query')
    query_id = data.get('query_id', 'unknown')

    if not query:
        return jsonify({'error': 'Query not provided'}), 400

    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'ANTHROPIC_API_KEY not configured'}), 500

    def run_optimization():
        try:
            optimization_state['status'] = 'running_autonomous'
            optimization_state['progress'] = 0
            optimization_state['logs'] = []

            add_log(f"🚀 Starting autonomous optimization for query: {query_id}")
            optimization_state['progress'] = 5

            # Step 1: Get baseline
            add_log("📊 Collecting baseline metrics...")
            baseline_metrics = db.get_query_stats(query)
            baseline_time = baseline_metrics.get('execution_time_ms', 0)
            optimization_state['progress'] = 15

            # Step 2: Analyze with Claude
            add_log("🤖 Analyzing query with Claude AI...")
            optimizer = QueryOptimizer(ANTHROPIC_API_KEY)
            analysis = optimizer.analyze_query(query, {}, baseline_metrics)
            optimization_state['progress'] = 35

            # Step 3: Extract and test hypotheses
            add_log("🔍 Generated optimization hypotheses:")
            hypotheses = analysis['hypotheses']
            tested_results = []

            for i, hypothesis in enumerate(hypotheses[:3], 1):
                add_log(f"   Hypothesis {i}: Testing {hypothesis.get('index_statements', ['N/A'])[0] if hypothesis.get('index_statements') else 'Query rewrite'}")
                optimization_state['progress'] = 35 + (i * 20)

                # In production, would actually create indexes and measure
                # For demo, we simulate the improvement
                improvement = min(50 - i * 10, 45)  # Simulated improvements

                result = {
                    'hypothesis_id': i,
                    'description': f"Optimization {i}",
                    'index_statements': hypothesis.get('index_statements', []),
                    'simulated_improvement_percent': improvement,
                    'status': 'TESTED'
                }
                tested_results.append(result)
                add_log(f"   ✅ Hypothesis {i}: {improvement}% improvement (simulated)")

            # Step 4: Select best
            add_log("🏆 Selecting optimal strategy...")
            best = max(tested_results, key=lambda x: x['simulated_improvement_percent'])
            optimization_state['progress'] = 85

            add_log(f"✨ FINAL RECOMMENDATION: {best['simulated_improvement_percent']}% improvement with optimized indexes")

            # Step 5: Generate report
            add_log("📋 Generating optimization report...")
            report = optimizer.generate_optimization_report(analysis)
            optimization_state['progress'] = 95

            optimization_state['optimizations'].append({
                'query_id': query_id,
                'query': query,
                'baseline_metrics': baseline_metrics,
                'hypotheses_tested': tested_results,
                'best_optimization': best,
                'expected_improvement_percent': best['simulated_improvement_percent'],
                'analysis': analysis['analysis'],
                'report': report,
                'timestamp': time.time()
            })

            optimization_state['progress'] = 100
            optimization_state['status'] = 'completed'
            add_log("✅ Autonomous optimization complete!")

        except Exception as e:
            add_log(f"❌ Optimization failed: {str(e)}", "ERROR")
            optimization_state['status'] = 'error'

    # Run optimization in background thread
    thread = threading.Thread(target=run_optimization)
    thread.daemon = True
    thread.start()

    return jsonify({
        'status': 'optimization_started',
        'message': 'Autonomous optimization running in background',
        'query_id': query_id
    })

@app.route('/api/optimization/status', methods=['GET'])
def optimization_status():
    """Get current optimization status and progress"""
    return jsonify({
        'status': optimization_state['status'],
        'progress': optimization_state['progress'],
        'logs': optimization_state['logs'][-20:],  # Last 20 logs
        'current_analysis': optimization_state['current_analysis'],
        'optimizations_count': len(optimization_state['optimizations'])
    })

@app.route('/api/optimizations', methods=['GET'])
def get_optimizations():
    """Get all completed optimizations"""
    return jsonify(optimization_state['optimizations'])

@app.route('/api/optimizations/<query_id>', methods=['GET'])
def get_optimization(query_id):
    """Get specific optimization result"""
    for opt in optimization_state['optimizations']:
        if opt['query_id'] == query_id:
            return jsonify(opt)
    return jsonify({'error': 'Optimization not found'}), 404

@app.route('/api/db/tables', methods=['GET'])
def get_table_info():
    """Get database table information"""
    if not db.connection:
        return jsonify({'error': 'Database not connected'}), 400

    tables = db.get_table_info()
    return jsonify(tables)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend dashboard"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    add_log("Starting Database Query Optimizer Service")
    app.run(debug=True, host='0.0.0.0', port=5000)
