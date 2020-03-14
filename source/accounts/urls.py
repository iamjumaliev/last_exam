from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, UserDetailView, UserChangeView, UserChangePasswordView

app_name = 'accounts'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', register_view, name='create'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<pk>/edit/', UserChangeView.as_view(), name='user_update'),
    path('profile/<pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),

]

