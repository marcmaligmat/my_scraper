from . import views
from django.urls import include,path,re_path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from accounts import views

urlpatterns = [
    path("register", views.signup, name="signup"),

    url(r'^login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name='logout'),

    re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]



