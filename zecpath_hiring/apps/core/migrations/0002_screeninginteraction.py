from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScreeningInteraction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_id", models.CharField(max_length=100)),
                ("question_category", models.CharField(blank=True, max_length=100)),
                ("transcript_text", models.TextField(blank=True)),
                ("normalized_text", models.TextField(blank=True)),
                ("confidence_level", models.FloatField(default=0.0)),
                ("interaction_timestamp", models.DateTimeField()),
                ("answer_payload", models.JSONField(blank=True, default=dict)),
                ("scoring_payload", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.candidateprofile")),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.jobprofile")),
            ],
        ),
    ]
