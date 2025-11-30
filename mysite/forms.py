from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": (
                "w-full pl-10 pr-4 py-2.5 rounded-xl "
                "bg-white/90 text-gray-800 "
                "border border-gray-300 "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
                "transition"
            ),
            "placeholder": "Enter your username",
            "autocomplete": "username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": (
                "w-full pl-10 pr-4 py-2.5 rounded-xl "
                "bg-white/90 text-gray-800 "
                "border border-gray-300 "
                "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
                "transition"
            ),
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        })
    )
