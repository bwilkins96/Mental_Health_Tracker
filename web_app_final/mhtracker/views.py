from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import MentalLog
from .forms import SignUpForm

@login_required
def index(request):
    num_logs = 10
    avg_mh, avg_env, avg_sleep = MentalLog.get_averages(num_logs, request.user)
    context = {
        'average_mh': round(avg_mh, 2),
        'average_env': round(avg_env, 2),
        'average_sleep': round(avg_sleep, 2),
        'num_logs': num_logs
    }

    return render(request, 'mhtracker/index.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            new_user = User.objects.create(username=username)
            new_user.set_password(password)
            new_user.save()

            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()
    
    context = {
        'form': form 
    }
    return render(request, 'registration/sign_up.html', context)

class MentalLogListView(LoginRequiredMixin, generic.ListView):
    model = MentalLog
    paginate_by = 10
    template_name = 'mhtracker/mh_log_list.html'

    def get_queryset(self):
        logs = MentalLog.objects.filter(user=self.request.user)
        return logs.order_by('-date_logged')

class MentalLogCreate(LoginRequiredMixin, CreateView):
    model = MentalLog
    fields = ['mh_rating', 'env_rating', 'diet_change', 'exercise', 'took_med', 'sleep_quality', 'notes']
    template_name = 'mhtracker/mh_log_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MentalLogUpdate(LoginRequiredMixin, UpdateView):
    model = MentalLog
    fields = ['mh_rating', 'env_rating', 'diet_change', 'exercise', 'took_med', 'sleep_quality', 'notes']
    template_name = 'mhtracker/mh_log_edit.html'

    def get_queryset(self):
        return MentalLog.objects.filter(user=self.request.user)

class MentalLogDelete(LoginRequiredMixin, DeleteView):
    model = MentalLog
    template_name = 'mhtracker/mh_log_delete.html'
    success_url = reverse_lazy('mhtracker:index')

    def get_queryset(self):
        return MentalLog.objects.filter(user=self.request.user)
