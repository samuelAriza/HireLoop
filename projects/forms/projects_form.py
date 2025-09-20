from django import forms
from ..models import Project, ProjectAssignment
from core.mixins.forms import BootstrapStylingMixin 

class ProjectCreateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget']

class ProjectUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'budget', 'status']
        widgets = {
            'status': forms.Select(choices=Project.ProjectStatus.choices)
        }

class ProjectAssignmentForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ['freelancer', 'role', 'agreed_payment']

class ProjectAssignmentUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ['role', 'agreed_payment', 'status']
        widgets = {
            'status': forms.Select(choices=ProjectAssignment.ProjectAssignmentStatus.choices)
        }