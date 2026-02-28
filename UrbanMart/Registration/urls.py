from django.urls import path
from . import views


urlpatterns = [
    path('',views.registration_views, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # Admin promotion URL
    path('promote-admin/', views.promote_to_admin, name='promote_admin'),
    path('demote-admin/<int:user_id>/', views.demote_admin, name='demote_admin'),

    #Oauth URLs
    path('oauth/success/', views.oauth_login_success, name='oauth_success'),
    path('oauth/error/', views.oauth_login_error, name = 'oauth_error'),

]
