from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django import forms
from .models import Task, Project

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # przekazanie niestandardowych komunikatów walidacji
        self.fields['password1'].error_messages = {
            'password_too_short': 'Hasło musi zawierać przynajmniej 8 znaków.',
            'password_common': 'Hasło nie może być powszechnie używanym hasłem.',
            'password_entirely_numeric': 'Hasło nie może składać się wyłącznie z cyfr.',
            'password_too_similar': 'Hasło nie może być zbyt podobne do innych danych osobowych.'
        }
        # Ustawienie niestandardowych komunikatów walidacji dla pola 'username'
        self.fields['username'].error_messages = {
            'unique': _("Ta nazwa użytkownika jest już zajęta."),
            'invalid': _("Nazwa użytkownika może zawierać tylko litery, cyfry oraz znaki @/./+/-/_."),
            'max_length': _("Nazwa użytkownika może zawierać maksymalnie 150 znaków.")
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'priority', 'assigned_to']

class ProjectForm(forms.ModelForm):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date']
