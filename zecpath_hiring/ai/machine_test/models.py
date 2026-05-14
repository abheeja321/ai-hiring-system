from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MachineTestType(str, Enum):
    CODING = "Coding"
    DEBUGGING = "Debugging"
    FILE_BASED = "File-Based"
    SYSTEM_DESIGN = "System_Design"


class CodeSnapshot(BaseModel):
    """
    Represents a periodic capture of the candidate's code during the test.
    Used for evaluating problem-solving approach and iterative development.
    """
    timestamp_ms: float
    code_content: str
    lines_added: int = 0
    lines_removed: int = 0


class ExecutionResult(BaseModel):
    """
    Represents the output from a secure code execution sandbox.
    """
    timestamp_ms: float
    total_test_cases: int
    passed_test_cases: int
    execution_time_ms: float
    memory_used_kb: float
    stdout: str = ""
    stderr: str = ""
    is_final_submission: bool = False


class TestEvaluationReport(BaseModel):
    """
    The final aggregated report for a specific machine test.
    """
    task_id: str
    test_type: MachineTestType
    
    correctness_score: float = Field(ge=0.0, le=100.0)
    efficiency_score: float = Field(ge=0.0, le=100.0)
    code_quality_score: float = Field(ge=0.0, le=100.0)
    approach_score: float = Field(ge=0.0, le=100.0)
    
    time_penalty_applied: float = Field(ge=0.0, le=100.0)
    final_score: float = Field(ge=0.0, le=100.0)
    
    feedback: List[str] = Field(default_factory=list)
