from django.contrib import admin

from .models import AIArtifact, CandidateProfile, HiringRun, JobProfile

admin.site.register(JobProfile)
admin.site.register(CandidateProfile)
admin.site.register(HiringRun)
admin.site.register(AIArtifact)

