from django.urls import path
from . import views
from .views import profile_view, profile_edit_view

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/profile/', profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='edit_profile'),

]
