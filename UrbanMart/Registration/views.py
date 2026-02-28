from django.shortcuts import render, redirect
from django.contrib import messages
from Registration.forms import RegistrationForm
from Registration.models import Registration
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
# Admin views

def promote_to_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Registration.objects.get(email=email)
            user.is_admin = True
            user.save()
            messages.success(request, f'{user.email} has been promoted to Admin!')
            return redirect('promote_admin')
        except Registration.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

    users = Registration.objects.all().order_by('-id')
    return render(request, 'promote_admin.html', {'users' : users})

def demote_admin(request, user_id):
    try:
        user = Registration.objects.get(id=user_id)
        user.is_admin = False
        user.save()
        messages.success(request, f'{user.email} has been demoted from Admin!')
    except Registration.DoesNotExist:
        messages.error(request, 'User not found!')

    return redirect('promote_admin')


# Registration Views
def registration_views(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('homepage')  
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Registration.objects.get(email=email, password=password)
        except Registration.DoesNotExist:
            return HttpResponse("Invalid email or password")

       
        request.session['user_id'] = user.id
        request.session['user_name'] = user.first_name
        request.session['is_admin'] = user.is_admin

        return redirect('homepage')  
   
    return redirect('homepage')

def oauth_login_success(request):
    messages.success(request, 'Successfully logged in  with Google!')
    return redirect('homepage')

def oauth_login_error(request):
    messages.error(request, 'Google login failed. Please try again.')
    return redirect('homepage')

def logout_user(request):
    request.session.flush()  
    messages.success(request, "Logout successful.")
    return redirect('homepage')  
