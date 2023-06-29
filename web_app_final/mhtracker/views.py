from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User

from .models import MentalLog
from .forms import SignUpForm

def index(request):
    num_logs = 10
    avg = MentalLog.avg_mh_last(num_logs)
    context = {
        'average': round(avg, 2),
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

class MentalLogListView(generic.ListView):
    model = MentalLog
    paginate_by = 10
    template_name = 'mhtracker/mh_log_list.html'
    queryset = MentalLog.objects.order_by('-date_logged')

class MentalLogCreate(CreateView):
    model = MentalLog
    fields = '__all__'
    template_name = 'mhtracker/mh_log_form.html'

class MentalLogUpdate(UpdateView):
    model = MentalLog
    fields = '__all__'
    template_name = 'mhtracker/mh_log_edit.html'

class MentalLogDelete(DeleteView):
    model = MentalLog
    template_name = 'mhtracker/mh_log_delete.html'
    success_url = reverse_lazy('mhtracker:index')
