from django import forms
from .models import Student,Folder
from django.contrib.auth.models import User


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
