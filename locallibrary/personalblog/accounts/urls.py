from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('edit/', views.UserAndProfileView.as_view(), name='edit'),
    path('update/', views.profile, name='profile-update')

]