from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh_token, name='refresh-token'),
    path('verify/', views.verify_token, name='verify-token'),
    path('me/', views.me, name='me'),
    path('change-password/', views.change_password, name='change-password'),
    path('assign-role/', views.assign_role, name='assign-role'),
    path('users/', views.list_users, name='list-users'),
    path('users/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate-user'),
]
