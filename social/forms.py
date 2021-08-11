from django.forms import ModelForm
from .models import Post

from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

 
from django.contrib.auth import get_user_model

User = get_user_model()
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username',]




class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['contents', 'image','access_level']
