from typing import List, Dict
from .models import SkillDomain, ExperienceLevel, QuestionType, Question

class DomainMapper:
    """
    Maps job roles to skill domains and fetches appropriate questions.
    """
    
    # Internal static question bank for Day 46 Architecture Blueprint
    _question_bank: List[Question] = [
        # MERN Stack - Basics
        Question(
            id="q_mern_basic_1",
            domain=SkillDomain.MERN,
            experience_level=ExperienceLevel.BASICS,
            question_type=QuestionType.CONCEPTUAL,
            text="Can you explain what the Virtual DOM is in React and how it improves performance?",
            expected_key_points=["In-memory representation", "Reconciliation", "Diffing algorithm", "Fewer actual DOM updates"],
            difficulty_score=3.0,
            follow_up_prompts=["How does React decide when to re-render a component?"]
        ),
        # MERN Stack - Intermediate
        Question(
            id="q_mern_inter_1",
            domain=SkillDomain.MERN,
            experience_level=ExperienceLevel.INTERMEDIATE,
            question_type=QuestionType.SCENARIO_BASED,
            text="If your Node.js/Express API is experiencing high latency under load, how would you diagnose and resolve it?",
            expected_key_points=["Profiling", "Database indexing", "Caching / Redis", "Event loop blocking", "Load balancing"],
            difficulty_score=6.5,
            follow_up_prompts=["How would you structure a Redis cache for frequently accessed but rarely changing data?"]
        ),
        # MERN Stack - Advanced
        Question(
            id="q_mern_adv_1",
            domain=SkillDomain.MERN,
            experience_level=ExperienceLevel.ADVANCED,
            question_type=QuestionType.SCENARIO_BASED,
            text="Design a scalable real-time collaborative code editor using MERN stack. Focus on state synchronization and handling network partitions.",
            expected_key_points=["WebSockets/Socket.io", "Operational Transformation / CRDTs", "Microservices", "State reconciliation", "Redis Pub/Sub"],
            difficulty_score=9.0,
            follow_up_prompts=["How would you handle conflicting edits from two users simultaneously disconnected and then reconnected?"]
        ),
        
        # General Experience Based
        Question(
            id="q_gen_exp_1",
            domain=SkillDomain.MERN, # Works for others too in a broader system
            experience_level=ExperienceLevel.INTERMEDIATE,
            question_type=QuestionType.EXPERIENCE_BASED,
            text="Walk me through the most technically challenging project on your resume. What was your specific architectural contribution?",
            expected_key_points=["Problem identification", "Architecture decisions", "Trade-offs", "Outcomes"],
            difficulty_score=5.0
        )
    ]

    @classmethod
    def get_questions_for_candidate(
        cls, 
        domain: SkillDomain, 
        experience: ExperienceLevel, 
        q_type: QuestionType,
        limit: int = 2
    ) -> List[Question]:
        """
        Retrieves a set of questions tailored to the candidate's exact domain and experience.
        """
        filtered = [
            q for q in cls._question_bank 
            if q.domain == domain 
            and q.experience_level == experience 
            and q.question_type == q_type
        ]
        return filtered[:limit]

    @staticmethod
    def map_job_role_to_domain(job_title: str) -> SkillDomain:
        """
        Maps a natural language job title to a specific technical skill domain.
        """
        title = job_title.lower()
        if "react" in title or "mern" in title or "node" in title:
            return SkillDomain.MERN
        if "java" in title or "spring" in title:
            return SkillDomain.JAVA
        if "python" in title or "django" in title or "flask" in title:
            return SkillDomain.PYTHON
        if "devops" in title or "sre" in title or "platform" in title:
            return SkillDomain.DEVOPS
        if "data" in title or "machine learning" in title:
            return SkillDomain.DATA_SCIENCE
            
        # Default fallback
        return SkillDomain.PYTHON
