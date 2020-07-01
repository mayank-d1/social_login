from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .models import User


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(email=email).first()
        if user is None:
            return HttpResponse("<h1>No such user exits</h1>")
        if user.check_password(password):
            auth_login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home", user_id="all")
    return render(request, 'login.html')


@login_required
def home(request, user_id="all"):
    if user_id.lower() == "all":
        users = User.objects.all()
    else:
        user_id = int(user_id)
        user = User.objects.filter(id=user_id).values()
        return render(request, 'user_details.html', context={"user": user})

    return render(request, 'home.html', context={"users": users})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("login")


@login_required
def set_password(request, user_id):
    if request.method == "POST":
        user = User.objects.filter(id=user_id).first()
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password != confirm_password:
            return HttpResponse("<h1>Password did not match</h1>")
        else:
            user.set_password(raw_password=password)
            user.save()
            update_session_auth_hash(request=request, user=user)
            return redirect("home", user_id="all")
    return render(request, "set_password.html")

