from django.db import models
from django.urls import reverse
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
    med_change = models.BooleanField('took medicine?')
    sleep_well = models.IntegerField('sleep quality', choices=RATING_CHOICES, default=5)
    notes = models.TextField('personal notes', null=True, blank=True)
    date_logged = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @classmethod
    def avg_mh_last(cls, num_logs, user):
        user_logs = cls.objects.filter(user=user)
        if len(user_logs) == 0: return 0
        recent_logs = user_logs.order_by('-date_logged')[:num_logs]
        
        total = 0
        for log in recent_logs:
            total += log.mh_rating
        
        return total / len(recent_logs)

    def get_date_str(self):
        return '{:%H:%M %m/%d/%Y}'.format(self.date_logged)
    
    def get_absolute_url(self):
        return reverse('mhtracker:edit', args=[str(self.id)])

    def __str__(self):
        return f'{self.mh_rating}, {self.get_date_str()}'

