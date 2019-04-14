from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('register/', views.register_views, name='register'),
    path('user_info/', views.user_info, name='user_info'),
]