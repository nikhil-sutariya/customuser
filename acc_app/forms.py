from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'phone', 'email']