from django.urls import path
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views

from . import views, forms, models

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('create/ticket/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('update/ticket/<int:pk>', views.update_ticket, name='update_ticket'),
    path('update/ticket/m/<int:pk>', views.ManagerTicketUpdateView.as_view(), name='manager_update'),
    path('update/ticket/s/<int:pk>', views.StaffTicketUpdateView.as_view(), name='staff_update'),
    path(
        'ticket/detail/<int:pk>/',
        DetailView.as_view(template_name='ticket_detail.html',model=models.Ticket),
        name='ticket_details'),
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="login.html",
            form_class=forms.AuthenticationForm,
        ),
        name="login",
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('landing/', views.landing, name='landing'),
    path('userinfo/create', views.UserInfoCreateView.as_view(), name='user_info'),
    path('userinfo/update/', views.userinfo_update, name='userinfo_update'),
    path('profile/', views.profile, name='profile'),
    path('tickets/high/', views.HighHomeView.as_view(), name='high'),
    path('tickets/medium/', views.MediumHomeView.as_view(), name='medium'),
    path('tickets/low/', views.LowHomeView.as_view(), name='low'),
    path('tickets/open/', views.OpenHomeView.as_view(), name='open'),
    path('tickets/in-progress/', views.InHomeView.as_view(), name='in_progress'),
    path('tickets/resolved/', views.ResolvedHomeView.as_view(), name='resolved'),
    path('tickets/engineering/', views.EngHomeView.as_view(), name='engineering'),
    path('tickets/sales/', views.SalesHomeView.as_view(), name='sales'),
    path('tickets/accounts/', views.AccountsHomeView.as_view(), name='accounts'),
    path('tickets/hr/', views.HRHomeView.as_view(), name='hr'),
    path('tickets/assigned-to/', views.AssignedHomeView.as_view(), name='assigned_to'),
    path('tickets/created/', views.CreatedHomeView.as_view(), name='created_tickets'),
    path('tickets/unresolved/', views.UnresolvedHomeView.as_view(), name='unresolved'),
    path('demo/', views.demo_user, name='demo_user'),
]