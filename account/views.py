from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username is already exist")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username,email=email, password=password)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login')
    else:
        print("this is not post method")
        return render(request, 'register.html')

        alert = True
        return render(request, "register.html", {'alert': alert})
    return render(request, "register.html")



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect(login)
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')
