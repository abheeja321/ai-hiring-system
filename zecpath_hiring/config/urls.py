from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from zecpath_hiring.apps.dashboard.views import dashboard_home, run_demo_pipeline
from zecpath_hiring.apps.core.api import (
    JobProfileViewSet,
    CandidateProfileViewSet,
    HiringRunViewSet,
    AIArtifactViewSet,
    ScreeningInteractionViewSet,
)

router = DefaultRouter()
router.register(r"jobs", JobProfileViewSet)
router.register(r"candidates", CandidateProfileViewSet)
router.register(r"runs", HiringRunViewSet)
router.register(r"artifacts", AIArtifactViewSet)
router.register(r"interactions", ScreeningInteractionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_home, name="dashboard_home"),
    path("run-demo/", run_demo_pipeline, name="run_demo_pipeline"),
    path("api/v1/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

