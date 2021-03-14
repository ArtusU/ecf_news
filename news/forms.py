from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.db.models import manager
from django.forms import fields
from .models import CustomUser, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CategoryForm(forms.ModelForm):
    #writers = forms.ModelMultipleChoiceField(queryset=User.objects.filter(userprofile__user_type='Writer'))
    managers = forms.ModelMultipleChoiceField(queryset=User.objects.filter(userprofile__user_type='Manager'))
    class Meta:
        model = Category
        fields = ['name', 'managers', 'writers']

    
    def clean(self):
        data = self.cleaned_data

        writers = data.get('writers', None)
        managers = data.get('managers', None)

        if writers is None:
            raise forms.ValidationError("Please select a writer")
        if managers is None:
            raise forms.ValidationError("Please select a manager")

        managers_check = writers.filter(userprofile__user_type='Manager')
        if managers_check.count() != managers.count():
            raise forms.ValidationError('Please ensure all the users are managers')

        '''
        writers_check = writers.filter(userprofile__user_type='Writer')
        if writers_check.count() != writers.count():
            raise forms.ValidationError('Please ensure all the users are valid writers')
        '''
        
