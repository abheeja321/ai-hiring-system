import math
import re
from typing import List, Dict, Any, Optional
from .models import MachineTestType, CodeSnapshot, ExecutionResult, TestEvaluationReport


class MachineTestEvaluator:
    """
    Evaluates real-world technical machine tests by analyzing execution results, code quality,
    and the candidate's problem-solving approach.
    """
    
    def __init__(self):
        # Weights for the different scoring pillars (Correctness, Efficiency, Quality, Approach)
        self.WEIGHTS = {
            MachineTestType.CODING: (0.50, 0.20, 0.15, 0.15),
            MachineTestType.DEBUGGING: (0.60, 0.10, 0.10, 0.20),
            MachineTestType.FILE_BASED: (0.40, 0.10, 0.30, 0.20),
            MachineTestType.SYSTEM_DESIGN: (0.00, 0.40, 0.40, 0.20) # System design relies heavily on quality/efficiency heuristics
        }

    def evaluate_task(
        self, 
        task_id: str, 
        test_type: MachineTestType, 
        snapshots: List[CodeSnapshot], 
        executions: List[ExecutionResult],
        optimal_time_ms: float,
        optimal_memory_kb: float,
        target_duration_ms: float
    ) -> TestEvaluationReport:
        """
        Main evaluation flow for a single machine test task.
        """
        
        # 1. Correctness Score (Based on the final submission execution)
        correctness, is_passed = self.evaluate_correctness(executions)
        
        # 2. Efficiency Score (Based on runtime/memory against optimal benchmarks)
        efficiency = self.evaluate_efficiency(executions, optimal_time_ms, optimal_memory_kb)
        
        # 3. Code Quality Score (Heuristic static analysis)
        final_code = snapshots[-1].code_content if snapshots else ""
        quality = self.evaluate_code_quality(final_code)
        
        # 4. Problem-Solving Approach Score (Delta tracking)
        approach = self.evaluate_approach(snapshots, executions)
        
        # 5. Calculate Base Score based on task type weights
        c_wt, e_wt, q_wt, a_wt = self.WEIGHTS.get(test_type, self.WEIGHTS[MachineTestType.CODING])
        
        base_score = (correctness * c_wt) + (efficiency * e_wt) + (quality * q_wt) + (approach * a_wt)
        
        # 6. Apply Time-Based Penalty
        # Determine actual time taken based on first and last snapshot/execution
        actual_time_ms = 0.0
        if snapshots:
            actual_time_ms = snapshots[-1].timestamp_ms - snapshots[0].timestamp_ms
            
        penalty = self.calculate_time_penalty(target_duration_ms, actual_time_ms)
        
        final_score = max(0.0, min(100.0, base_score - penalty))
        
        # Generate Feedback
        feedback = self._generate_feedback(correctness, efficiency, quality, approach, penalty)
        
        return TestEvaluationReport(
            task_id=task_id,
            test_type=test_type,
            correctness_score=round(correctness, 2),
            efficiency_score=round(efficiency, 2),
            code_quality_score=round(quality, 2),
            approach_score=round(approach, 2),
            time_penalty_applied=round(penalty, 2),
            final_score=round(final_score, 2),
            feedback=feedback
        )

    def evaluate_correctness(self, executions: List[ExecutionResult]) -> tuple[float, bool]:
        """
        Calculates correctness based on test cases passed in the final submission.
        Returns a tuple of (score 0-100, is_fully_passed)
        """
        if not executions:
            return 0.0, False
            
        # Look for the final submission, or default to the last execution attempt
        final_exec = next((e for e in reversed(executions) if e.is_final_submission), executions[-1])
        
        if final_exec.total_test_cases <= 0:
            return 0.0, False
            
        ratio = final_exec.passed_test_cases / final_exec.total_test_cases
        score = ratio * 100.0
        
        # If there are syntax errors / stderr, penalize heavily
        if final_exec.stderr and score == 0.0:
            score = 10.0 # Minor points for attempting, but failed execution
            
        return score, (final_exec.passed_test_cases == final_exec.total_test_cases)

    def evaluate_efficiency(self, executions: List[ExecutionResult], optimal_time_ms: float, optimal_memory_kb: float) -> float:
        """
        Analyzes the execution time and memory usage relative to the optimal benchmark.
        """
        if not executions:
            return 0.0
            
        final_exec = next((e for e in reversed(executions) if e.is_final_submission), executions[-1])
        
        if optimal_time_ms <= 0 or optimal_memory_kb <= 0:
            return 100.0 # Can't evaluate without baseline
            
        # Time Score: 100 if faster than optimal, scales down logarithmically
        time_ratio = final_exec.execution_time_ms / optimal_time_ms
        time_score = 100.0
        if time_ratio > 1.0:
            # e.g., 2x slower = ~80 score, 5x slower = ~50 score
            time_score = max(0.0, 100.0 - (math.log(time_ratio) * 30.0))
            
        # Memory Score
        mem_ratio = final_exec.memory_used_kb / optimal_memory_kb
        mem_score = 100.0
        if mem_ratio > 1.0:
            mem_score = max(0.0, 100.0 - (math.log(mem_ratio) * 20.0))
            
        return (time_score * 0.6) + (mem_score * 0.4)

    def evaluate_code_quality(self, final_code: str) -> float:
        """
        Uses heuristic static analysis to determine code quality.
        In a full system, this would trigger an LLM or an external linter (like Pylint).
        """
        if not final_code.strip():
            return 0.0
            
        score = 100.0
        
        # Heuristic 1: Variable naming (penalize single-letter vars unless i, j, k)
        words = re.findall(r'\b[a-zA-Z_]\w*\b', final_code)
        bad_vars = [w for w in words if len(w) == 1 and w not in ('i', 'j', 'k', 'x', 'y', 'n')]
        score -= len(bad_vars) * 2.0
        
        # Heuristic 2: Lack of comments/docstrings
        if '#' not in final_code and '"""' not in final_code and '//' not in final_code:
            score -= 15.0
            
        # Heuristic 3: Overly long functions/lines (naive check)
        lines = final_code.split('\n')
        long_lines = sum(1 for line in lines if len(line) > 100)
        score -= long_lines * 1.5
        
        return max(0.0, min(100.0, score))

    def evaluate_approach(self, snapshots: List[CodeSnapshot], executions: List[ExecutionResult]) -> float:
        """
        Evaluates problem-solving methodology based on how the candidate arrived at the solution.
        """
        if len(snapshots) <= 1:
            return 40.0 # Penalize for giant copy-paste or lack of iteration
            
        score = 80.0 # Baseline for taking an iterative approach
        
        # 1. Frequency of execution attempts
        # Frequent small test runs are good, never running until the end is bad
        if len(executions) >= 3:
            score += 10.0
        elif len(executions) == 1:
            score -= 15.0
            
        # 2. Delta analysis (Detect massive copy-paste dumps)
        massive_dumps = 0
        for snap in snapshots:
            if snap.lines_added > 50 and snap.lines_removed == 0:
                massive_dumps += 1
                
        if massive_dumps > 0:
            score -= (massive_dumps * 20.0) # Heavy penalty for likely copy-pasting an entire solution
            
        return max(0.0, min(100.0, score))

    def calculate_time_penalty(self, target_duration_ms: float, actual_duration_ms: float) -> float:
        """
        Calculates a score penalty if the candidate exceeds the target time allocation.
        """
        if target_duration_ms <= 0 or actual_duration_ms <= target_duration_ms:
            return 0.0
            
        # Logarithmic penalty scaling
        # Example: Target 10 mins. Actual 15 mins (ratio 1.5). Penalty = log(1.5) * 20 = ~8 points
        overage_ratio = actual_duration_ms / target_duration_ms
        penalty = math.log(overage_ratio) * 20.0
        
        return min(25.0, penalty) # Cap the maximum time penalty to 25 points

    def _generate_feedback(self, c: float, e: float, q: float, a: float, p: float) -> List[str]:
        feedback = []
        if c == 100.0:
            feedback.append("Perfect correctness. All test cases passed.")
        elif c > 50.0:
            feedback.append("Partial correctness. Failed some edge cases.")
        else:
            feedback.append("Solution failed majority of test cases.")
            
        if e < 70.0:
            feedback.append("Solution is functionally correct but lacks optimization (high time/space complexity).")
            
        if a < 50.0:
            feedback.append("Approach flagged: Detected non-iterative development or massive code dumps.")
            
        if p > 5.0:
            feedback.append(f"Time penalty of -{round(p,1)} applied for exceeding optimal task duration.")
            
        return feedback
