import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import time

class DatabaseConnection:
    def __init__(self, host="localhost", port=5432, database="banking_db",
                 user="banking_user", password="banking_pass"):
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.conn_params)
            print("✅ Connected to PostgreSQL")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL")

    def execute_query(self, query: str, params=None) -> List[Dict]:
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Query execution error: {e}")
            return []

    def explain_query(self, query: str) -> Dict:
        """Get EXPLAIN PLAN for a query"""
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
            cursor.execute(explain_query)
            result = cursor.fetchone()
            cursor.close()
            return json.loads(result[0]) if result else {}
        except Exception as e:
            print(f"EXPLAIN error: {e}")
            return {}

    def get_query_stats(self, query: str) -> Dict:
        """Get execution statistics for a query"""
        try:
            start_time = time.time()
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            # Reset query stats
            cursor.execute("SELECT pg_stat_statements_reset();")

            # Execute query
            cursor.execute(query)
            results = cursor.fetchall()

            execution_time = (time.time() - start_time) * 1000  # ms
            row_count = len(results)

            cursor.close()

            return {
                'execution_time_ms': round(execution_time, 2),
                'rows_returned': row_count,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Stats collection error: {e}")
            return {'error': str(e)}

    def get_table_info(self) -> Dict:
        """Get information about tables and indexes"""
        query = """
        SELECT
            t.tablename,
            (SELECT count(*) FROM pg_indexes WHERE tablename = t.tablename) as index_count,
            (SELECT count(*) FROM information_schema.columns WHERE table_name = t.tablename) as column_count
        FROM pg_tables t
        WHERE schemaname = 'public'
        ORDER BY tablename;
        """
        return self.execute_query(query)

    def create_index(self, table: str, column: str, index_name: Optional[str] = None) -> bool:
        """Create an index on a column"""
        try:
            if not index_name:
                index_name = f"idx_{table}_{column}"

            query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column});"
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            print(f"✅ Index created: {index_name}")
            return True
        except Exception as e:
            print(f"❌ Index creation failed: {e}")
            return False

    def drop_index(self, index_name: str) -> bool:
        """Drop an index"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DROP INDEX IF EXISTS {index_name};")
            self.connection.commit()
            cursor.close()
            print(f"✅ Index dropped: {index_name}")
            return True
        except Exception as e:
            print(f"❌ Index drop failed: {e}")
            return False

    def get_slow_queries(self) -> List[Dict]:
        """Get a list of slow queries for optimization"""
        queries = [
            {
                'id': 'slow_q1',
                'name': 'Customer Transfer History',
                'description': 'Get all transfers for a customer in last 30 days',
                'query': """
                    SELECT c.name, a.account_id, t.transaction_id, t.amount, t.created_at
                    FROM customers c
                    JOIN accounts a ON c.customer_id = a.customer_id
                    JOIN transactions t ON a.account_id = t.from_account_id
                    WHERE c.customer_id = 1
                    AND t.created_at >= CURRENT_DATE - INTERVAL '30 days'
                    ORDER BY t.created_at DESC;
                """,
                'optimization_opportunity': 'Missing index on transactions.created_at and customer_id join path'
            },
            {
                'id': 'slow_q2',
                'name': 'Loan Payment Summary',
                'description': 'Aggregate loan payments by customer',
                'query': """
                    SELECT
                        c.customer_id, c.name,
                        COUNT(lp.payment_id) as total_payments,
                        SUM(lp.principal_paid) as total_principal,
                        SUM(lp.interest_paid) as total_interest
                    FROM customers c
                    JOIN loans l ON c.customer_id = l.customer_id
                    JOIN loan_payments lp ON l.loan_id = lp.loan_id
                    WHERE lp.status = 'COMPLETED'
                    GROUP BY c.customer_id, c.name
                    HAVING COUNT(lp.payment_id) > 0
                    ORDER BY total_principal DESC;
                """,
                'optimization_opportunity': 'Missing indexes on loan_payments.status and foreign keys'
            },
            {
                'id': 'slow_q3',
                'name': 'Fraud Detection - High Risk Transactions',
                'description': 'Find high-risk transactions by amount and customer velocity',
                'query': """
                    SELECT
                        fa.alert_id, fa.alert_type, fa.risk_score,
                        t.transaction_id, t.amount, t.created_at,
                        c.name, c.country_code
                    FROM fraud_alerts fa
                    JOIN transactions t ON fa.transaction_id = t.transaction_id
                    JOIN accounts a ON t.from_account_id = a.account_id
                    JOIN customers c ON a.customer_id = c.customer_id
                    WHERE fa.risk_score > 50
                    AND fa.status = 'PENDING'
                    AND t.created_at >= CURRENT_DATE - INTERVAL '7 days'
                    ORDER BY fa.risk_score DESC
                    LIMIT 100;
                """,
                'optimization_opportunity': 'Multiple table joins without indexes, missing composite indexes'
            },
            {
                'id': 'slow_q4',
                'name': 'Account Balance Verification',
                'description': 'Verify account balances with recent transactions',
                'query': """
                    SELECT
                        a.account_id, a.balance, a.currency,
                        COUNT(DISTINCT t.transaction_id) as recent_transactions,
                        SUM(CASE WHEN t.from_account_id = a.account_id THEN t.amount ELSE 0 END) as outflows
                    FROM accounts a
                    LEFT JOIN transactions t ON (a.account_id = t.from_account_id OR a.account_id = t.to_account_id)
                    WHERE t.created_at >= CURRENT_DATE - INTERVAL '90 days'
                    OR t.transaction_id IS NULL
                    GROUP BY a.account_id, a.balance, a.currency
                    ORDER BY outflows DESC;
                """,
                'optimization_opportunity': 'Missing indexes on transaction timestamp and account references'
            }
        ]

        # Collect actual metrics for each query
        for q in queries:
            stats = self.get_query_stats(q['query'])
            q['metrics'] = stats

        return queries

    def health_check(self) -> bool:
        """Check if database is healthy"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            return True
        except:
            return False
