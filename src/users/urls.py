from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('delete_user/<int:id>', views.delete_user_view, name='delete_user'),
    path('delete_user_confirmation/<int:id>', views.delete_user_confirmation_view, name='delete_user_confirmation'),
    path('report_user/<int:reported_user_id>', views.report_user, name='report_user'),
    #path('report_issue/<int:reported_user_id>/', views.report_issue, name='report_issue'),
]