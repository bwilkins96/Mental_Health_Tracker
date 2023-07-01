from django.test import TestCase
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

