from django.shortcuts import render
from .models import Participant
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from .forms import participantform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class usercreateview(CreateView):
    model=Participant
    form_class=participantform
    template_name='user/register.html'
    success_url= reverse_lazy('login')
class logincustomview(LoginView):
    template_name='user/login.html'
    #def get_success_url(self):
     #   return reverse('listviewconf')
class logoutcustomview(LogoutView):
    next_page= reverse_lazy('login')
