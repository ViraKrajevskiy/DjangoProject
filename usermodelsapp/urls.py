from django.urls import path
from .views import (
    logout_user, register_user, login_user,
    superadmin_dashboard, admin_dashboard, user_dashboard,
    index, add_user, change_role, delete_user
)

urlpatterns = [
    path("", index, name="home"),

    # Аутентификация
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),

    # Панели управления
    path("superadmin/", superadmin_dashboard, name="superadmin_dashboard"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("user/", user_dashboard, name="user_dashboard"),

    # Управление пользователями
    path("add_user/", add_user, name="add_user"),
    path("delete_user/<int:user_id>/", delete_user, name="delete_user"),  # Удаление пользователя
    path("change_role/<int:user_id>/", change_role, name="change_role"),  # Изменение роли пользователя
]
