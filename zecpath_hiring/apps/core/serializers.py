from rest_framework import serializers

from .models import AIArtifact, CandidateProfile, HiringRun, JobProfile, ScreeningInteraction


class JobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfile
        fields = "__all__"


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = "__all__"


class HiringRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringRun
        fields = "__all__"


class AIArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIArtifact
        fields = "__all__"


class ScreeningInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningInteraction
        fields = "__all__"


class PipelineRunRequestSerializer(serializers.Serializer):
    candidate_name = serializers.CharField(max_length=255)
    resume_text = serializers.CharField(required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=255)
    job_description = serializers.CharField()
