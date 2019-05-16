from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('register/', views.register_views, name='register'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verify_code/', views.send_verify_code, name='send_verify_code'),
    path('ajax_confirm/', views.ajax_confirm, name='ajax_confirm'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('cancel_email/', views.cancel_email, name='cancel_email'),
    path('login_by_qq', views.login_by_qq, name='login_by_qq'),    # welisit.com/user/login_by_qq
    path('bind_accout/', views.bind_accout, name='bind_accout'),
    path('oauth_login/<oauth_type>', views.OAuthLoginView.as_view(), name='oauth_login'),
]