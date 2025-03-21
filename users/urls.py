from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/',views.register, name='register'),
    path('active/<active_code>', views.active_user, name='active_user'),
    path('forget_pwd', views.forget_pwd, name='forget_pwd'),
    path('forget_pwd_url/<active_code>', views.forget_pwd_url, name='forget_pwd_url'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('editor_user/', views.editor_users, name='editor_users'),
]