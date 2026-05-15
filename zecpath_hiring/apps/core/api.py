from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .models import AIArtifact, AIAuditLog, CandidateProfile, HiringRun, JobProfile, ScreeningInteraction
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
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = JobProfile.objects.all().order_by("-created_at")
    serializer_class = JobProfileSerializer


class CandidateProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = CandidateProfile.objects.all().order_by("-created_at")
    serializer_class = CandidateProfileSerializer


class HiringRunViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = HiringRun.objects.all().order_by("-created_at")
    serializer_class = HiringRunSerializer

    @action(detail=False, methods=["post"])
    def run_pipeline(self, request):
        serializer = PipelineRunRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
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

                AIAuditLog.objects.create(
                    run_id=str(hiring_run.id),
                    action="PIPELINE_RUN",
                    actor=request.user.username if request.user and request.user.is_authenticated else "SYSTEM",
                    details={"candidate": candidate_name, "job": job_title, "decision": result["decision"]["decision"]}
                )

                response_data = HiringRunSerializer(hiring_run).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                # Fallback API response for pipeline crashes
                return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = AIArtifact.objects.all().order_by("-created_at")
    serializer_class = AIArtifactSerializer


class ScreeningInteractionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = ScreeningInteraction.objects.all().order_by("-created_at")
    serializer_class = ScreeningInteractionSerializer
