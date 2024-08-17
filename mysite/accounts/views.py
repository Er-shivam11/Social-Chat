from django.shortcuts import render
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from accounts.models import CustomUser
from django.http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from chat.models import Post,Comment
from django.shortcuts import get_object_or_404


from django import forms
from django.db.models import Q

# Create your views here.
def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('home')  # Superuser, redirect to the 'home' page
                else:
                    return redirect('userhome')  
                
            else:
                if username == '' or password == '':
                    messages.error(
                        request, message='Please Enter Username and Passowrd Correctly')
                else:
                    messages.error(
                        request, message='Username or Password not correct')

    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('success')  # Redirect to a success page (change 'success' to your desired URL)
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


# @login_required(login_url="login")
def createuser(request):
    create_form = RegisterForm    
    # user_details = CustomUser.objects.first()
    if request.user.is_superuser:

        if request.method == 'POST':
            create_form = RegisterForm(request.POST,request.FILES)
            
            if create_form.is_valid():
                create_form.save()
                
                return userlist(request)
            else:
                print(create_form.errors)
        else:
            create_form = RegisterForm()
    else:
        return HttpResponse('you are not allowed')

    context = {'createform': create_form}
    return render(request, 'auth/createuser.html',context )

@login_required(login_url="login")
def deleteuser(request, pk):
    delete_user=CustomUser.objects.get(id=pk)
    delete_user_form=RegisterForm(instance=delete_user)
    if  request.user.is_superuser:
        
        delete_user.is_active = False
        delete_user.save()
        return redirect('userlist')
    else:
        return HttpResponse('you are not allowed')  
      
@login_required(login_url="login")
def updateuser(request, pk):
    update_user_det = get_object_or_404(CustomUser, id=pk)

    if request.user.is_superuser or request.user.username:
        if request.method == 'POST':
            update_user_form = RegisterForm(request.POST, request.FILES, instance=update_user_det)
            print("Form data:", request.POST)
            if update_user_form.is_valid():
                print("Form is valid")
                # Check if the username has changed
                if update_user_form.cleaned_data['username'] != update_user_det.username:
                    # Check if the new username already exists
                    if CustomUser.objects.filter(username=update_user_form.cleaned_data['username']).exists():
                        update_user_form.add_error('username', 'A user with that username already exists.')
                        print("Username already exists")
                    else:
                        update_user_form.save()
                        return redirect('userlist')
                else:
                    update_user_form.save()
                    return redirect('userlist')
            else:
                print("Form errors:", update_user_form.errors)
        else:
            update_user_form = RegisterForm(instance=update_user_det)
    else:
        return HttpResponse('You are not allowed')

    context = {
        "updateregisterform": update_user_form
    }
    return render(request, 'auth/updateuser.html', context)

def checksuperusre(request):
    if User.objects.filter(is_superuser=True).exists():
        # Superuser exists
        return HttpResponse('exist')
    else:
        # Superuser does not exist
        return HttpResponse('not exist')


@login_required(login_url="login")
def userlist(request):
    user_list = CustomUser.objects.filter(~Q(username=request.user.username) & ~Q(is_superuser=True) & Q(is_active=True))
    # user_list = CustomUser.objects.filter(username=request.user.username)
    # user_list = CustomUser.objects.exclude(Q(username=request.user.username) & Q(request.user.is_superuser))
    if request.user.is_superuser or request.user.is_authenticated and not request.user.is_staff:
        context = {"userlist": user_list}
    else:
        return HttpResponse('you are not allowed')
    
    return render(request, "auth/userlist.html", context)

@login_required(login_url="login")
def userprofile(request):
    user_profile = CustomUser.objects.filter(username=request.user.username)
    print(user_profile)
    context = {"userprofile": user_profile}

    return render(request, "auth/userprofile.html", context)

def basicuserprofile(request):
    user_profile = CustomUser.objects.filter(username=request.user.username)
    user_post=Post.objects.filter(user=request.user) 
    
    print(user_profile)

    context = {"userprofile": user_profile,"userpost":user_post}
    return render(request,"auth/basicuser.html",context)


def userhome(request):
    posts = Post.objects.all().order_by('-created_at')
    profile=CustomUser.objects.filter(username=request.user)
    user_profile = CustomUser.objects.get(username=request.user)
    print(profile,'this is profile')
    others_profile=CustomUser.objects.exclude(username=request.user)
    print(others_profile,'this is other profile')
    for post in posts:
        post.comments = Comment.objects.filter(post=post).order_by('-created_at')
        post.profile_picture = post.user.profile_picture

    
    return render(request,"userhome.html", {'posts': posts,'profile':profile,'othersprofile':others_profile,'user_profile':user_profile})

