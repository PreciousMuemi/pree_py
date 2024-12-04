from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import Skill
from django.views.generic import TemplateView

User = get_user_model()

class SkillSwapUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$', 
                'Enter a valid username. Alphanumeric characters and @/./+/-/_ only.'
            )
        ]
    )
    email = forms.EmailField(
        required=True,
        help_text="A valid email is required for account verification"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'location')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class ProfileCompletionForm(forms.ModelForm):
    skills_offered = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select skills you can teach"
    )
    skills_desired = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select skills you want to learn"
    )

    class Meta:
        model = User
        fields = ['bio', 'location', 'profile_picture', 'skills_offered', 'skills_desired']
