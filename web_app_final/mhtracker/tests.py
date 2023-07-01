from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import MentalLog
from .forms import SignUpForm

class MentalLogModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test_user')

        MentalLog.objects.create(mh_rating=5, env_rating=4, sleep_quality=3, user=test_user,
                                 diet_change=False, exercise=False, took_med=False)
        MentalLog.objects.create(mh_rating=5, env_rating=2, sleep_quality=1, user=test_user,
                                 diet_change=False, exercise=False, took_med=False)

    def test_get_averages(self):
        test_user = User.objects.get(username='test_user')
        mh_avg, env_avg, sleep_avg = MentalLog.get_averages(10, test_user)

        self.assertEqual(mh_avg, 5)
        self.assertEqual(env_avg, 3)
        self.assertEqual(sleep_avg, 2)

    def test_get_absolute_url(self):
        test_log = MentalLog.objects.get(id=1)
        self.assertEqual(test_log.get_absolute_url(), '/logs/1/')

class SignUpFormTests(TestCase):
    
    def test_invalid_on_different_passwords(self):
        test_form = SignUpForm({'username': 'test_user', 'password': 'test', 
                                'confirm_password': 'different'})
        
        self.assertEqual(test_form.is_valid(), False)

    def test_invalid_on_non_unique_username(self):
        User.objects.create_user(username='test_user')
        test_form = SignUpForm({'username': 'test_user', 'password': 'test', 
                                'confirm_password': 'test'})
        
        self.assertEqual(test_form.is_valid(), False)

    def test_valid_on_valid_input(self):
        test_form = SignUpForm({'username': 'test_user', 'password': 'test', 
                                'confirm_password': 'test'})
        
        self.assertEqual(test_form.is_valid(), True)

class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test_user', password='P3jwt/VWMENJNA==')

        MentalLog.objects.create(mh_rating=5, env_rating=4, sleep_quality=3, user=test_user,
                                 diet_change=False, exercise=False, took_med=False)
        MentalLog.objects.create(mh_rating=5, env_rating=2, sleep_quality=1, user=None,
                                 diet_change=False, exercise=False, took_med=False)
    @classmethod       
    def get_urls(cls, id):
        url_info = [('index', False), ('list', False), ('create', False), ('delete', True), ('edit', True)]
        urls = []

        for url_data in url_info:
            if url_data[1]:
                url = reverse(f'mhtracker:{url_data[0]}', args=[id])
            else:
                url = reverse(f'mhtracker:{url_data[0]}')

            urls.append(url)

        return urls

    def test_login_required(self):
        urls = self.get_urls(1)

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user', password='P3jwt/VWMENJNA==')
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_user_can_only_access_own_logs(self):
        self.client.login(username='test_user', password='P3jwt/VWMENJNA==')

        url_names = ['mhtracker:edit', 'mhtracker:delete']
        for name in url_names:
            response_1 = self.client.get(reverse(name, args=[1]))
            response_2 = self.client.get(reverse(name, args=[2]))

            self.assertEqual(response_1.status_code, 200)
            self.assertEqual(response_2.status_code, 404)

    def test_list_view(self):
        test_user = User.objects.get(username='test_user')
        self.client.login(username='test_user', password='P3jwt/VWMENJNA==')
        
        for i in range(15):
            MentalLog.objects.create(mh_rating=5, env_rating=4, sleep_quality=3, user=test_user, 
                                     diet_change=False, exercise=False, took_med=False)
            
        response = self.client.get(reverse('mhtracker:list'))
        test_user_logs = response.context['object_list']
        self.assertEqual(len(test_user_logs), 10) 

        last_date = test_user_logs[0].date_logged
        for i in range(1, len(test_user_logs)):
            log_date = test_user_logs[i].date_logged
            
            self.assertTrue(log_date <= last_date)
            last_date = log_date

