from django.conf.urls import url
from . import views

urlpatterns = [
    url('update-profile/', views.update_profile, name='update_profile'),
    url('login-facebook/', views.facebook_login_web, name='login_facebook-web'),
    url('login-facebook-api/', views.facebook_login_api, name='login-facebook-api'),
    url('sing-up-api/', views.register, name='sing-up-api'),
    url('sing-up-web/', views.sing_up_web, name='sing-up-web'),
    url('login-api/', views.login_api, name='login-api'),
    url('login-web/', views.login_web, name='login-web'),
    url('profile/', views.my_profile, name='my_profile'),
    url('logout/', views.logout_user, name='logout_user'),
    url('fanpage/', views.fanpage, name='fanpage'),

]