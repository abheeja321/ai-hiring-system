# Machine Test AI Design Document

## 1. Overview
The Machine Test AI module is designed to evaluate real-world technical skills by analyzing code execution results, algorithmic efficiency, and problem-solving methodology (captured via code snapshots) rather than relying solely on multiple-choice or verbal Q&A.

## 2. Types of Machine Tests
The framework supports four primary test configurations:

1. **Coding Problems**: Traditional algorithmic or data structure challenges (e.g., LeetCode style). Requires strict test-case validation.
2. **Debugging Tasks**: Candidate is provided with a broken codebase and must identify and fix the logical/syntax errors to make the test suite pass.
3. **File-Based Tasks**: Candidate works on a small repository (e.g., building a REST API endpoint, refactoring a React component). Evaluated on file structure, linting, and functional tests.
4. **Mini System Design**: Candidate writes architecture specs or pseudo-code logic. Evaluated heuristically via LLM for coverage of key design principles (scalability, fault tolerance).

## 3. Input/Output Capture Mechanism
To accurately assess a candidate's *approach* rather than just the final result, the client IDE must capture and send two data streams:
- **Execution Results**: Sent every time the candidate clicks "Run" or "Submit". Contains boolean flags for test cases passed, runtime (ms), memory usage, stdout, and stderr.
- **Code Snapshots**: Captured periodically (e.g., every 30 seconds or upon significant code edits). This provides a time-series view of how the candidate built their solution.

## 4. Evaluation Metrics

### 4.1 Correctness
* **Metric**: Percentage of unit tests and hidden edge-case tests passed.
* **Weight**: High (Usually 40-50% of the final score).

### 4.2 Efficiency
* **Metric**: Time Complexity (Big-O analysis) and raw execution time/memory consumption compared to optimal benchmarks.
* **Weight**: Medium (20%). Penalizes brute-force solutions that pass correctness but fail scalability.

### 4.3 Code Quality
* **Metric**: Static analysis scoring. Looks for clean code practices: descriptive variable naming, presence of necessary comments, modularity, and adherence to language-specific conventions (e.g., PEP 8 for Python).
* **Weight**: Medium (20%).

### 4.4 Problem-Solving Approach
* **Metric**: Delta analysis across `CodeSnapshot`s.
* **Logic**: 
  - *Positive Signals*: Incremental development, writing helper functions before the main logic, frequent small successful test runs.
  - *Negative Signals*: Massive copy-paste dumps, erratic rewrites indicating guessing, or compiling only once at the very end.
* **Weight**: Low/Medium (10-20%). Serves as a strong differentiator between senior and junior developers.

## 5. Time-Based Scoring Logic
While tests have a hard timeout, candidates are also judged on speed relative to the "optimal" completion time.
* **Logic**: A decay function is applied to the final score if the candidate exceeds the optimal baseline.
* **Formula Example**: 
  - Optimal Time: 15 mins. Max Time: 30 mins.
  - If completed in <= 15 mins: No penalty.
  - If completed in > 15 mins: Score penalty scales linearly or logarithmically up to a maximum penalty (e.g., -15 points at 30 mins).
  - This ensures that a slow but perfect solution scores slightly lower than a fast and perfect solution, reflecting real-world proficiency.
