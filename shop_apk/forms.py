from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, inlineformset_factory
from django import forms
from shop_apk.models import Profile, Product, Image
from django.contrib.auth.models import User



class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password1'])
        return user.save()


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']





