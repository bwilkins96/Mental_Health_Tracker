from django.shortcuts import render
from django.http import HttpResponse

from .models import MentalLog

def index(request):
    num_logs = 10
    context = {
        'average': MentalLog.avg_mh_last(num_logs),
        'num_logs': num_logs
    }

    return render(request, 'mhtracker/index.html', context)
