
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import User, Role
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from .forms import UploadFileForm


#
# def register_user(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         name = request.POST.get("name")
#
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Этот email уже используется!")
#             return redirect("register")
#
#         user = User.objects.create_user(email=email, password=password, name=name)
#         messages.success(request, "Регистрация прошла успешно! Теперь войдите.")
#         return redirect("login")
#
#     return render(request, "register.html")


def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Этот email уже используется!")
            return redirect("register")

        # Создаем пользователя
        user = User.objects.create_user(email=email, password=password, name=name)

        # 📌 Создаем ему роль по умолчанию (обычный пользователь)
        Role.objects.create(user=user, role="user")

        messages.success(request, "Регистрация прошла успешно! Теперь войдите.")
        return redirect("login")

    return render(request, "register.html")





from django.contrib.auth.decorators import login_required

@login_required
def add_user(request):
    if request.user.role.role != "admin":
        messages.error(request, "У вас нет доступа!")
        return redirect("user_dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        role = request.POST.get("role")  # Получаем роль из формы

        if User.objects.filter(email=email).exists():
            messages.error(request, "Этот email уже зарегистрирован!")
            return redirect("add_user")

        user = User.objects.create_user(email=email, password=password, name=name)
        Role.objects.create(user=user, role=role)  # Создаем запись в Role
        messages.success(request, f"Пользователь {email} добавлен!")
        return redirect("admin_dashboard")

    return render(request, "add_user.html")


def index(request):
    return render(request, "user.html")

#
# def login_user(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#
#         user = authenticate(request, email=email, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Вы успешно вошли!")
#
#             # Проверяем, кто зашел
#             if user.is_superuser:  # Суперадмин
#                 return redirect("superadmin_dashboard")
#             elif user.is_staff:  # Админ
#                 return redirect("admin_dashboard")
#             else:  # Обычный пользователь
#                 return redirect("user_dashboard")
#
#         else:
#             messages.error(request, "Неверный email или пароль!")
#
#     return render(request, "login.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли!")

            # Если у пользователя нет роли, ставим "user"
            role = user.role.role if hasattr(user, "role") else "user"

            if role == "superadmin":
                return redirect("superadmin_dashboard")
            elif role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")

        else:
            messages.error(request, "Неверный email или пароль!")

    return render(request, "login.html")

@login_required
def delete_user(request, user_id):
    if request.user.role.role != "admin":
        messages.error(request, "У вас нет доступа!")
        return redirect("user_dashboard")

    user = get_object_or_404(User, id=user_id)

    if user.role.role == "superadmin":
        messages.error(request, "Нельзя удалить супер-админа!")
        return redirect("admin_dashboard")

    user.delete()
    messages.success(request, "Пользователь удален!")
    return redirect("admin_dashboard")

@login_required
def change_role(request, user_id):
    if request.user.role.role != "superadmin":
        messages.error(request, "У вас нет доступа!")
        return redirect("user_dashboard")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        if new_role in ["user", "admin", "superadmin"]:
            user.role.role = new_role
            user.role.save()
            messages.success(request, f"Роль пользователя обновлена на {new_role}!")
        else:
            messages.error(request, "Некорректная роль!")

        return redirect("superadmin_dashboard")

    return render(request, "change_role.html", {"user": user})



@login_required
def superadmin_dashboard(request):
    return render(request, "superadmin.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin.html")

@login_required
def user_dashboard(request):
    return render(request, "user.html")



def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы!")
    return redirect("login")  # Перенаправление на страницу входа




def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("upload_success")
    else:
        form = UploadFileForm()

    return render(request, "upload.html", {"form": form})
