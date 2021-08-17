import json
import bcrypt
import jwt
import unittest
import re

from codecs       import encode, decode
from django.test  import TestCase, Client
from users.models import User
from my_settings  import SECRET_KEY, algorithm

client = Client()

class SignUpTest(TestCase):
    
    def setUp(self):
        
        User.objects.create(
            email    = 'test1@test.com',
            password = '12341234',
            name     = 'runningman'
        )
        
    def test_success_signup(self):
        
        data = {
            'email'    : 'test2@test.com',
            'password' : '12341234',
            'name'     : 'sosominmin'
        }
        
        response = client.post('/users/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})
        
    def test_fail_email_exist(self):
        
        data = {
            'email'    : 'test1@test.com',
            'password' : '12341234',
            'name'     : 'runnigman'            
        }
        
        response = client.post('/users/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EXIST_EMAIL'})

    def test_email_vaildation_check(self):

        data = {
                'email'    : 'test1test.com',
                'password' : '12341234',
                'name'     : 'runningman'
                }

        response = client.post('/users/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_EMAIL_FORM'})
        
    def tearDown(self):
        User.objects.all().delete()
        
    def test_password_vaildation_check(self):
        
        data = {
                'email'    : 'test2@test.com',
                'password' : '!!!!!!!',
                'name'     : 'runningman'
                }

        response = client.post('/users/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_PASSWORD_FORM'})
        
class SignInTest(TestCase):
    
    def setUp(self):    

        User.objects.create(
            email    = 'test1@test.com',
            password = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            name     = 'runningman'
            )
        
    def test_success_signin(self):
        
        data = {
            'email'    : 'test1@test.com',
            'password' : '12345'
            }

        user_email   = User.objects.get(email='test1@test.com')
        access_token = jwt.encode({'id' : user_email.id}, SECRET_KEY, algorithm)
        
        response = client.post('/users/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'access_token' : access_token,
            'message' : 'SUCCESS'
            }
        )
        
    def test_fail_not_input_email(self):
        
        data = {
            'email'    : '',
            'password' : '12345' 
        }
        
        response = client.post('/users/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'CHECK_YOUR_INPUT'})
    
    def test_fail_not_input_password(self):
        
        data = {
            'email'    : 'test1@test.com',
            'password' : '' 
        }
        
        response = client.post('/users/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'CHECK_YOUR_INPUT'})
        
    def test_fail_not_matched_email(self):
        
        data = {
            'email'    : 'test2@test.com',
            'password' : '12345'
        }
        
        response = client.post('/users/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_EMAIL'})
        
    def test_fail_not_matched_password(self):
        
        data = {
            'email'    : 'test1@test.com',
            'password' : '123'
        }
        
        response = client.post('/users/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_PASSWORD'})
        
    def tearDown(self):
        User.objects.all().delete()