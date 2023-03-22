from .models import Profile,Post,Follower
from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.

@login_required(login_url='signup') 
def index(request):
    current_user=Profile.objects.get(user=request.user)
    follower_object=Follower.objects.get(current_user=current_user)
    following_users=follower_object.following_user_id.all()
    posts=Post.objects.all()
    feed=[]
    for post in posts:
       if post.user in following_users:
           feed.append(post)
           
    return render(request,'core/index.html',{
        'current_user': current_user,
        'posts':feed
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

                #creating the follower model
                Follower.objects.create(current_user=new_profile)

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
    if request.method=='POST':
        image=request.FILES.get('image')
        caption=request.POST.get('caption')
        new_post=Post(user=Profile.objects.get(user=request.user),image=image,caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return render(request,'core/upload.html')

@login_required(login_url='signin') 
def signout(request):
    logout(request)
    return render(request,'core/signup.html')

@login_required(login_url='signin') 
def profile(request,username):
    requested_user=User.objects.get(username=username)
    requested_profile=Profile.objects.get(user=requested_user)
    posts=Post.objects.filter(user=requested_profile)
    return render(request,'core/profile.html',{
        'requested_profile':requested_profile,
        'posts':posts
    })

@login_required(login_url='signin') 
def follow(request,username):
    current_user=Profile.objects.get(user=request.user)
    if request.method=='POST':
        following_list=Follower.objects.get(current_user=current_user)
        requested_user=User.objects.get(username=username)
        #update follower
        requested_profile=Profile.objects.get(user=requested_user)
        following_list.following_user_id.add(requested_profile)
        following_list.save()
        #update following
        follower_list=Follower.objects.get(current_user=requested_profile)
        follower_list.follower_user_id.add(current_user)
        follower_list.save()
        print('bhak')
        return profile(request,username)
    else:
        return profile(request,username)