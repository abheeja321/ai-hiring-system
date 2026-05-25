# AI Monitoring & Observability Code Designs

As requested, here are the code implementations for the AI Monitoring & Observability plan. You can integrate these into your existing codebase when ready.

## 1. Logging Structure Configuration

### `config/settings.py` (Logging Setup)
Add this to configure JSON-structured logging for APIs, Models, and Errors.

```python
# config/settings.py
import os

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "api_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "ai_api.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "json",
        },
        "model_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "ai_model.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "json",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "ai_error.log",
            "level": "ERROR",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "json",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "zecpath_ai.api": {
            "handlers": ["api_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "zecpath_ai.model": {
            "handlers": ["model_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "zecpath_ai.error": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        }
    },
}
```

### `ai/utils/logging.py` (Structured Logger Setup)

```python
# ai/utils/logging.py
import logging

def get_api_logger():
    return logging.getLogger("zecpath_ai.api")

def get_model_logger():
    return logging.getLogger("zecpath_ai.model")

def get_error_logger():
    return logging.getLogger("zecpath_ai.error")

def log_model_output(model_name: str, execution_time_ms: float, success: bool, details: dict = None):
    logger = get_model_logger()
    logger.info(
        f"Model execution: {model_name}",
        extra={
            "model": model_name,
            "execution_time_ms": execution_time_ms,
            "success": success,
            "details": details or {}
        }
    )
```

---

## 2. Key Metrics & Alert Models

### `apps/core/models.py` (Monitoring Models)

```python
# apps/core/models.py
from django.db import models

class AIMetric(models.Model):
    """Stores key performance indicators for the AI system."""
    METRIC_TYPES = [
        ('response_time', 'Response Time (ms)'),
        ('accuracy', 'Accuracy Score'),
        ('failure_rate', 'Failure Rate (%)'),
    ]
    
    metric_name = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField(default=dict, blank=True, help_text="e.g., {'model': 'v1', 'pipeline_step': 'screening'}")

    def __str__(self):
        return f"{self.metric_name}: {self.value} at {self.timestamp}"


class SystemAlert(models.Model):
    """Stores triggered alerts based on metric rules."""
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    rule_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='medium')
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.severity.upper()}] {self.rule_name} - {self.is_resolved}"
```

---

## 3. Alerting Rules Engine

### `apps/core/alerts.py`

```python
# apps/core/alerts.py
from .models import AIMetric, SystemAlert

def check_thresholds_and_alert():
    """Evaluate recent metrics and create alerts if thresholds are breached."""
    
    # Rule 1: High Response Time (e.g., > 5000ms)
    recent_slow_responses = AIMetric.objects.filter(
        metric_name='response_time', 
        value__gt=5000
    ).order_by('-timestamp')[:5]
    
    if recent_slow_responses.exists():
        SystemAlert.objects.create(
            rule_name="High Response Time",
            severity="high",
            message=f"Detected response times exceeding 5000ms. Latest value: {recent_slow_responses.first().value}ms"
        )
        
    # Rule 2: Model Accuracy Drop (e.g., < 0.7)
    recent_accuracy = AIMetric.objects.filter(
        metric_name='accuracy'
    ).order_by('-timestamp').first()
    
    if recent_accuracy and recent_accuracy.value < 0.7:
        SystemAlert.objects.create(
            rule_name="Low Model Accuracy",
            severity="critical",
            message=f"Model accuracy dropped below 0.7 threshold. Current: {recent_accuracy.value}"
        )
```

---

## 4. Monitoring Dashboard Structure

### `apps/dashboard/views.py` (Dashboard Logic)

```python
# apps/dashboard/views.py
from django.shortcuts import render
from django.db.models import Avg, Count
from zecpath_hiring.apps.core.models import AIMetric, SystemAlert, HiringRun

def observability_dashboard(request):
    """Renders the AI Monitoring Dashboard."""
    
    # 1. Candidate Processing Stats
    total_runs = HiringRun.objects.count()
    success_runs = HiringRun.objects.filter(decision='HIRE').count()
    success_rate = (success_runs / total_runs * 100) if total_runs > 0 else 0

    # 2. Key Metrics Aggregation
    avg_response_time = AIMetric.objects.filter(metric_name='response_time').aggregate(Avg('value'))['value__avg'] or 0
    avg_accuracy = AIMetric.objects.filter(metric_name='accuracy').aggregate(Avg('value'))['value__avg'] or 0
    
    # 3. Active Alerts
    active_alerts = SystemAlert.objects.filter(is_resolved=False).order_by('-created_at')[:10]

    context = {
        'total_runs': total_runs,
        'success_rate': round(success_rate, 2),
        'avg_response_time': round(avg_response_time, 2),
        'avg_accuracy': round(avg_accuracy, 2),
        'active_alerts': active_alerts,
    }
    return render(request, "dashboard/observability.html", context)
```

### `templates/dashboard/observability.html` (Dashboard UI)

```html
<!-- templates/dashboard/observability.html -->
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2>AI Observability Dashboard</h2>
    
    <div class="row mt-4">
        <!-- Candidate Processing Stats -->
        <div class="col-md-3">
            <div class="card bg-light">
                <div class="card-body">
                    <h5>Total Processed</h5>
                    <h3>{{ total_runs }}</h3>
                </div>
            </div>
        </div>
        <!-- Success Rate -->
        <div class="col-md-3">
            <div class="card bg-light">
                <div class="card-body">
                    <h5>Hire Rate</h5>
                    <h3>{{ success_rate }}%</h3>
                </div>
            </div>
        </div>
        <!-- Response Time -->
        <div class="col-md-3">
            <div class="card bg-light">
                <div class="card-body">
                    <h5>Avg Latency</h5>
                    <h3>{{ avg_response_time }} ms</h3>
                </div>
            </div>
        </div>
        <!-- Accuracy -->
        <div class="col-md-3">
            <div class="card bg-light">
                <div class="card-body">
                    <h5>Avg Accuracy</h5>
                    <h3>{{ avg_accuracy }}</h3>
                </div>
            </div>
        </div>
    </div>

    <!-- Active Alerts Table -->
    <div class="row mt-5">
        <div class="col-md-12">
            <h4>Active System Alerts</h4>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Rule</th>
                        <th>Severity</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    {% for alert in active_alerts %}
                    <tr class="{% if alert.severity == 'critical' %}table-danger{% elif alert.severity == 'high' %}table-warning{% endif %}">
                        <td>{{ alert.created_at|date:"Y-m-d H:i" }}</td>
                        <td>{{ alert.rule_name }}</td>
                        <td>{{ alert.severity|upper }}</td>
                        <td>{{ alert.message }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">No active alerts</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```
