from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def base(request):
    return render (request,"base.html")

@login_required
def home(request):
    return render(request,"home.html")


def login_m(request):
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
    return redirect('') 

@login_required
def logout_user(request):
    logout(request)
    return redirect('')

def regis(request):
    return render(request,"regis.html")


def resgistrar(request):
    data = {}
    data['msg']=[]
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        passw1 = request.POST.get('passw1')
        passw2 = request.POST.get('passw2')
        if username == "" or email == "" or passw1 == "" or  passw2  == "":
                data['msg'].append("Sistema indisponível. Tente novamente mais tarde!")  
                return render(request, 'regis.html', data)             
        try:
            user = User.objects.filter(email = email)
            if (len(user)>0):
                return redirect('regis')
        except:
                data['msg'].append("Erro email ja cadastrado")
                return render(request, 'regis.html', data)     
        if (passw1 == passw2):
            try:
                user = user.objects.create_user(username=username, email= email, password=passw1, is_superuser=False, is_staff=True, is_active=True)
                user.save()
                return redirect('login.html')
            except:
                data['msg'].append("erro ao cadastrar")
                return render(request, 'regis.html', data)
        else:
            messages.error(request, "usuário e senha invalido favor tentar novamente.")
    else:
        data['msg'].append("erro ao cadastrar")
        return render(request, 'regis.html', data)

@csrf_protect
def nova_senha(request):
    data = {}
    data['msg'] = []
    data['error'] = []
    if request.method =='POST':
        email = request.POST.get('email')
        try:
            if(email == ''):
                data['error'].append('email inválido')
            else:
                val_user = User.objects.filter(email=email)
                if (len(val_user) > 0):
                    newpass = randint(10000000,99999999)
                    user = User.objects.get(email=email)
                    user.set_password(newpass)
                    user.save()
                    emailService.recoveryPass(newpass, user.username, email)
                    data['msg'].append('Sua nova senha foi enviada no email!')
                else:
                    data['error'].append('email não cadastrado!')   
        except:
            data['error'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'recovery_pass.html', data)  
    return render(request, 'recovery_pass.html', data)




