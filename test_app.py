from app import app
from flask import session
from unittest import TestCase



# below shows real python errors rather than flask intercepted html errors if an exception is raised
app.config['TESTING'] = True

# below blocks huge html blocks from FDT from spamming console
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# testing tips
# is there too much logic in your view function? break it up
# separate your tests in multiple files if it makes sense to 
# add multiple assertions per test function 
# test failing things like forms that don't validate (what if form is empty when submitted)

#  python3 -m unittest test_app.py

class ColorViewsTestCase(TestCase):
    # # @classmethod setUpClass tearDownClass runs once at the start and once at the end of this entire body (not for each test inside)
    # @classmethod
    # def setUpClass(cls):
    #     print("INSIDE SET UP CLASS")

    # @classmethod
    # def tearDownClass(cls):
    #     print("INSIDE TEAR DOWN CLASS")

    # # setUp will run before each test, tearDown will run after each test
    # def setUp(self):
    #     print("INSIDE SET UP")

    # def tearDown(self):
    #     print("INSIDE TEAR DOWN")

    def test_color_form(self):
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()
            # can pass query string info below if making get request
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Color Form</h1>', html)
    def test_color_submit(self):
        with app.test_client() as client:
            # getting form with name=color and posting 'orange' to /fav-color
            # if testing large dataset, would probably make a standalone dicionary then pass dict name into where data is below
            res = client.post('/fav-color', data={'color': 'orange'})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Woah! I like orange, too</h3>', html)
    def test_redirection(self):
        with app.test_client() as client:
            res = client.get('/redirect-me')
            self.assertEqual(res.status_code, 302)
            # self.assertEqual(res.location, 'http://localhost:5000/')
            # test client doesn't ask for a port, its just faking it
            self.assertEqual(res.location, 'http://localhost/')
        # separate redirect test below to see what happens after redirect happens
    def test_redirection_followed(self):
        with app.test_client() as client:
            res = client.get('/redirect-me', follow_redirects=True)
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Color Form</h1>', html)

    def test_session_count(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            # session will start from scratch for each request, it acts like a new session
            self.assertEqual(session['count'], 1)

# not optimal to run client.get several times
    # def test_session_count_multiple(self):
    #      with app.test_client() as client:
    #         res = client.get('/')
    #         client.get('/')
    #         client.get('/')
    #         client.get('/')
    #         self.assertEqual(res.status_code, 200)
    #         # session will start from scratch for each request, it acts like a new session
    #         self.assertEqual(session['count'], 4)



    def test_session_count_set(self):
         with app.test_client() as client:
            # below is great for manipulating and changing session data
            with client.session_transaction() as change_session:
                change_session['count'] = 999
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['count'], 1000)
            

# best to keep view functions as clean as possible 
# #example only
#     def test_submit_taxes(self):
#         with app.test_client() as client:
#             res = client.post('/taxes', data={'income': '1000'})
#             html = res.get_data(as_text=True)
#             self.assertEqual(res.status_code, 200)
#             self.assertIn('<h3>You owe $150</h3>', html)
# will need to submit a seprate network request  for each res variable you want to test if 
# you are testing the functionality several different ways, better to separate 

        
# # better to separate network test from funcionality test
# # no need to send network request, separate form data, look in response, etc.
## then after you test the functionality, you can test it once or twice in conjunction with the request flow (integration test)
#     def test_calc_taxes(self):
#         self.assertEqual(calc_taxes(100), 15)
#         self.assertEqual(calc_taxes(10000), 15)
#         self.assertEqual(calc_taxes(0), 15)
#         self.assertEqual(calc_taxes(-23651), 15)
#         self.assertEqual(calc_taxes("asdf"), 15)



# from app import app
# from flask import session
# from unittest import TestCase


# app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


# class ColorViewsTestCase(TestCase):
#     # @classmethod
#     # def setUpClass(cls):
#     #     print("INSIDE SET UP CLASS")

#     # @classmethod
#     # def tearDownClass(cls):
#     #     print("INSIDE TEAR DOWN CLASS")

#     # def setUp(self):
#     #     print("INSIDE SET UP")

#     # def tearDown(self):
#     #     print("INSIDE TEAR DOWN")

#     def test_color_form(self):
#         with app.test_client() as client:
#             res = client.get('/')
#             html = res.get_data(as_text=True)

#             self.assertEqual(res.status_code, 200)
#             self.assertIn('<h1>Color Form</h1>', html)

#     def test_color_submit(self):
#         with app.test_client() as client:
#             res = client.post('/fav-color', data={'color': 'orange'})
#             html = res.get_data(as_text=True)

#             self.assertEqual(res.status_code, 200)
#             self.assertIn('<h3>Woah! I like orange, too</h3>',  html)

#     def test_redirection(self):
#         with app.test_client() as client:
#             res = client.get('/redirect-me')

#             self.assertEqual(res.status_code, 302)
#             self.assertEqual(res.location, 'http://localhost/')

#     def test_redirection_followed(self):
#         with app.test_client() as client:
#             res = client.get('/redirect-me', follow_redirects=True)
#             html = res.get_data(as_text=True)

#             self.assertEqual(res.status_code, 200)
#             self.assertIn('<h1>Color Form</h1>', html)

#     def test_session_count(self):
#         with app.test_client() as client:
#             res = client.get('/')

#             self.assertEqual(res.status_code, 200)
#             self.assertEqual(session['count'], 1)

#     def test_session_count_set(self):
#         with app.test_client() as client:
#             with client.session_transaction() as change_session:
#                 change_session['count'] = 999

#             res = client.get('/')

#             self.assertEqual(res.status_code, 200)
#             self.assertEqual(session['count'], 1000)
