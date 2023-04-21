from django.test import TestCase
from . import views

class LoginValidateTestCase(TestCase):
    def test_login_valid(self):
        # Create a request object with POST data
        request = self.client.post('/login', {'email': 'arthdetroja01@gmail.com', 'password': '1'})
        
        # Call the loginValidate function with the request object
        response = loginValidate(request)
        
        # Assert that the response is a redirect to the home page
        self.assertRedirects(response, '/home', status_code=302, target_status_code=200)

    def test_login_unverified(self):
        # Create a request object with POST data
        request = self.client.post('/login', {'email': 'newEmail@gmail.com', 'password': '12'})
        
        # Call the loginValidate function with the request object
        response = loginValidate(request)
        
        # Assert that the response is a render of the login page
        self.assertTemplateUsed(response, 'w-login.html')

    def test_login_invalid(self):
        # Create a request object with POST data
        request = self.client.post('/login', {'email': 'arthdetroja01@gmail.com', 'password': 'wrongpassword'})
        
        # Call the loginValidate function with the request object
        response = loginValidate(request)
        
        # Assert that the response is a render of the login page
        self.assertTemplateUsed(response, 'w-login.html')
