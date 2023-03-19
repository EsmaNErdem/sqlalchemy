from unittest import TestCase
from app import app
from flask import request

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BloglyTestCase(TestCase):
    """Tests Blogly Flask app"""

    def test_main_page(self):
        with app.test_client() as client:

            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/add-user">Add More User</a>', html)

    def test_add_user(self):
        with app.test_client() as client:

            resp = client.post('/add-user', data={
                'first-name': 'Esma',
                'last-name' : 'Baker',
                'img-url': 'https://hips.hearstapps.com/hmg-prod/images/dog-jokes-1581711487.jpg?crop=0.684xw:1.00xh;0.274xw,0&resize=1200:*'
            }, follow_redirects=True)

            assert resp.status == '200 OK'
            html = resp.get_data(as_text=True)
            assert resp.request.path == '/'
            self.assertIn('Esma Baker</a></li>', html)

    def test_user_detail(self):
        with app.test_client() as client:

            resp = client.get('/users/1')
            assert resp.status == '200 OK'
            html = resp.get_data(as_text=True)
            self.assertIn('<button formaction="/users/1/delete" formmethod="POST">DELETE USER</button>', html)

    def test_add_post(self):
        with app.test_client() as client:

            resp = client.post('/users/3/posts/new', data={
                'post-title': 'you better work',
                'post-content': 'I hope it works'
            }, follow_redirects=True)

            assert resp.status == '200 OK'
            html = resp.get_data(as_text=True)
            assert resp.request.path == '/users/3'
            self.assertIn('you better work</a></li>', html)


    def test_post_edit(self):
        with app.test_client() as client:

            resp = client.post('/posts/1/edit', data={
                'post-title': 'you better work',
                'post-content': 'I hope it works'
            }, follow_redirects=True)

            assert resp.status == '200 OK'
            html = resp.get_data(as_text=True)
            assert resp.request.path == '/posts/1'
            self.assertIn('<p>I hope it works</p>', html)
            
            # import pdb
            # pdb.set_trace()