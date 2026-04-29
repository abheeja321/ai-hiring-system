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
