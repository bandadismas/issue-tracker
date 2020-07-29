from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import datetime

from . import forms, models


class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm
    #success_url = reverse_lazy('login')

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()

        return response


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    template_name = "ticket_form.html"
    fields = [
        'name',
        'description',
        'priority',
        'department_concerned',
    ]
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return super().form_valid(form)


def update_ticket(request, pk):
    if request.user.is_manager:
        return HttpResponseRedirect(reverse('manager_update', args=(pk,)))
    else:
        return HttpResponseRedirect(reverse('staff_update', args=(pk,)))


class ManagerTicketUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    template_name = 'ticket_update.html'
    fields = [
        'name',
        'description',
        'priority',
        'department_concerned',
        'assigned_to',
        'status',
    ]
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.status == 'R':
            obj.date_resolved = datetime.now()
        obj.save()
        return super().form_valid(form)


class StaffTicketUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    template_name = 'ticket_update.html'
    fields = [
        'name',
        'description',
        'priority',
        'department_concerned',
        'status',
    ]
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.status == 'R':
            obj.date_resolved = datetime.now()
        obj.save()
        return super().form_valid(form)


def landing(request):
    if request.user.first_login:
        request.user.first_login = False
        request.user.save()
        return HttpResponseRedirect(reverse('user_info'))
    else:
        return HttpResponseRedirect(reverse('home'))


class UserInfoCreateView(LoginRequiredMixin, CreateView):
    model = models.UserInfo
    template_name = "userinfo_form.html"
    fields = [
        'firstname',
        'surname',
        'gender',
        'date_of_birth',
        'department',
        'contact_line1',
        'contact_line2'
    ]
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


# class UserInfoUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.UserInfo
#     template_name = 'userinfo_update.html'
#     fields = [
#         'firstname',
#         'surname',
#         'gender',
#         'date_of_birth',
#         'department',
#         'contact_line1',
#         'contact_line2'
#     ]
#     success_url = reverse_lazy('home')


def userinfo_update(request):
    instance = request.user.userinfo
    if request.method == 'POST':
        form = forms.UserInfoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print('form valid')
            # file is saved
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = forms.UserInfoForm(instance=instance)
    return render(request,'userinfo_update.html', {'form': form})

def profile(request):
    try:
        userinfo = models.UserInfo.objects.get(user=request.user)
        return render(request, 'profile.html')

    except:
        return HttpResponseRedirect(reverse('user_info'))


class HomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.all()
        return tickets


class HighHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(priority='H')
        return tickets


class MediumHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(priority='M')
        return tickets


class LowHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(priority='L')
        return tickets


class OpenHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(status='O')
        return tickets


class InHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(status='I')
        return tickets


class ResolvedHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(status='R')
        return tickets


class EngHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(department_concerned='E')
        return tickets


class AccountsHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(department_concerned='A')
        return tickets


class SalesHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(department_concerned='S')
        return tickets


class HRHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(department_concerned='H')
        return tickets


class AssignedHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(assigned_to=self.request.user)
        return tickets


class CreatedHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.filter(created_by=self.request.user)
        return tickets


class UnresolvedHomeView(LoginRequiredMixin, ListView):
    model = models.Ticket
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        tickets = models.Ticket.objects.exclude(status='R')
        return tickets


def demo_user(request):
    email = 'demo_account@gmail.com'
    password = 'test_admin'

    user = authenticate(email=email, password=password)
    login(request, user)

    return HttpResponseRedirect((reverse('home')))
