from django.shortcuts import render,HttpResponseRedirect
from .forms import signupform,loginform,postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    post=Post.objects.all()
    return render(request,'home.html',{'posts':post})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        fullname=user.get_full_name()
        gps=user.groups.all()
        return render(request,'dashboard.html',{'posts':posts,'fullname':fullname,'groups':gps})
    else:
        return HttpResponseRedirect('/blog/userlogin/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=loginform(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully')
                    return HttpResponseRedirect('/blog/dashboard/')
        else:
            form=loginform()      
        return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method=="POST":
        form=signupform(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! you have become successfully Author')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=signupform()
    return render(request,'signup.html',{'form':form})


def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=postform(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                post=Post(title=title,desc=desc)
                post.save()
                messages.success(request,'Post Added Successfully')
                form=postform()
        else:
            form=postform()
        return render(request,'addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/userlogin/')
    
def update_post(request,pk):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=pk)
            form=postform(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Post Updated Successfully')
        else:
            pi=Post.objects.get(pk=pk)
            form=postform(instance=pi)
        return render(request,'updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/userlogin/')
    
def del_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
            messages.success(request,'Post Deleted Successfully')
            return HttpResponseRedirect('/blog/dashboard/')
    else:
       return HttpResponseRedirect('/blog/dashboard/')
        