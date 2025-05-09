
from settings.form import EmailSettingForm, SettingForm
from django.shortcuts import render,redirect

from django.contrib import messages

from .models import Setting

from user.models import User

def settings_view(request):
    conf=Setting.objects.all().first()
    if conf is not None:
        print("=================== CAS AVEC INFO===================")
        form = SettingForm(request.POST or None, instance=conf)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request,"Informations enregistrées avec succès")
                return render(request,'config/index.html',{'form':form})
            messages.error(request, " impossible d'enregistrer ces informations veuillez verifier si tous les champs sont bien remplis")
        return render(request,'config/index.html',{'form':form})
    else:
        print("====================== CAS SANS INFO +++++++++===================")
        form = SettingForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request,"Informations enregistrées avec succès")
                return render(request,'config/index.html',{'form':form})
            messages.error(request, " impossible d'enregistrer ces informations veuillez verifier si tous les champs sont bien remplis")
        return render(request,'config/index.html',{'form':form})


def mail_settings(request):
    users=User.objects.all()
    form=EmailSettingForm()
    return render(request,'config/email_setting.html',{'users':users,'form':form})

def update_user_notification(request, pk):
    qs= User.objects.get(pk= pk)
    user_notif=qs.notified
    notif= None
    if user_notif==True:
       notif=False
    else:
        notif=True 
    qs.notified=notif
    qs.save()
    return redirect("config:mail_settings")
