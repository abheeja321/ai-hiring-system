from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import AIArtifact, CandidateProfile, HiringRun, JobProfile, ScreeningInteraction
from .serializers import (
    AIArtifactSerializer,
    CandidateProfileSerializer,
    HiringRunSerializer,
    JobProfileSerializer,
    PipelineRunRequestSerializer,
    ScreeningInteractionSerializer,
)
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text
from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline


class JobProfileViewSet(viewsets.ModelViewSet):
    queryset = JobProfile.objects.all().order_by("-created_at")
    serializer_class = JobProfileSerializer


class CandidateProfileViewSet(viewsets.ModelViewSet):
    queryset = CandidateProfile.objects.all().order_by("-created_at")
    serializer_class = CandidateProfileSerializer


class HiringRunViewSet(viewsets.ModelViewSet):
    queryset = HiringRun.objects.all().order_by("-created_at")
    serializer_class = HiringRunSerializer

    @action(detail=False, methods=["post"])
    def run_pipeline(self, request):
        serializer = PipelineRunRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            job_title = data["job_title"]
            job_description = data["job_description"]
            candidate_name = data["candidate_name"]
            resume_text = data.get("resume_text", "")

            structured_job = parse_job_description(job_title, job_description)
            structured_resume = parse_resume_text(candidate_name, resume_text)

            job = JobProfile.objects.create(
                title=job_title,
                raw_description=job_description,
                structured_profile=structured_job,
            )
            candidate = CandidateProfile.objects.create(
                full_name=candidate_name,
                raw_resume=resume_text,
                structured_profile=structured_resume,
            )

            result = run_hiring_pipeline(structured_resume, structured_job)
            
            hiring_run = HiringRun.objects.create(
                candidate=candidate,
                job=job,
                ats_score=result["ats"]["final_score"],
                screening_score=result["screening"]["screening_score"],
                interview_score=result["interview"]["interview_score"],
                behavior_score=result["behavior"]["behavior_score"],
                final_score=result["decision"]["final_score"],
                decision=result["decision"]["decision"],
                explanation=result,
            )

            AIArtifact.objects.create(
                artifact_type="pipeline_result",
                candidate=candidate,
                job=job,
                payload=result,
                model_version="api-v1",
            )

            response_data = HiringRunSerializer(hiring_run).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIArtifact.objects.all().order_by("-created_at")
    serializer_class = AIArtifactSerializer


class ScreeningInteractionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScreeningInteraction.objects.all().order_by("-created_at")
    serializer_class = ScreeningInteractionSerializer
