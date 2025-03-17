from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=32, widget=forms.TextInput(attrs={
        'class':'input','placeholder':'username/email'
    }))
    password = forms.CharField(label='password',min_length=6, widget=forms.PasswordInput(attrs={
        'class':'input','placeholder':'password'
    }))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('Username and password cannot be the same!')
        return password


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=32, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'email'
    }))
    password = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'password'
    }))
    password_1 = forms.CharField(label='Confirm Password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'password'
    }))

    class Meta:
        model = User
        fields = ('email','password')

    def clean_email(self):
        """Verify that the user exists"""
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('The user name already exists!')
        return email

    def clean_password_1(self):
        """Verify that passwords are the same"""
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_1'):
            raise forms.ValidationError("Two different passwords entered.")
        return self.cleaned_data['password_1']

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='Please enter your registered email address', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'email address'
    }))

class ModifyPwdForm(forms.Form):
    """Reset password form"""
    password = forms.CharField(label="Enter new password", min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'enter password'}))


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input', 'readonly': 'readonly'
    }))

    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """Form definition for UserInfo."""

    class Meta:
        """Meta definition for UserInfo form."""

        model = UserProfile
        fields = ('nike_name', 'desc', 'character_signature', 'birthday', 'gender', 'address', 'image')