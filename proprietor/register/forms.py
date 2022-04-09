from django.contrib.auth import forms as auth_forms, get_user_model, password_validation
from django import forms

from proprietor.register.models import Profile

AppUserModel = get_user_model()


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': 'Password'}),
    )


class RegistrationForm(auth_forms.UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. A valid email address.',
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': 'Password confirmation'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = AppUserModel
        fields = ('email',)


class CreateProfileForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'birth_date',
            'gender',
            'picture',
            'phone_code',
            'phone',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}, )
        }
