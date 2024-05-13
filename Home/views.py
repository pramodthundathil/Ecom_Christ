from django.shortcuts import render, HttpResponse, redirect
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorator import admin_only
from django.contrib.auth.models import Group
from Product.models import Products, Cart


@admin_only
def Index(request):
    product = Products.objects.all()
    try:
        cart_items_count = Cart.objects.filter(user = request.user).count()
    except:
        cart_items_count = 0

    context = {
        "product":product,
        "cart_items_count":cart_items_count
    }
    return render(request,'index.html',context)

def MerchantIndex(request):
    return render(request,"merchantindex.html")

def AdminIndex(request):
    
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            group = Group.objects.get(name='merchant')
            user.groups.add(group)

            messages.info(request,"merchant Created.....")
            return redirect("AdminIndex")
        
    context = {
        "form":form
    }
    return render(request,"adminindex.html",context)


def SignIn(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["pswd"]

        user = authenticate(request,username = username, password = password)
        print(username, password, "............................................................")
        if user is not None:
            login(request,user)
            return redirect("Index")
        else:
            messages.error(request,"Username or password incorrect")
            return redirect("SignIn")
        
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.info(request,"User Created.....")
            return redirect("SignIn")

    context = {"form":form}
    return render(request,"register.html",context)

def SignOut(request):
    logout(request)
    messages.info(request,"You are signed out....")
    return redirect("SignIn")

