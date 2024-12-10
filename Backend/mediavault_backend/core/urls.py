from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('verify-login/<str:token>/', views.verify_login, name='verify_login'),
]