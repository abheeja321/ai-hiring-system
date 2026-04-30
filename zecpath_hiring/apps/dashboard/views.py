from django.shortcuts import render

from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text
from zecpath_hiring.ai.parsers.resume_reader import extract_uploaded_resume_text
from zecpath_hiring.apps.core.models import AIArtifact, CandidateProfile, HiringRun, JobProfile

from .forms import DemoPipelineForm


def dashboard_home(request):
    form = DemoPipelineForm()
    latest_runs = HiringRun.objects.select_related("candidate", "job").order_by("-created_at")[:10]
    return render(request, "dashboard/home.html", {"form": form, "latest_runs": latest_runs})


def run_demo_pipeline(request):
    context = {"form": DemoPipelineForm(request.POST or None, request.FILES or None)}
    if request.method == "POST" and context["form"].is_valid():
        data = context["form"].cleaned_data
        resume_file = data["resume_file"]
        resume_text = extract_uploaded_resume_text(resume_file)
        resume_source = f"uploaded_file:{resume_file.name}"

        structured_job = parse_job_description(data["job_title"], data["job_description"])
        structured_resume = parse_resume_text(data["candidate_name"], resume_text)
        structured_resume["resume_source"] = resume_source

        job = JobProfile.objects.create(
            title=data["job_title"],
            raw_description=data["job_description"],
            structured_profile=structured_job,
        )
        candidate = CandidateProfile.objects.create(
            full_name=data["candidate_name"],
            raw_resume=resume_text,
            structured_profile=structured_resume,
        )

        result = run_hiring_pipeline(structured_resume, structured_job)
        result["resume_source"] = resume_source
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
            model_version="demo-v1",
        )
        context.update(
            {
                "result": result,
                "resume_source": resume_source,
                "hiring_run": hiring_run,
                "latest_runs": HiringRun.objects.select_related("candidate", "job").order_by("-created_at")[:10],
            }
        )
        return render(request, "dashboard/results.html", context)

    context["latest_runs"] = HiringRun.objects.select_related("candidate", "job").order_by("-created_at")[:10]
    return render(request, "dashboard/home.html", context)


def job_search(request):
    query = request.GET.get("q", "")
    if query:
        jobs = JobProfile.objects.filter(title__icontains=query).order_by("-created_at")
    else:
        jobs = JobProfile.objects.all().order_by("-created_at")
    
    return render(request, "dashboard/job_search.html", {"jobs": jobs, "query": query})


def job_detail(request, pk):
    from django.shortcuts import get_object_or_404
    job = get_object_or_404(JobProfile, pk=pk)
    return render(request, "dashboard/job_detail.html", {"job": job})
