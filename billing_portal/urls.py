from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='root_login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('company/<int:pk>/edit/', views.edit_company, name='edit_company'),
    path('company/<int:pk>/delete/', views.delete_company, name='delete_company'),
    path('register-company/', views.register_company, name='register_company'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('billing/', views.billing_view, name='billing'),
]
