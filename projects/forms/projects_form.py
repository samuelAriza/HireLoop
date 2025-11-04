from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from ..models import Project, ProjectAssignment, ProjectApplication
from core.mixins.forms import BootstrapStylingMixin


class ProjectCreateForm(BootstrapStylingMixin, forms.ModelForm):
    """
    Form for creating a new project by a client.
    """
    image = forms.ImageField(
        label=_("Project Image"),
        required=False,
        help_text=_("Optional. Upload a relevant image (JPEG, PNG, GIF). Max 5MB.")
    )

    class Meta:
        model = Project
        fields = ["title", "description", "budget", "image"]
        labels = {
            "title": _("Project Title"),
            "description": _("Description"),
            "budget": _("Budget (USD)"),
        }
        help_texts = {
            "title": _("A clear and descriptive title for your project."),
            "description": _("Explain what you need, requirements, and deliverables."),
            "budget": _("Total budget in USD. This is the maximum you’re willing to pay."),
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("e.g., Build a responsive website")}),
            "description": forms.Textarea(attrs={"rows": 6, "placeholder": _("Detailed project description...")}),
            "budget": forms.NumberInput(attrs={"min": "5", "step": "0.01"}),
        }


class ProjectUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    """
    Form for updating an existing project (client or admin).
    """
    image = forms.ImageField(
        label=_("Update Project Image"),
        required=False,
        help_text=_("Optional. Upload a new image to replace the current one.")
    )

    class Meta:
        model = Project
        fields = ["title", "description", "budget", "status", "image"]
        labels = {
            "title": _("Project Title"),
            "description": _("Description"),
            "budget": _("Budget (USD)"),
            "status": _("Status"),
        }
        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 6}),
            "budget": forms.NumberInput(attrs={"min": "5", "step": "0.01"}),
            "status": forms.Select(choices=Project.ProjectStatus.choices),
        }


class ProjectAssignmentForm(BootstrapStylingMixin, forms.ModelForm):
    """
    Form for assigning a freelancer to a project.
    Validates that agreed payment does not exceed project budget.
    """
    class Meta:
        model = ProjectAssignment
        fields = ["freelancer", "role", "agreed_payment"]
        labels = {
            "freelancer": _("Freelancer"),
            "role": _("Role"),
            "agreed_payment": _("Agreed Payment (USD)"),
        }
        widgets = {
            "freelancer": forms.Select(attrs={"class": "form-select"}),
            "role": forms.TextInput(attrs={"placeholder": _("e.g., Frontend Developer")}),
            "agreed_payment": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }

    def __init__(self, *args, project=None, **kwargs):
        self.project = project
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        agreed_payment = cleaned_data.get("agreed_payment")

        if self.project and agreed_payment is not None:
            if agreed_payment > self.project.budget:
                raise forms.ValidationError(
                    _("Agreed payment cannot exceed the project's total budget of $%(budget)s."),
                    params={"budget": self.project.budget},
                )
        return cleaned_data


class ProjectAssignmentUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    """
    Form for updating an existing project assignment.
    Ensures updated payment doesn't exceed available budget.
    """
    class Meta:
        model = ProjectAssignment
        fields = ["role", "agreed_payment", "status"]
        labels = {
            "role": _("Role"),
            "agreed_payment": _("Agreed Payment (USD)"),
            "status": _("Status"),
        }
        widgets = {
            "role": forms.TextInput(),
            "agreed_payment": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "status": forms.Select(choices=ProjectAssignment.ProjectAssignmentStatus.choices),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_payment = cleaned_data.get("agreed_payment")
        assignment = self.instance

        if not assignment.pk:
            return cleaned_data  # New assignment, skip budget check

        project = assignment.project
        old_payment = assignment.agreed_payment or Decimal("0.00")
        available_budget = project.budget - (project.total_assigned_payments() - old_payment)

        if new_payment is not None and new_payment > available_budget:
            raise forms.ValidationError(
                _("Cannot update payment. Available budget: $%(available)s"),
                params={"available": available_budget},
            )

        return cleaned_data


class ProjectApplicationForm(BootstrapStylingMixin, forms.ModelForm):
    """
    Form for freelancers to apply to a project.
    """
    class Meta:
        model = ProjectApplication
        fields = ["cover_letter", "proposed_payment"]
        labels = {
            "cover_letter": _("Cover Letter"),
            "proposed_payment": _("Proposed Payment (USD)"),
        }
        help_texts = {
            "cover_letter": _("Explain why you're the best fit for this project."),
            "proposed_payment": _("Your proposed compensation for completing the work."),
        }
        widgets = {
            "cover_letter": forms.Textarea(attrs={"rows": 5, "placeholder": _("Tell us about your experience...")}),
            "proposed_payment": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }

    def __init__(self, *args, project=None, **kwargs):
        self.project = project
        super().__init__(*args, **kwargs)

    def clean_proposed_payment(self):
        proposed_payment = self.cleaned_data["proposed_payment"]
        if self.project and proposed_payment > self.project.budget:
            raise forms.ValidationError(
                _("Your proposal exceeds the project budget of $%(budget)s."),
                params={"budget": self.project.budget},
            )
        return proposed_payment