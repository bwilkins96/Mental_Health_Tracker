from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic

from .models import MentalLog

def index(request):
    num_logs = 10
    avg = MentalLog.avg_mh_last(num_logs)
    context = {
        'average': round(avg, 2),
        'num_logs': num_logs
    }

    return render(request, 'mhtracker/index.html', context)

class MentalLogListView(generic.ListView):
    model = MentalLog
    paginate_by = 10
    template_name = 'mhtracker/mh_log_list.html'

class MentalLogCreate(CreateView):
    model = MentalLog
    fields = '__all__'
    template_name = 'mhtracker/mh_log_form.html'

class MentalLogUpdate(UpdateView):
    model = MentalLog
    fields = '__all__'
    template_name = 'mhtracker/mh_log_form.html'

class MentalLogDelete(DeleteView):
    model = MentalLog
    template_name = 'mhtracker/mh_log_delete.html'
    success_url = reverse_lazy('mhtracker:index')
