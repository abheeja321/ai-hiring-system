from django import forms


class DemoPipelineForm(forms.Form):
    job_title = forms.CharField(max_length=255, initial="Software Engineer", widget=forms.HiddenInput())
    candidate_name = forms.CharField(max_length=255, initial="Applicant", widget=forms.HiddenInput())
    job_description = forms.CharField(widget=forms.HiddenInput(), initial="Looking for a software engineer.")
    resume_file = forms.FileField(required=True, label="Upload Resume (PDF/DOCX/TXT)")

    def clean(self):
        cleaned_data = super().clean()
        resume_file = cleaned_data.get("resume_file")
        if not resume_file:
            raise forms.ValidationError("Please upload a resume file.")
        return cleaned_data
