from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def base(request):
    return render (request,"base.html")

@login_required
def home(request):
    return render(request,"home.html")


def login_u(request):
    return render (request,'login.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,"home.html")
        else:
            messages.error(request,'uwu deu bosta')
    return redirect('/') 

@login_required
def logout_user(request):
    logout(request)
    return redirect('')

def registro(request):
    return render(request,"registro.html")


def resgistrar(request):
    data = {}
    data['msg']=[]
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        passw1 = request.POST.get('passw1')
        passw2 = request.POST.get('passw2')
        if username == "" or email == "" or passw1 == "" or  passw2  == "":
                data['msg'].append("prencha todos os campos")  
                return render(request, 'registro.html', data)             
        try:
            user = User.objects.filter(email = email)
            if (len(user)>0):
                data['msg'].append("Email já cadastrado!") 
                return redirect('registro.html')
        except:
                data['msg'].append("Erro email ja cadastrado")
                return render(request, 'registro.html', data)     
        if (passw1 == passw2):
            try:
                user = User.objects.create_user(username=username, email= email, password=passw1, is_superuser=False, is_staff=True, is_active=True)
                user.save()
                return redirect('login.html')
            except:
                data['msg'].append("erro ao cadastrar")
                return render(request, 'registro.html', data)
        else:
           data['msg'].append("Erro senha") 
        return render(request,'registro.html',data)
    else:
        data['msg'].append("erro ao cadastrar")
        return render(request, 'registro.html', data)

def recpass_v(request):
    return render (request,'recpass.html')

@csrf_protect
def recpass(request):
    data = {}
    data['msg'] = []
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email__exact=email)
            if user is not None:
                #Envia e-mail com a senha....https://code.tutsplus.com/pt/tutorials/sending-emails-in-python-with-smtp--cms-29975
                #print(user.username)
                #print(user.first_name)
                # Reseta a senha e envia a nova senha .. Por segurança. deve-se gerar uma senha automaticamente random()....
                user.set_password("ABC123")
                user.save()
                data['msg'].append("E-mail enviado com sucesso! --> " + str(user.email) + "--> Nova Senha --> ABC123")
        except:  
            data['msg'].append("E-mail não cadastrado!") 
            return render(request, 'recpass.html', data)
        return render(request, 'login.html', data)
    



