from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CandidateProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("raw_resume", models.TextField()),
                ("structured_profile", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="JobProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("department", models.CharField(blank=True, max_length=255)),
                ("raw_description", models.TextField()),
                ("structured_profile", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="AIArtifact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("artifact_type", models.CharField(max_length=100)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("model_version", models.CharField(default="v1", max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("candidate", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.candidateprofile")),
                ("job", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.jobprofile")),
            ],
        ),
        migrations.CreateModel(
            name="HiringRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ats_score", models.FloatField(default=0.0)),
                ("screening_score", models.FloatField(default=0.0)),
                ("interview_score", models.FloatField(default=0.0)),
                ("behavior_score", models.FloatField(default=0.0)),
                ("final_score", models.FloatField(default=0.0)),
                ("decision", models.CharField(default="REVIEW", max_length=64)),
                ("explanation", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.candidateprofile")),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.jobprofile")),
            ],
        ),
    ]

