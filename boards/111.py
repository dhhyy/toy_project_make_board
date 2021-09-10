    def test_keyerror_posting(self):
        
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