from django.shortcuts import render
from .models import Conference,category
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .form import conferenceform
from django.contrib.auth.mixins import LoginRequiredMixin
def conferenceList(req):
    liste=Conference.objects.all().order_by('-start_date')
    return render(req,'conference/conferencelist.html',{'conferencelist':liste})
class conferenceListeview (ListView):
    model=Conference
    template_name='conference/conference_list.html'
    context_object_name='conferences'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=category.objects.all()
        return context
    def get_queryset(self):
        category_id=self.request.GET.get('category')
        query= Conference.objects.order_by('-start_date')
        if category_id:
            query=Conference.objects.filter(category=category_id)
        return query
class detailsviewconference(DetailView):
    model=Conference
    template_name='conference/conference_detail_view.html'
    context_object_name='conference'
class Createviewconference(LoginRequiredMixin,CreateView):
    login_url=reverse_lazy('login')
    model = Conference
    template_name='conference/conference_form.html'
    form_class=conferenceform
    #fields=('title','description','location', 'start_date', 'end_date',  'price','capacity','program','category')
    success_url=reverse_lazy('listviewconf')
class UpdateViewconference(UpdateView):
    model = Conference
    form_class=conferenceform
    #fields=('title','description','location', 'start_date', 'end_date',  'price','capacity','program','category')
    success_url=reverse_lazy('listviewconf')
class  DeleteViewconference(DeleteView):
    model = Conference
    success_url=reverse_lazy('listviewconf')
