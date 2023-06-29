from django.db import models
from django.urls import reverse

class MentalLog(models.Model):
    RATING_CHOICES = [
        (5, '5 - Best'),
        (4, '4'),
        (3, '3 -Middle'),
        (2, '2'),
        (1, '1 - Worst')        
    ]

    mh_rating = models.IntegerField('mental health rating', choices=RATING_CHOICES, default=5)
    env_rating = models.IntegerField('daily environment rating', choices=RATING_CHOICES, default=5)
    diet_change = models.BooleanField('diet change?')
    exercise = models.BooleanField('exercise today?')
    med_change = models.BooleanField('medication change?')
    sleep_well = models.BooleanField('sleep well?')
    notes = models.TextField('personal notes', null=True, blank=True)
    date_logged = models.DateTimeField(auto_now=True)

    @classmethod
    def avg_mh_last(cls, num_logs):
        recent_logs = cls.objects.order_by('-date_logged')[:num_logs]
        
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


# from django.forms import ModelForm

# class MentalLogForm(ModelForm):
#     class Meta:
#         model = MentalLog
