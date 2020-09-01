from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.urls import reverse
# Create your views here.

def adminlog(request):
    us = User.objects.all()
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'adminpanel.html', {"info" : us})
    
    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        #user = auth.authenticate(username=username, password=password)

        if username == 'thanseef' and password == '1234':
            request.session['username'] = username
            return render(request, 'adminpanel.html', {"info" : us})
        
        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect(adminlog)
    else:
        return render(request,'adminlog.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.error(request, '😢 Wrong username/password!')
            return redirect('/')
    else:
        return render(request,'login.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect(home)

    elif request.method == "POST":
        username = request.POST['Username']
        first_name = request.POST['Firstname']
        last_name = request.POST['Lastname']
        email = request.POST['Email']
        password = request.POST['Password']
        confirmpassword = request.POST['confirmpassword']
        dicti = {"first_name":first_name,"last_name":last_name,"username":username,"email":email}
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already taken')
                return render(request,'register.html',dicti)
            elif User.objects.filter(username=username).exists():
                messages.error(request,"username already taken") 
                return render(request,'register.html',dicti)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print("USER CREATED")
                return redirect('/')
        else:
            messages.error(request,'Password wrong')
            return render(request,'register.html',dicti)
    else:
        return render(request, 'register.html')


@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def home(request):
    return render(request,'home.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logout(request):
    del request.session['username']
    return redirect('admin/')

def logoutuser(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminpanel(request):
    user=User.objects.all()
    return render(request,'adminpanel.html', {'info': user})

    #return redirect(adminpanel)
             

@login_required(login_url='/')
def product(request):
    return render(request,'product.html')


@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def add(request):
    if request.user.is_superuser:     
        if request.method == "POST":
            username = request.POST['Username']
            first_name = request.POST['Firstname']
            last_name = request.POST['Lastname']
            email = request.POST['Email']
            password = request.POST['Password']
            confirmpassword = request.POST['confirmpassword']
            dicti = {"first_name":first_name,"last_name":last_name,"username":username,"email":email}
            if password == confirmpassword:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already taken')
                    return render(request,'add.html',dicti)
                elif User.objects.filter(username=username).exists():
                    messages.error(request,"username already taken") 
                    return render(request,'add.html',dicti)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save();
                    print("USER CREATED")
                    return redirect('adminpanel')
            else:
                messages.error(request,'Password wrong')
                return render(request,'add.html',dicti)
        else:
            return render(request, 'add.html')
    else:
        return redirect(home)


def update(request,id):
    user=User.objects.get(id=id)
    if request.method=='POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()
        return redirect(adminlog)
    else:
        return render(request,'update.html',{'user':user})


'''
@login_required(login_url='/')
def search (request):
    if request.method=='POST':
        username=request.POST['search']
        if User.objects.filter(username= username).exists():
            user=User.objects.get(username=username)
            return render(request,'search.html',{'data':user})
        else:
            messages.error(request,'NO SUCH A USERNAME ')
            return render(request,'nosearch.html')
    messages.error(request,'PLEASE put something ')      
    return render(request,'search.html')
'''

def delete(request,id):
        user=User.objects.get(id=id)
        user.delete()
        return redirect(adminlog)


@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def user(request):
    return render(request,'home.html')
        
