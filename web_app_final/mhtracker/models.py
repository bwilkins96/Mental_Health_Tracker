from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class MentalLog(models.Model):
    RATING_CHOICES = [
        (5, '5 - Best'),
        (4, '4'),
        (3, '3 - Middle'),
        (2, '2'),
        (1, '1 - Worst')        
    ]

    mh_rating = models.IntegerField('mental health rating', choices=RATING_CHOICES, default=5)
    env_rating = models.IntegerField('daily environment rating', choices=RATING_CHOICES, default=5)
    diet_change = models.BooleanField('diet change?')
    exercise = models.BooleanField('exercise today?')
    took_med = models.BooleanField('took medicine?')
    sleep_quality = models.IntegerField('sleep quality', choices=RATING_CHOICES, default=5)
    notes = models.TextField('personal notes', null=True, blank=True)
    date_logged = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @classmethod
    def get_averages(cls, num_logs, user):
        user_logs = cls.objects.filter(user=user)
        if len(user_logs) == 0: return (0, 0, 0)
        recent_logs = user_logs.order_by('-date_logged')[:num_logs]
        
        total_mh = 0
        total_env = 0
        total_sleep = 0
        for log in recent_logs:
            total_mh += log.mh_rating
            total_env += log.env_rating
            total_sleep += log.sleep_quality
        
        len_logs = len(recent_logs)
        avg_mh = total_mh / len_logs
        avg_env = total_env / len_logs
        avg_sleep = total_sleep /len_logs

        return (avg_mh, avg_env, avg_sleep)

    def get_date_str(self):
        return '{:%H:%M %m/%d/%Y}'.format(timezone.localtime(self.date_logged))
    
    def get_absolute_url(self):
        return reverse('mhtracker:edit', args=[str(self.id)])

    def __str__(self):
        log_str = f'Mental Health: {self.mh_rating}/5'
        log_str += f', Environment: {self.env_rating}/5'
        log_str += f', Sleep: {self.sleep_quality}/5'
        log_str += f' - {self.get_date_str()} '

        if self.diet_change: log_str += 'D'
        if self.exercise: log_str += 'E'
        if self.took_med: log_str += 'M'
        
        return log_str
