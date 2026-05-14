from django.db import models


class JobProfile(models.Model):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    raw_description = models.TextField()
    structured_profile = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class CandidateProfile(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    raw_resume = models.TextField()
    structured_profile = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Consent and Governance
    consent_given = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(null=True, blank=True)
    data_retention_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class HiringRun(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    ats_score = models.FloatField(default=0.0)
    screening_score = models.FloatField(default=0.0)
    interview_score = models.FloatField(default=0.0)
    behavior_score = models.FloatField(default=0.0)
    final_score = models.FloatField(default=0.0)
    decision = models.CharField(max_length=64, default="REVIEW")
    explanation = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AIArtifact(models.Model):
    artifact_type = models.CharField(max_length=100)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(JobProfile, on_delete=models.CASCADE, null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    model_version = models.CharField(max_length=100, default="v1")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Secure Storage
    is_encrypted = models.BooleanField(default=False)
    encryption_key_id = models.CharField(max_length=255, blank=True)


class ScreeningInteraction(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=100)
    question_category = models.CharField(max_length=100, blank=True)
    transcript_text = models.TextField(blank=True)
    normalized_text = models.TextField(blank=True)
    confidence_level = models.FloatField(default=0.0)
    interaction_timestamp = models.DateTimeField()
    answer_payload = models.JSONField(default=dict, blank=True)
    scoring_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Secure Storage
    is_encrypted = models.BooleanField(default=False)
    encryption_key_id = models.CharField(max_length=255, blank=True)


class AIAuditLog(models.Model):
    """
    Audit trail for AI decisions, scorings, and artifact access to ensure compliance.
    """
    run_id = models.CharField(max_length=255, blank=True)
    action = models.CharField(max_length=255)
    actor = models.CharField(max_length=255, default="SYSTEM")
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"{self.action} by {self.actor} at {self.timestamp}"
