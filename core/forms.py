from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Get the configured user model - follows DRY principle
User = get_user_model()

class RegisterForm(UserCreationForm):
    """
    User registration form.
    Follows SRP: Only handles user registration and validation.
    Applies DRY: Reuses Django's built-in UserCreationForm.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling to all fields - DRY principle
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    """
    User login form.
    Follows SRP: Only handles authentication validation.
    Applies KISS: Simple, clear field definitions.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label="Password", 
        strip=False, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )


class FreelancerProfileForm(forms.Form):
    """
    Freelancer profile form.
    Follows SRP: Only handles freelancer profile data.
    Applies DRY: Consistent field styling and validation patterns.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g: Python, Django, JavaScript (comma separated)'
        }),
        help_text="Separate skills with commas"
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5, 
            'placeholder': 'Tell us about your experience...'
        }),
        max_length=1000,
        help_text="Maximum 1000 characters"
    )

    def clean_skills(self):
        """
        Validates and processes skills.
        Applies business rule: Maximum 20 skills allowed.
        """
        skills_str = self.cleaned_data.get('skills', '')
        if not skills_str.strip():
            return []
        
        skills_list = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
        if len(skills_list) > 20:
            raise ValidationError("You cannot have more than 20 skills")
        
        return skills_list


class ClientProfileForm(forms.Form):
    """
    Client profile form.
    Follows SRP: Only handles client profile data.
    Applies DRY: Reuses styling patterns from other profile forms.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    company = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Company name'
        })
    )
    billing_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Billing email'
        }),
        help_text="Email for billing purposes (optional)"
    )


class ServiceForm(forms.Form):
    """
    Service creation and editing form.
    Follows SRP: Only handles service data validation.
    Applies KISS: Clear field definitions with consistent styling.
    """
    CATEGORY_CHOICES = [
        ('WEB_DEVELOPMENT', 'Web Development'),
        ('MOBILE_DEVELOPMENT', 'Mobile Development'),
        ('DESIGN', 'Design'),
        ('WRITING', 'Writing'),
        ('MARKETING', 'Marketing'),
        ('CONSULTING', 'Consulting'),
        ('OTHER', 'Other'),
    ]
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Service title'
        }),
        help_text="A clear and descriptive title for your service"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5,
            'placeholder': 'Describe your service in detail...'
        }),
        help_text="Explain what your service includes, methodology, etc."
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'step': '0.01',
            'placeholder': '0.00'
        }),
        help_text="Price in USD"
    )
    delivery_time = forms.IntegerField(
        min_value=1,
        max_value=365,
        initial=7,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '7'
        }),
        help_text="Delivery time in days"
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Category that best describes your service"
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text="Check to make service visible to public"
    )
    
    def clean_title(self):
        """Validates title length - business rule: minimum 10 characters"""
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters long")
        return title
    
    def clean_description(self):
        """Validates description length - business rule: minimum 50 characters"""
        description = self.cleaned_data.get('description')
        if len(description) < 50:
            raise ValidationError("Description must be at least 50 characters long")
        return description


class ProjectForm(forms.Form):
    """
    Project creation and editing form.
    Follows SRP: Only handles project data validation.
    Applies KISS: Simple fields with consistent styling.
    """
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Project title'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Describe your project in detail...'
        })
    )
    budget = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        }),
        help_text="Optional budget in USD"
    )
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Optional deadline"
    )
    
    def clean_title(self):
        """Validates title length - business rule: minimum 10 characters"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 10:
            raise ValidationError("Title must be at least 10 characters long")
        return title
    
    def clean_description(self):
        """Validates description length - business rule: minimum 50 characters"""
        description = self.cleaned_data.get('description')
        if description and len(description) < 50:
            raise ValidationError("Description must be at least 50 characters long")
        return description
    
    def clean_budget(self):
        """Validates budget - business rule: must be positive"""
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise ValidationError("Budget must be greater than 0")
        return budget


class ProjectApplicationForm(forms.Form):
    """
    Form for freelancers to apply to projects.
    Follows SRP: Only handles project application data.
    """
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell the client why you are the best for this project...'
        }),
        help_text="Optional message to the client"
    )

class MentorshipSessionForm(forms.Form):
    """
    Form for scheduling mentorship sessions.
    Follows SRP: Only handles mentorship session data.
    """
    topic = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Session topic'
        }),
        help_text="Briefly describe the topic of the mentorship session"
    )
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text="Select date and time for the session"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Any specific areas you want to focus on...'
        }),
        help_text="Optional notes for the session"
    )