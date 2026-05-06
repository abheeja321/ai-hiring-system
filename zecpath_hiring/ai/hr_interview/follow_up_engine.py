from enum import Enum
import re

class FollowUpType(str, Enum):
    CLARIFICATION = "Clarification"
    DEEPENING = "Deepening"
    SCENARIO_BASED = "Scenario-based"
    SUFFICIENT = "Sufficient"


class FollowUpEngine:
    """
    Analyzes candidate responses using heuristics to determine if a follow-up is needed,
    and what type of follow-up it should be.
    """

    def __init__(self):
        # Basic heuristics markers
        self.vagueness_markers = ["stuff", "things", "did some", "worked on", "helped out", "was involved"]
        self.confidence_markers = ["successfully", "led", "managed", "achieved", "improved", "architected", "resolved"]
        self.structure_markers = [
            "situation",
            "task",
            "action",
            "result",
            "first",
            "then",
            "finally",
            "because",
            "measured",
            "outcome",
        ]
        self.detail_markers = [
            "percent",
            "%",
            "users",
            "customers",
            "stakeholders",
            "team",
            "deadline",
            "metrics",
            "reduced",
            "increased",
            "launched",
        ]
        
    def analyze_response(self, response_text: str) -> FollowUpType:
        """
        Determines the type of follow-up needed based on word count and keyword heuristics.
        """
        words = re.findall(r"\b[\w%.-]+\b", response_text)
        word_count = len(words)
        lower_response = response_text.lower()
        if word_count == 0:
            return FollowUpType.CLARIFICATION
        
        # 1. Check for extreme brevity or vagueness -> CLARIFICATION
        vague_count = sum(1 for marker in self.vagueness_markers if marker in lower_response)
        detail_count = sum(1 for marker in self.detail_markers if marker in lower_response)
        structure_count = sum(1 for marker in self.structure_markers if marker in lower_response)
        confidence_count = sum(1 for marker in self.confidence_markers if marker in lower_response)

        if word_count < 12:
            return FollowUpType.CLARIFICATION

        if vague_count > 1 and detail_count == 0:
            return FollowUpType.CLARIFICATION

        if word_count < 25 and detail_count == 0 and structure_count == 0:
            return FollowUpType.CLARIFICATION

        # 2. Check for high confidence and detail -> SCENARIO_BASED
        if word_count > 30 and confidence_count >= 2:
            return FollowUpType.SCENARIO_BASED

        # Complete structured answers should not receive a mechanical follow-up.
        if word_count >= 35 and structure_count >= 3 and detail_count >= 2:
            return FollowUpType.SUFFICIENT

        # 3. Standard response that might lack structural depth (STAR method) -> DEEPENING
        # If it's a medium length response without strong confident action verbs
        if 12 <= word_count <= 60:
            return FollowUpType.DEEPENING

        # 4. If none of the above, it's a comprehensive answer -> SUFFICIENT
        return FollowUpType.SUFFICIENT

    def get_follow_up_instruction(self, follow_up_type: FollowUpType, category_context: str) -> str:
        """
        Provides the LLM instruction on how to frame the follow-up question.
        """
        if follow_up_type == FollowUpType.CLARIFICATION:
            return "The candidate's previous answer was too brief or vague. Ask a direct clarifying question to get them to explain specifically what they did."
        elif follow_up_type == FollowUpType.DEEPENING:
            return "The candidate provided a basic answer. Probe deeper by asking for a specific example, or asking about the specific challenges they faced (focusing on the 'Action' and 'Result' of the STAR method)."
        elif follow_up_type == FollowUpType.SCENARIO_BASED:
            return f"The candidate gave a strong, confident answer regarding {category_context}. Test their adaptability by posing a 'What if' scenario related to their answer where things go wrong."
        
        return ""
