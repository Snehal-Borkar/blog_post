from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import  SignUpForm
 
from django_oso.auth import authorize

from .models import Post,User
from .forms import PostForm

import random

# Create your views here.
 

def list_posts(request):
    
    posts = Post.objects.all().order_by('-created_at')
    public_posts = Post.objects.filter(access_level='0')
    authorized_posts = []
    for post in posts:
        try:
            authorize(request, post, action="view")
            authorized_posts.append(post)
        except PermissionDenied:
            continue

    return render(request, 'social/list.html', {'posts': authorized_posts,'public_posts':public_posts})


def user_signup(request): 
    if request.method == "POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
        return HttpResponse("<h4>Successfully created Account</h4>")
    else:
        fm= SignUpForm()
    return render(request,'social/signup.html',{'form':fm})






@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        post = form.save(commit=False)

        post.created_by = request.user
        post.save()

        return HttpResponseRedirect(reverse('index'))
    elif request.method == 'GET':
        form = PostForm()
        return render(request, 'social/new_post.html', { 'form': form })
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def search(request):
    query=None
    results=[]
    if request.method=="GET":
        query=request.GET.get('search')
        user=User.objects.filter(username__icontains=query)     
    return render(request,'social/search.html',{'query':query, 'user':user})