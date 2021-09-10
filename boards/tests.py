import bcrypt
import json
from django.core.checks import messages
import jwt

from django.test import TestCase, Client
from django.http import response

from .models     import Board, Tag
from users.models import User
from my_settings import SECRET_KEY, algorithm

class PostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        self.maxDiff = None
        self.tag     = Tag.objects.create(
            id=1, 
            name='test'
            )
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        
    def test_success_posting(self):

        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title"    : "testing_post",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : self.tag.id
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_keyerror_posting(self):
    
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title1"    : "testing_post",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : self.tag.id
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)

class RePostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        self.maxDiff = None
        
        Tag.objects.create(
            id   = 1,
            name = 'test'
        )
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        User.objects.create(
            id       = 1,
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            id          = 1,
            title       = 'testing_post1',
            content     = 'testing_content1',
            password    = hashed_password,
            depth       = 1,
            groupno     = 1,
            orderno     = 1,
            writer_id   = 1,
            tag_id      = 1
        )
        
    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        
    def test_success_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,
            'title'    : 'modify_test',
            'content'  : 'modify_content',
            'password' : '1234',
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
    
    # delete와 마찬가지로 패스워드 부분이 문제다
    def test_fail_not_matched_password_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        print(header)
        
        data = {
            'id'       : 1,
            'title'    : 'modify_test',
            'content'  : 'modify_content',
            'password' : '12',
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
class PostingDeleteTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.maxDiff = None
        
        self.tag     = Tag.objects.create(
            id = 1, 
            name = 'test'
            )
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        User.objects.create(
            id       = 1,
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            id          = 1,
            title       = 'testing_post1',
            content     = 'testing_content1',
            password    = hashed_password,
            depth       = 1,
            groupno     = 1,
            orderno     = 1,
            writer_id   = 1,
            tag_id      = 1
        )
        
    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        
    def test_success_delete_posting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'password' : '1234'
        }
        
        response = self.client.post('/boards/delete/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    # 이 부분이 안됨
    # AssertionError: 200 != 400
    # 이렇게 나왔다는 거는 일단 패스워드를 12로 수정을 했는데 이게 반영이 안된다는 뜻
    # 왜 안될까?
    
    def test_fail_not_matched_password(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'password' : '12'
        }
        
        response = self.client.post('/boards/delete/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)