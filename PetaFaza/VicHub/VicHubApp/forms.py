from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.subscribed = 'N'
        user.status = 'A'
        user.type = 'U'
        if commit:
            user.save()
        return user
