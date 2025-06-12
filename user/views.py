from datetime import datetime
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from user.form import LoginForm, UserCreationForm
from utils import numFacture
from vente.models import Session, Vente
from .models import  PasswordResetRequest
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model


User=get_user_model()

@login_required
def user_view(request):
   
    users=User.objects.all().order_by('username')
    form = UserCreationForm()
    context={
        'items':users,
        'page':'user',
        'form':form,
    }
   
    if request.htmx:
        return render(request,'auth/partial/response.html',context) 
    return render(request,'auth/user_list.html',context)


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')  # Get role from the form (student, teacher, or admin)
        
        # Create the user
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Assign the appropriate role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()  # Save the user with the assigned role
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('home:admin_dashboard')  # Redirect to the index or home page
    return render(request, 'auth/register.html')  # Render signup template


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        
        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found.')
    
    return render(request, 'auth/forgot-password.html')  # Render forgot password template


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()
    
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'auth/reset_password.html', {'token': token})  # Render reset password template


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def user_add(request):
    users = User.objects.all().order_by('username')
    form = UserCreationForm()
    context = {
        'items': users,
        'page': 'users',
        'form': form,
    }
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user=User.objects.create(username=username,password=password,email=email,role=role)
            user.set_password(password)
            user.save()

            messages.success(request,"Utilisateur ajouté avec succès")
            html = render(request, "auth/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, form.errors)
        html = render(request, "auth/partial/response.html", context)
        return HttpResponse(html)
    return render(request, 'auth/partial/_add_user_form.html', context)



def login_view(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':

        form = LoginForm(request.POST)

        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        print("****************************USER****************************")
        print(user)
       
        if user is not None:
            utilisateur=User.objects.get(username=request.POST.get('username'))
            login(request, user)
            u=login(request, user)
            if user.is_active:
                if user.role=='admin':
                    obj, created=Vente.objects.get_or_create(dateVente=datetime.now().date())
                    return redirect('dashboard:home_page')
                else:
                    session=Session.objects.get(login=utilisateur)
                    if session.EstOuvert:
                        return redirect('dashboard:teller_page')
                    messages.error(request, ("La session n'est pas ouverte !"))
            else:
                messages.error(request, ("Votre compte a été désactivé !"))
                return render(request, 'auth/login.html', context={'form': form})
        else:
            messages.error(request, ("Authentification echouée ou ce compte n'existe pas ! ou il est désactivé"))
    return render(
        request, 'auth/login.html', context={'form': form, 'message': message})

def user_list(request):
    users = User.objects.all()
    form = UserCreationForm()
    context = {
        'users': users,
        'page': 'users',
        'form': form,
    }
    return render(request, 'auth/user_list.html', context)


def user_update_view(request, pk):
    cat=User.objects.get(pk=pk)
    items=User.objects.all().order_by('username')
    form = UserCreationForm(request.POST or None, instance=cat)
    context = {
        'form': form,
        'items':items,
        'page':'user'
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"modification éffectuée avec succès")
            
            html = render(request, "auth/partial/response.html", context)
            return HttpResponse(html)
        messages.error(request, "Modification échouée verifier les données entrées")
        html = render(request, "auth/partial/response.html", context)
        return HttpResponse(html)

    return render(request,'auth/partial/_user_modal.html',context)

def user_delete_view(request,pk):
    cat=User.objects.get(pk=pk).delete()
   
    items=User.objects.all().order_by('username')
    context={
        'items':items,
        'page':'user'
    }
    messages.success(request,"Utilisateur supprimé avec succès")
    html = render(request, "auth/partial/response.html", context)
    return HttpResponse(html)
    

def user_delete_selection(request):
    items = User.objects.all().order_by('username')
    form = UserCreationForm()
    context = {
        'items': items,
        'page': 'user',
        'form': form,
    }

    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "auth/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = User.objects.get(pk=id)
            cat.delete()
        messages.success(request, f"{len(cat_ids)} Utilisateurs supprimés avec succès")
        html = render(request, "auth/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('auth:user_list'))


def user_activate_selection(request):
    items = User.objects.all().order_by('username')
    form = UserCreationForm()
    context = {
        'items': items,
        'page': 'user',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "auth/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = User.objects.get(pk=id)
            cat.is_active = True
            cat.save()
        messages.success(request, "Comptes d'utilisateurs  activés avec succès")
        html = render(request, "auth/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('auth:user_view'))


def user_deactivate_selection(request):
    items = User.objects.all().order_by('username')
    form = UserCreationForm()
    context = {
        'items': items,
        'page': 'user',
        'form': form,
    }
    if request.method == "POST":
        cat_ids = request.POST.getlist('id[]')
        if len(cat_ids) == 0:
            messages.error(request, "Veuillez selectionner au moins une unité de vente")
            html = render(request, "auth/partial/response.html", context)
            return HttpResponse(html)
        for id in cat_ids:
            cat = User.objects.get(pk=id)
            cat.is_active = False
            cat.save()
        messages.success(request, "Comptes utilisateurs désactivés avec succès")
        html = render(request, "auth/partial/response.html", context)
        return HttpResponse(html)
    return HttpResponseRedirect(reverse('auth:user_view'))


def user_delete_all_view(request):
    count = User.objects.all().count()
    
    User.objects.all().delete()
   
    items=User.objects.all().order_by('username')
    context={
        'items':items,
        'page':'user'
    }
    messages.success(request,f"{count} Comptes utilisateurs supprimés avec succès")
    html = render(request, "auth/partial/response.html", context)
    return HttpResponse(html)

def user_active_all_view(request):
    count = User.objects.filter(is_active=False).count()
    
    User.objects.filter(is_active=False).update(is_active=True)
   
    items=User.objects.all().order_by('username')
    context={
        'items':items,
        'page':'user'
    }
    messages.success(request,f"{count} Comptes utilisateur activés avec succès")
    html = render(request, "auth/partial/response.html", context)
    return HttpResponse(html)

def user_deactive_all_view(request):
    count = User.objects.filter(is_active=True).count()
    
    User.objects.filter(is_active=True).update(is_active=False)
   
    items=User.objects.all().order_by('username')
    context={
        'items':items,
        'page':'user'
    }
    messages.success(request,f"{count} Comptes utilisateur activés avec succès")
    html = render(request, "auth/partial/response.html", context)
    return HttpResponse(html)
    

 