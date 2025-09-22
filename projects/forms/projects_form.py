from django import forms
from ..models import Project, ProjectAssignment, ProjectApplication
from core.mixins.forms import BootstrapStylingMixin 

class ProjectCreateForm(BootstrapStylingMixin, forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'image']

class ProjectUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'status', 'image']
        widgets = {
            'status': forms.Select(choices=Project.ProjectStatus.choices)
        }

class ProjectAssignmentForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ['freelancer', 'role', 'agreed_payment']

    def clean(self):
        cleaned_data = super().clean()
        project = self.initial.get("project")
        agreed_payment = cleaned_data.get("agreed_payment")

        if project and agreed_payment and agreed_payment > project.budget:
            raise forms.ValidationError("Not enough budget for this project.")

        return cleaned_data


class ProjectAssignmentUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ['role', 'agreed_payment', 'status']
        widgets = {
            'status': forms.Select(choices=ProjectAssignment.ProjectAssignmentStatus.choices)
        }

    def clean(self):
        cleaned_data = super().clean()
        assignment = self.instance
        project = assignment.project
        new_payment = cleaned_data.get("agreed_payment")

        if project and new_payment:
            available = project.budget + (assignment.agreed_payment or 0)
            if new_payment > available:
                raise forms.ValidationError("Not enough budget to update this assignment.")

        return cleaned_data

class ProjectApplicationForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ProjectApplication
        fields = ['cover_letter', 'proposed_payment']