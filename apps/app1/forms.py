from django import forms
from .models import Student,Folder
from django.contrib.auth.models import User

from .models import Department, Profile
from django.apps import apps

import csv
import io
from django.shortcuts import render, redirect
from django.apps import apps
from django.http import HttpResponseBadRequest


class CSVImportForm(forms.Form):
    model = forms.ChoiceField(choices=[])
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_choices = []
        for model in apps.get_models():
            label = f"{model._meta.app_label}.{model.__name__}"
            model_choices.append((label, label))

        self.fields["model"].choices = model_choices


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'bio', 'avatar', 'barcode']
        widgets = {
            'department': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Select Department',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 resize-none',
                'rows': 4,
                'placeholder': 'Tell us something about yourself...',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-700 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'barcode': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'User Barcode',
            }),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border border-gray-300 rounded-md px-3 py-2 w-full',
                'rows': 4
            }),
        }

# Form to create User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'
    }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
        }

# Form to create Student
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'folder', 'middle_name', 'mobile_number', 'gender']
        widgets = {
            'user': forms.Select(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'folder': forms.Select(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'middle_name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'mobile_number': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
            'gender': forms.Select(attrs={'class': 'border border-gray-300 rounded-md px-3 py-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=False)
        self.fields['user'].required = False


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name', 'folder_capacity', 'floor_number']
        widgets = {
            'folder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'folder_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
