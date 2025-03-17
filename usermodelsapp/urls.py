from django.urls import path
from .views import *

urlpatterns = [
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("superadmin/", superadmin_dashboard, name="superadmin_dashboard"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("user/", user_dashboard, name="user_dashboard"),
]
