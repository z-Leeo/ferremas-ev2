from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.')
    email = forms.EmailField(max_length=254, help_text='Requerido. Dirección de email válida.')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text='Requerido. Al menos 8 caracteres y no puede ser solo numérico.')
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text='Repetir la misma contraseña para verificar.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# forms.py
from django import forms
from django.contrib.auth.models import User, Group

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True, role=None):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if role:
                group = Group.objects.get(name=role)
                user.groups.add(group)
        return user
