from .models import Profile,Post
from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='signin') 
def index(request):
    current_user=Profile.objects.get(user=request.user)
    posts=Post.objects.all()
    return render(request,'core/index.html',{
        'current_user': current_user,
        'posts':posts
    })
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confpassword=request.POST['confpassword']
        if password==confpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
                return redirect('signup') 
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                #creating a profile model
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()

                #login the user
                login(request,user)
                return redirect('/')
    else:
        return render(request,'core/signup.html')
    
def signin(request):
    if request.method=='POST':
        #attempt user to sign in
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)

            return redirect('/')
        else:
            messages.info(request,'enter a valid username and password')
            return redirect('login')
    else:
        return render(request,'core/signup.html')
    
@login_required(login_url='signin') 
def settings(request):
    current_user=Profile.objects.get(user=request.user)
    if request.method=='POST':
        if request.FILES.get('profilepic')==None:
            profilepic=current_user.profileimage
            bio=request.POST['bio']
            location=request.POST['location']
            current_user.profileimage=profilepic
            current_user.bio=bio
            current_user.location=location
            current_user.save()
            return render(request,'core/index.html')
        
        elif request.FILES.get('profilepic')!=None:
            profilepic=request.FILES.get('profilepic')
            bio=request.POST['bio']
            location=request.POST['location']
            current_user.profileimage=profilepic
            current_user.bio=bio
            current_user.location=location
            current_user.save()
            return render(request,'core/index.html')

    else:
        
        return render(request,'core/settings.html',{
            'current_user':current_user
            })
    

@login_required(login_url='signin') 
def upload(request):
    pass

@login_required(login_url='signin') 
def signout(request):
    logout(request)
    return render(request,'core/signin.html')