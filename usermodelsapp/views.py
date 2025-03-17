from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.decorators import login_required


def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Этот email уже используется!")
            return redirect("register")

        user = User.objects.create_user(email=email, password=password, name=name)
        messages.success(request, "Регистрация прошла успешно! Теперь войдите.")
        return redirect("login")

    return render(request, "register.html")
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли!")

            # Проверяем, кто зашел
            if user.is_superuser:  # Суперадмин
                return redirect("superadmin_dashboard")
            elif user.is_staff:  # Админ
                return redirect("admin_dashboard")
            else:  # Обычный пользователь
                return redirect("user_dashboard")

        else:
            messages.error(request, "Неверный email или пароль!")

    return render(request, "login.html")


@login_required
def superadmin_dashboard(request):
    return render(request, "superadmin.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin.html")

@login_required
def user_dashboard(request):
    return render(request, "user.html")

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы!")
    return redirect("login")  # Перенаправление на страницу входа
