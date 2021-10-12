from unittest import mock
import bcrypt
import json
import jwt

from datetime      import date, datetime
from django.test   import TestCase, Client
from django.http   import response
from boards.models import Board, Tag
from users.models  import User
from my_settings   import SECRET_KEY, algorithm
from unittest.mock import patch, Mock
from freezegun     import freeze_time

class PostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Tag.objects.create(
            id   = 1,
            name = "test"
        )
        
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        
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
            "tag"      : 1
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
            "title1"   : "testing_post",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)

class RePostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()

        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Tag.objects.create(
            id   = 1,
            name = 'test'
        )
        
        User.objects.create(
            id       = 1,
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            id          = 1,
            title       = 'testing_post_1',
            content     = 'testing_content_1',
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

    def test_fail_not_matched_password_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }
        
        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            "id"       : 1,
            "title"    : "modify_test",
            "content"  : "modify_content",
            "password" : "12",
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 401)
        
    def test_fail_key_error_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }
        
        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            "id"       : 1,
            # "title"    : "modify_test",
            "content"  : "modify_content",
            "password" : "1212",
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
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
        
class PostingDeleteTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        
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
        self.assertEqual(response.status_code, 401)

@freeze_time('2021-10-12 00:00:00')
class PostingListViewTest(TestCase):
        
    def setUp(self):
        TestCase.maxDiff = None
        self.client      = Client()
        
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
            title       = 'testing_post_1',
            content     = 'testing_content_1',
            password    = hashed_password,
            depth       = 1,
            groupno     = 1,
            orderno     = 1,
            writer_id   = 1,
            tag_id      = 1,
        )

    def tearDown(self):
        Board.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()

    def test_success_posting_list_view(self):
        
        data = [
            {
            "id"        : 1,
            "title"     : 'testing_post_1',
            "content"   : 'testing_content_1',
            "hits"      : 0,
            "groupno"   : 1,
            "orderno"   : 1,
            "depth"     : 1,
            "writer"    : "runningman",
            "tag"       : "test",
            "create_at" : '2021-10-12 00:00:00'
        }
            ]

        response = self.client.get('/boards/list?offset=0&limit=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : data})