from django.urls import path
from .views import register_view, UserDetailView, UserChangeView, UserChangePasswordView,logout_view,login_view

app_name = 'accounts'


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', register_view, name='create'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<pk>/edit/', UserChangeView.as_view(), name='user_update'),
    path('profile/<pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),

]

