
from django.contrib import admin
from django.urls import path, include
from .views import UserListRead, UserDetailView,profile, register,user_delete, user_detail, user_login, user_logout, users_list_read
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('register/', register , name='register'),
    path('getdata/<int:id>', user_detail, name='profile'),
    # path('getdata/<int:id>', UserDetailView.as_view(), name='getdata'),
    # path('list/', users_list_read, name='userlist'),
    path('list/', UserListRead.as_view(), name='userlist'),
    path('login/', user_login, name='user_login'),#bunu yazmasak da olur aslında accounts/login ile  kendisi yapıyor.
    path('logout/', LogoutView.as_view(), name='logout_app'),#bunu yazmasak da olur aslında accounts/logout ile  kendisi yapıyor.
    path('logout/', user_logout, name='logout_app'),#bunu yazmasak da olur aslında accounts/logout ile  kendisi yapıyor.
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html"), name="password_change"),
    # password_change/ ya istek geldiğinde bizi  auth_views.PasswordChangeView.as_view a gönder ama bu da template_name="registration/password_change.html içinde demişiz.
    #  from django.contrib.auth import views as auth_views
    #veya stteingste authusers yani override edilecek yeni html lerin app ini en üste taşı.
    path("delete/<int:id>", user_delete, name="delete"),
    path("profile/", profile, name="profile"),
]
