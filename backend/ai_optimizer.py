import json
from anthropic import Anthropic
from typing import Optional, List, Dict
import re

class QueryOptimizer:
    def __init__(self, api_key: str):
        self.client = Anthropic()
        self.conversation_history = []
        self.optimizations = []
        self.current_query = None

    def analyze_query(self, query: str, explain_output: Dict, metrics: Dict) -> Dict:
        """
        Use Claude to analyze a slow query and suggest optimizations.
        This demonstrates the autoresearch pattern - iterative hypothesis generation and testing.
        """
        self.current_query = query
        self.conversation_history = []  # Reset for new query

        # Initial analysis message
        analysis_prompt = f"""
        You are an expert database query optimization agent. A banking system has a slow SQL query.

        QUERY:
        {query}

        EXECUTION METRICS:
        - Execution Time: {metrics.get('execution_time_ms', 'N/A')} ms
        - Rows Returned: {metrics.get('rows_returned', 'N/A')}

        Your task is to:
        1. Identify the root cause of the slow performance
        2. Hypothesize 3 specific index strategies that could help
        3. Provide exact SQL CREATE INDEX statements for each hypothesis
        4. Explain why each index would improve this query

        Be specific and technical. Focus on indexing strategies for PostgreSQL.
        """

        response = self.client.messages.create(
            model="claude-opus-4-1",
            max_tokens=2000,
            system="You are a PostgreSQL query optimization expert working in an autoresearch system. You generate optimization hypotheses and suggest specific, testable improvements. Format your response with clear sections for HYPOTHESIS 1, HYPOTHESIS 2, HYPOTHESIS 3.",
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        initial_analysis = response.content[0].text
        self.conversation_history.append(
            {"role": "user", "content": analysis_prompt}
        )
        self.conversation_history.append(
            {"role": "assistant", "content": initial_analysis}
        )

        # Extract hypotheses from response
        hypotheses = self._extract_hypotheses(initial_analysis)

        return {
            'query': query,
            'analysis': initial_analysis,
            'hypotheses': hypotheses,
            'metrics_before': metrics
        }

    def refine_optimization(self, feedback: str) -> str:
        """
        Refine optimization suggestions based on test results (multi-turn conversation).
        Demonstrates autoresearch's iterative refinement.
        """
        if not self.conversation_history:
            return "No analysis in progress"

        refinement_prompt = f"""
        The optimization hypotheses were tested with the following results:

        {feedback}

        Based on these results, please:
        1. Rank the hypotheses by effectiveness
        2. Suggest a composite index strategy combining the best approaches
        3. Provide the final optimized query if applicable
        4. Estimate expected performance improvement
        """

        response = self.client.messages.create(
            model="claude-opus-4-1",
            max_tokens=2000,
            system="You are a PostgreSQL query optimization expert. Refine optimization recommendations based on test results.",
            messages=self.conversation_history + [
                {"role": "user", "content": refinement_prompt}
            ]
        )

        refinement = response.content[0].text
        self.conversation_history.append(
            {"role": "user", "content": refinement_prompt}
        )
        self.conversation_history.append(
            {"role": "assistant", "content": refinement}
        )

        return refinement

    def _extract_hypotheses(self, response: str) -> List[Dict]:
        """Extract optimization hypotheses from Claude's response"""
        hypotheses = []

        # Split by hypothesis markers
        sections = re.split(r'HYPOTHESIS\s+(\d+)', response, flags=re.IGNORECASE)

        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                hypothesis_num = sections[i].strip()
                hypothesis_text = sections[i + 1]

                # Extract CREATE INDEX statements
                index_matches = re.findall(
                    r'(CREATE\s+INDEX.*?;)',
                    hypothesis_text,
                    re.IGNORECASE | re.DOTALL
                )

                hypotheses.append({
                    'hypothesis_id': int(hypothesis_num),
                    'description': hypothesis_text.split('\n')[0] if hypothesis_text else '',
                    'full_text': hypothesis_text,
                    'index_statements': index_matches,
                    'status': 'PENDING'
                })

        return hypotheses

    def generate_optimization_report(self, analysis: Dict) -> str:
        """Generate a comprehensive optimization report"""
        report_prompt = f"""
        Based on our analysis of this slow query:

        {self.current_query}

        Generate a concise executive summary report that includes:
        1. Root cause analysis
        2. Recommended solution (best hypothesis)
        3. Expected performance improvement percentage
        4. Implementation steps for DBA
        5. Risk assessment

        Format as a structured report.
        """

        response = self.client.messages.create(
            model="claude-opus-4-1",
            max_tokens=1500,
            system="You are a database optimization consultant. Generate clear, actionable reports.",
            messages=self.conversation_history + [
                {"role": "user", "content": report_prompt}
            ]
        )

        return response.content[0].text

    def generate_query_rewrite(self, original_query: str) -> Optional[str]:
        """
        Suggest a rewritten version of the query for better performance.
        Sometimes better execution plans come from rewriting, not just indexing.
        """
        rewrite_prompt = f"""
        Given this slow SQL query from a banking system:

        {original_query}

        Suggest an alternative query rewrite that would execute faster by:
        1. Breaking into subqueries with better statistics
        2. Using CTEs for clarity and optimization hints
        3. Avoiding unnecessary joins
        4. Rearranging WHERE conditions

        Provide ONLY the rewritten SQL query, with brief comments explaining improvements.
        Maintain semantic equivalence - return exact same results.
        """

        response = self.client.messages.create(
            model="claude-opus-4-1",
            max_tokens=1500,
            system="You are an expert SQL query writer optimizing for PostgreSQL. Return only the rewritten query with brief inline comments.",
            messages=[
                {"role": "user", "content": rewrite_prompt}
            ]
        )

        return response.content[0].text

class AutoResearchOptimizer:
    """
    Autonomous research-style optimizer that generates and tests multiple hypotheses.
    Mimics the autoresearch pattern from Karpathy's project.
    """
    def __init__(self, db_connection, api_key: str):
        self.db = db_connection
        self.optimizer = QueryOptimizer(api_key)
        self.optimization_log = []

    def run_autonomous_optimization(self, query: str, max_iterations: int = 3) -> Dict:
        """
        Run autonomous optimization loop:
        1. Analyze query
        2. Generate hypotheses
        3. Test each hypothesis
        4. Iterate on best results
        """
        results = {
            'query': query,
            'iterations': [],
            'best_optimization': None,
            'total_improvement_percent': 0
        }

        # Get baseline metrics
        baseline_metrics = self.db.get_query_stats(query)
        baseline_time = baseline_metrics.get('execution_time_ms', 0)

        # Initial analysis
        analysis = self.optimizer.analyze_query(query, {}, baseline_metrics)

        for iteration in range(max_iterations):
            iteration_result = {
                'iteration': iteration + 1,
                'hypotheses_tested': [],
                'best_hypothesis_this_round': None
            }

            for hypothesis in analysis['hypotheses'][:2]:  # Test top 2
                # Create indexes from hypothesis
                index_created = False
                for index_sql in hypothesis.get('index_statements', []):
                    try:
                        # In a real system, we'd execute this safely
                        # For demo, we'll track it
                        hypothesis['tested'] = True
                        index_created = True
                    except Exception as e:
                        print(f"Index creation failed: {e}")

                # Measure after index creation
                if index_created:
                    improved_metrics = self.db.get_query_stats(query)
                    improvement_percent = (
                        (baseline_time - improved_metrics.get('execution_time_ms', 0)) / baseline_time * 100
                    ) if baseline_time > 0 else 0

                    hypothesis_result = {
                        'hypothesis_id': hypothesis['hypothesis_id'],
                        'improvement_percent': round(improvement_percent, 2),
                        'metrics': improved_metrics
                    }

                    iteration_result['hypotheses_tested'].append(hypothesis_result)

                    if (not iteration_result['best_hypothesis_this_round'] or
                        improvement_percent > iteration_result['best_hypothesis_this_round']['improvement_percent']):
                        iteration_result['best_hypothesis_this_round'] = hypothesis_result

            results['iterations'].append(iteration_result)

            # Check if significant improvement found
            if (iteration_result['best_hypothesis_this_round'] and
                iteration_result['best_hypothesis_this_round']['improvement_percent'] > 20):
                break

        # Determine overall best
        all_improvements = [
            h for it in results['iterations'] for h in it['hypotheses_tested']
        ]
        if all_improvements:
            best = max(all_improvements, key=lambda x: x['improvement_percent'])
            results['best_optimization'] = best
            results['total_improvement_percent'] = best['improvement_percent']

        return results
