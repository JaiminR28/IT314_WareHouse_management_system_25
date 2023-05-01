import requests
from pymongo import MongoClient
from django.test import Client, TestCase
import sys
import os
from unittest import mock
from math import pi, cos, asin, sqrt
from datetime import datetime, timedelta
from pprint import pprint
import uuid
from unittest.mock import MagicMock, patch

client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
farmer = db['Farmer']
warehouse = db['Warehouse']
items_stored = db['Items_Stored']
items = db['Items']

# def assertEqual(a, b):
#     if a != b:
#         print('Response: FAIL')
#     else:
#         print("Response: PASS")
# def assertTemplateUsed(response, template):
#     if template not in response.templates[0].name:
#         print('Template: FAIL')
#     else:
#         print("Template: PASS")

# class IndexTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        

#     def test_index(self):
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-index.html')
        
# class LoginTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_login_with_logged_in_user(self):
#         # Make a GET request to the login view
#         response = self.client.get('/farmer/login')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#     def test_login_with_not_logged_in_user(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()

#         # Make a GET request to the login view
#         response = self.client.get('/farmer/login')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#     def test_login_with_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()

#         # Make a GET request to the login view
#         response = self.client.get('/farmer/login')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

# class LoginValidateTestCase(TestCase):
#     def setUp(self):
#         new_user1 = {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_num': '8488887253', 
#             'verified': True   
#         }

#         new_user2 = {
#             'first_name': 'test1',
#             'last_name': 'test1',
#             'email': 'test2@gmail.com',
#             'password': 'testPass',
#             'phone_num': '8488887253',
#             'verified': False 
#         }

#         farmer.insert_many([new_user1, new_user2])

        
#     def test_valid_login(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/login/validate', {'email': 'test1@gmail.com', 'password': 'testPass'})
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-home.html')

#     def test_unverified_login(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/login/validate', {'email': 'test2@gmail.com', 'password': 'testPass'})
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), "You have not verfied your email")

#     def test_invalid_login_email_not_present(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/login/validate', {'email': 'test3@gmail.com', 'password': 'testPass'})
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), "Email or Password incorrect")

#     def test_invalid_login_password_incorrect(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/login/validate', {'email': 'test1@gmail.com', 'password': 'incorrect'})
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), "Email or Password incorrect")

#     def test_with_get_method(self):
#         # Make a POST request to the view
#         response = self.client.get('/farmer/login/validate')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-error.html')

#     def tearDown(self):
#         farmer.delete_many({})



# class RegisterTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()

#     def test_register(self):
#         # Make a GET request to the view
#         response = self.client.get('/farmer/register')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

# class RegistrationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
#         self.new_user1 = {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_num': '8488887253',
#             'verified': True   
#         }
#         farmer.insert_one(self.new_user1)

#     def test_valid_registration(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': 'tP123@#456',
#             'phoneNum': '8488887253'    
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Registration successfull !! please check your email for verification')

#     # Length less than 8
#     def test_invalid_password1(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': 'tP1#345',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')

#     # Empty password
#     def test_invalid_password2(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': '',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Enter details in all the fields')

#     # Length greater than 20
#     def test_invalid_password3(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': 'FOO123bar@#!FOO123bar',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')


#     # Only lowercase
#     def test_invalid_password4(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': 'foobarfoobar',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')

#     # Only uppercase
#     def test_invalid_password5(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': 'FOOBARFOOBAR',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')


#     # Only numbers
#     def test_invalid_password6(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': '12345678',
#             'phoneNum': '8488887253'    
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')

#     # Only special characters
#     def test_invalid_password7(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test2@gmail.com',
#             'password': '@#@#@#@#!!!&&',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')

#     def test_email_present(self):
#         # Make a POST request to the view
#         response = self.client.post('/farmer/register/entry', {
#             'firstName': 'test',
#             'lastName': 'test',
#             'email': 'test1@gmail.com',
#             'password': '@#456',
#             'phoneNum': '8488887253'      
#         })

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-register.html')

#         # Check that the correct message is used
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Email already registered!')



#     def tearDown(self):
#         farmer.delete_many({})



# class LogoutTestCase(TestCase):
#     def test_logout(self):
#         self.client = Client()
#         # simulate a logged-in user by setting isLoggedIn to True
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#         # make a GET request to the logout view
#         response = self.client.get('/farmer/logout')

#         # ensure the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # ensure the isLoggedIn variable in the session is set to False
#         self.assertFalse(self.client.session['isLoggedIn'])

#         # ensure the response uses the f-login.html template
#         self.assertTemplateUsed(response, 'f-login.html')

# class HomeTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         self.new_user1 = {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_num': '8488887253',
#             'verified': True   
#         }
#         farmer.insert_one(self.new_user1)
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test1@gmail.com'
#         session.save()

#     def test_home_with_logged_in_user(self):
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/home')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-home.html')
        
#         # Check that context is present
#         self.assertEqual(response.context['first_name'], 'test')
#         self.assertEqual(response.context['email'], 'test1@gmail.com')

#     def test_home_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/home')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')
    
#     def test_with_anonymous_user(self):
#         # Delete the session variable
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()

#         # Make a GET request to the home view
#         response = self.client.get('/farmer/home')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')

#     def tearDown(self):
#         farmer.delete_many({})

# class SearchNearbyWarehousesTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_with_logged_in_user(self):
#         # Make a GET request to the view
#         response = self.client.get('/farmer/search-nearby-warehouses')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-search-nearby-warehouses.html')
        
#     def test_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/search-nearby-warehouses')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')

#     def test_with_anonymous_user(self):

#         # Delete the session variable
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()

#         # Make a GET request to the home view
#         response = self.client.get('/farmer/search-nearby-warehouses')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')

# class ShowNearbyWarehousesTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#         warehouse.insert_many([
#             {
#                 'name': 'test1',
#                 'latitude': 40.7128,
#                 'longitude': -74.0060,
#                 'storage_capacity': 80, 
#                 'email': 'test1@gmail.com',
#                 'verified': True,
#                 'password': 'password',
#                 'phone_number': '1234567890',
#             },
#             {
#                 'name': 'test2',
#                 'latitude': 37.7749,
#                 'longitude': -122.4194,
#                 'storage_capacity': 80, 
#                 'email': 'test2@gmail.com',
#                 'verified': True,
#                 'password': 'password',
#                 'phone_number': '1234567890',
#             }
#         ])

#     def test_show_nearby_warehouses_with_valid_inputs(self):
#         response = self.client.post('/farmer/show-nearby-warehouses', {
#             'latitude': '40.7282',
#             'longitude': '-73.7949',
#             'distance': '100'
#         })

#         # print(response.context['warehouse_list'])
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-show-nearby-warehouses.html')
#         self.assertQuerysetEqual(
#             response.context['warehouse_list'],
#             [
#                 {
#                     'name': 'test1',
#                     'latitude': 40.7128,
#                     'longitude': -74.0060,
#                     'storage_capacity': 80, 
#                     'email': 'test1@gmail.com',
#                     'verified': True,
#                     'password': 'password',
#                     'phone_number': '1234567890',
#                     'distance': 17.87,
#                 }
#             ]
#         )
#         self.assertEqual(response.context['distance'], 100)

#     def test_show_nearby_warehouses_with_missing_fields(self):
#         response = self.client.post('/farmer/show-nearby-warehouses', {
#             'latitude': '40.7282',
#             'longitude': '-73.7949'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-search-nearby-warehouses.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Enter details in all the fields')

#     def test_show_nearby_warehouses_with_invalid_session(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()

#         response = self.client.post('/farmer/show-nearby-warehouses', {
#             'latitude': '40.7282',
#             'longitude': '-73.7949',
#             'distance': '100'
#         }, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def test_show_nearby_warehouses_with_invalid_request_method(self):
#         response = self.client.get('/farmer/show-nearby-warehouses')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-error.html')

#     def test_show_nearby_warehouses_with_invalid_distance(self):
#         response = self.client.post('/farmer/show-nearby-warehouses', {
#             'latitude': '40.7282',
#             'longitude': '-73.7949',
#             'distance': '-100'
#         })

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-search-nearby-warehouses.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Distance value invalid')

#     def test_show_nearby_warehouses_with_anonymous_user(self):
#         # Delete the session variable
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()

#         # Make a POST request to the home view
#         response = self.client.post('/farmer/show-nearby-warehouses', {
#             'latitude': '40.7282',
#             'longitude': '-73.7949',
#             'distance': '100'
#         })
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def tearDown(self):
#         warehouse.delete_many({})


# class MakeReservationTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_logged_in_user(self):
#         response = self.client.get('/farmer/make-reservation')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')
#         self.assertQuerysetEqual(response.context['items'], [])

#     def test_logged_out_user(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
#         response = self.client.get('/farmer/make-reservation')
#         self.assertTemplateUsed(response, 'f-login.html')
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')

#     def test_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()
#         response = self.client.get('/farmer/make-reservation')
#         self.assertTemplateUsed(response, 'f-login.html')
#         # Check that an error message is displayed
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to login first!')

# class ReservationEntryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test2@gmail.com'
#         session.save()

#         warehouse.insert_one({
#             'name': "test",
#             'latitude': 12.4,
#             'longitude': 12.3,
#             'storage_capacity': 100.0,
#             'email': "test1@gmail.com",
#             'verified': True,
#             'password': 'password',
#             'phone_number': '1234567890'
#         })

#         farmer.insert_one({
#             'first_name': 'test',
#             'last_name': 'test',
#             'phone_num': '1234567890',
#             'email': 'test2@gmail.com',
#             'password': 'password',
#             'verified': True
#         })

#         items.insert_one({
#             'name': 'test',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

#         reservation_id = str(uuid.uuid4())
#         items_stored.insert_one({
#             'reservation_id': reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 10.0
#         })

#     def test_reservation_entry_success(self):
#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 90.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         # self.assertContains(response, 'Reservation successful')
#         self.assertTemplateUsed(response, 'f-home.html')
#         # for item in self.items_stored.find({}, {}):
#         #     pprint(item)
#         self.assertQuerysetEqual([{
#                 'warehouse_email': 'test1@gmail.com',
#                 'farmer_email': 'test2@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 90.0}], items_stored.find({
#                 'warehouse_email': 'test1@gmail.com',
#                 'farmer_email': 'test2@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 90.0
#             }, {'_id': 0, 'reservation_id': 0}))

#     def test_reservation_entry_insufficient_capacity(self):
#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 100.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')

#     def test_reservation_entry_invalid_dates(self):
#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.tomorrow,
#             'endDate': self.today,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')

#     def test_reservation_entry_missing_fields(self):
#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), "Enter details in all the fields")

#     def test_reservation_entry_unauthenticated(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()


#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def test_reservation_entry_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()


#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def test_method_not_post(self):
#         response = self.client.get('/farmer/make-reservation/entry')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-error.html')

#     def test_warehouse_not_found(self):
#         response = self.client.post('/farmer/make-reservation/entry', {
#             'warehouseEmail': 'test@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')

#     def tearDown(self):
#         warehouse.delete_many({'name': 'test'})
#         farmer.delete_many({'first_name': 'test'})
#         items.delete_many({'name': 'test'})
#         items_stored.delete_many({'item_name': 'test'})


# class ShowReservationsTestCase(TestCase):
#     def setUp(self):
#         self.reservation_id = str(uuid.uuid4())
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         items_stored.insert_one({
#             'reservation_id': self.reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 10.0
#         })

#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test2@gmail.com'
#         session.save()


#     def test_show_reservations_authenticated(self):
#         response = self.client.get('/farmer/show-reservations')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-show-reservations.html')
#         self.assertIn('items', response.context)
#         # print("In test case")
#         # for i in response.context['items']:
#         #     print(i)
#         # print(response.context['items'])
        
#         self.assertQuerysetEqual(response.context['items'], items_stored.find({}, {}))

    # def test_show_reservations_unauthenticated(self):
    #     session = self.client.session
    #     session['isLoggedIn'] = False
    #     session.save()
    #     response = self.client.get('/farmer/show-reservations')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-login.html')
    #     messages = list(response.context.get('messages'))
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'You need to Login first!')

    # def test_show_reservations_anonymous_user(self):
    #     session = self.client.session
    #     del session['isLoggedIn']
    #     session.save()
    #     response = self.client.get('/farmer/show-reservations')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-login.html')
    #     messages = list(response.context.get('messages'))
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'You need to Login first!')

    # def tearDown(self):
    #     items_stored.delete_many({})


# class AddItemTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_add_item_authenticated(self):
#         response = self.client.get('/farmer/add-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-add-item.html')

#     def test_add_item_unauthenticated(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
#         response = self.client.get('/farmer/add-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
    
#     def test_add_item_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()
#         response = self.client.get('/farmer/add-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')


# class ItemEntryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#         items.insert_one({
#             'name': 'test1',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#     def test_item_entry_authenticated_post(self):
#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'test2',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'storageLife': 30,
#             'isCrop': 'True'
#         })

#         self.assertEqual(response.status_code, 200)
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Item entered successfully')
#         self.assertTemplateUsed(response, 'f-make-reservation.html')

#     def test_item_entry_authenticated_post_duplicate_item(self):
#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'test1',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'storageLife': 30,
#             'isCrop': 'True'
#         })
#         self.assertEqual(response.status_code, 200)
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Item Name already present in the system')
#         self.assertTemplateUsed(response, 'f-add-item.html')

#     def test_item_entry_authenticated_post_missing_fields(self):
#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-add-item.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Enter details in all the fields')

#     def test_item_entry_authenticated_get(self):
#         response = self.client.get('/farmer/add-item/entry')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-error.html')

#     def test_item_entry_unauthenticated(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()

#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertTemplateUsed(response, 'f-login.html')   
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def test_item_entry_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()

#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertTemplateUsed(response, 'f-login.html')   
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def tearDown(self):
#         items.delete_many({})



# class ModifyReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test2@gmail.com'
#         session.save()

#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.reservation_id = str(uuid.uuid4())
#         items_stored.insert_one({
#             'reservation_id': self.reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 11.0
#         })

#     def test_modify_reservation_with_logged_in_user(self):
#         # Make a GET request to the modifyReservation view
#         response = self.client.get(f'/farmer/modify-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-modify-reservation.html')
        
#         # Check that the reservation_id is in the context
#         self.assertEqual(response.context['reservation_id'], self.reservation_id)
        
#         # Check that the items_list is in the context
#         self.assertQuerysetEqual(response.context['items'], [])
        
#     def test_modify_reservation_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the modifyReservation view
#         response = self.client.get(f'/farmer/modify-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
    
#     def test_modify_reservation_with_anonymous_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()
        
#         # Make a GET request to the modifyReservation view
#         response = self.client.get(f'/farmer/modify-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
        
#     def test_invalid_reservation_id(self):
#         response = self.client.get('/farmer/modify-reservation/1')

#         # Check that the correct template is used
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-show-reservations.html')

#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Reservation not found!')

#     def tearDown(self):
#         items_stored.delete_many({})


# class ModifyReservationEntryTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test3@gmail.com'
#         session.save()
        
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.reservation_id = str(uuid.uuid4())

#         warehouse.insert_many([{
#             'name': "test",
#             'latitude': 12.4,
#             'longitude': 12.3,
#             'storage_capacity': 100,
#             'email': "test1@gmail.com",
#             'verified': True,
#             'password': 'password',
#             'phone_number': '1234567890'
#         }, {
#             'name': "test",
#             'latitude': 12.4,
#             'longitude': 12.3,
#             'storage_capacity': 100,
#             'email': "test2@gmail.com",
#             'verified': True,
#             'password': 'password',
#             'phone_number': '1234567890'
#         }])

#         farmer.insert_one({
#             'first_name': 'test',
#             'last_name': 'test',
#             'phone_num': '1234567890',
#             'email': 'test3@gmail.com',
#             'password': 'password',
#             'verified': True
#         })

#         items.insert_one({
#             'name': 'test',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#         items_stored.insert_one({
#             'reservation_id': self.reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test3@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 10.0
#         })
#     def test_reservation_entry_success(self):
#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test2@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 90.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-show-reservations.html')
#         self.assertQuerysetEqual([{
#                 'warehouse_email': 'test2@gmail.com',
#                 'farmer_email': 'test3@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 90.0}], items_stored.find({
#                 'warehouse_email': 'test2@gmail.com',
#                 'farmer_email': 'test3@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 90.0
#             }, {'_id': 0, 'reservation_id': 0}))

#     def test_reservation_entry_insufficient_capacity(self):
#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test2@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 200.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)

#     def test_reservation_entry_invalid_dates(self):
#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test2@gmail.com',
#             'itemName': 'test',
#             'startDate': self.tomorrow,
#             'endDate': self.today,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)

#     def test_reservation_entry_missing_fields(self):
#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Enter details in all the fields')
#         self.assertTemplateUsed(response, 'f-modify-reservation.html')

#     def test_reservation_entry_unauthenticated(self):
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()


#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')

#     def test_reservation_entry_anonymous_user(self):
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()


#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test1@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-login.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
    
#     def test_method_not_post(self):
#         response = self.client.get(f'/farmer/modify-reservation/entry/{self.reservation_id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-error.html')

#     def test_warehouse_not_found(self):
#         response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
#             'warehouseEmail': 'test@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-modify-reservation.html')

#     def test_invalid_reservation_id(self):
#         response = self.client.post('/farmer/modify-reservation/entry/1', {
#             'warehouseEmail': 'test@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-modify-reservation.html')


#     def tearDown(self):
#         warehouse.delete_many({'name': 'test'})
#         farmer.delete_many({'first_name': 'test'})
#         items.delete_many({'name': 'test'})
#         items_stored.delete_many({'item_name': 'test'})

    

class ShowCropSuggestionsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['isLoggedIn'] = True
        session.save()

        items.insert_many([{
            'name': 'test1',
            'min_temperature': 39,
            'max_temperature': 67,
            'storage_life': 35,
            'is_crop': True
        },{
            'name': 'test2',
            'min_temperature': 39,
            'max_temperature': 67,
            'storage_life': 35,
            'is_crop': True
        },{
            'name': 'test3',
            'min_temperature': 39,
            'max_temperature': 67,
            'storage_life': 35,
            'is_crop': False
        }
        ])

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        items_stored.insert_many([{
            'reservation_id': str(uuid.uuid4()),
            'item_name': 'test1',
            'warehouse_email': 'test1@gmail.com',
            'farmer_email': 'test2@gmail.com',
            'start_date': self.today,
            'end_date': self.tomorrow,
            'quantity': 11.0
        }, {
            'reservation_id': str(uuid.uuid4()),
            'item_name': 'test1',
            'warehouse_email': 'test1@gmail.com',
            'farmer_email': 'test2@gmail.com',
            'start_date': self.today,
            'end_date': self.tomorrow,
            'quantity': 12.0
        }, {
            'reservation_id': str(uuid.uuid4()),
            'item_name': 'test2',
            'warehouse_email': 'test1@gmail.com',
            'farmer_email': 'test2@gmail.com',
            'start_date': self.today,
            'end_date': self.tomorrow,
            'quantity': 33.0
        }, {
            'reservation_id': str(uuid.uuid4()),
            'item_name': 'test3',
            'warehouse_email': 'test1@gmail.com',
            'farmer_email': 'test2@gmail.com',
            'start_date': self.today,
            'end_date': self.tomorrow,
            'quantity': 50.0
        }])

    def test_show_crop_suggestions_success(self):
        response = self.client.get('/farmer/show-crop-suggestions')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'f-show-crop-suggestions.html')
        self.assertQuerysetEqual(response.context['items'], [
            {'name': 'test1', 'totQty': 23.0},
            {'name': 'test2', 'totQty': 33.0}
        ])
        
    def test_show_crop_suggestions_not_logged_in(self):
        session = self.client.session
        session['isLoggedIn'] = False
        session.save()


        response = self.client.get('/farmer/show-crop-suggestions')
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You need to Login first!')  
        self.assertTemplateUsed(response, 'f-login.html')

    def test_show_crop_suggestions_anonymous_user(self):
        session = self.client.session
        del session['isLoggedIn']
        session.save()


        response = self.client.get('/farmer/show-crop-suggestions')
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You need to Login first!')  
        self.assertTemplateUsed(response, 'f-login.html')


    def tearDown(self):
        items_stored.delete_many({})
        items.delete_many({})


# class DeleteReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test2@gmail.com'
#         session.save()

#         farmer.insert_one({
#             'first_name': 'test',
#             'last_name': 'test',
#             'phone_num': '1234567890',
#             'email': 'test2@gmail.com',
#             'password': 'password',
#             'verified': True
#         })
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.reservation_id = str(uuid.uuid4())
#         items_stored.insert_one({
#             'reservation_id': self.reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 11.0
#         })

#     def test_modify_reservation_with_logged_in_user(self):
#         # Make a GET request to the view
#         response = self.client.get(f'/farmer/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-show-reservations.html')
        
#     def test_modify_reservation_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the view
#         response = self.client.get(f'/farmer/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
    
#     def test_modify_reservation_with_anonymous_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         del session['isLoggedIn']
#         session.save()
        
#         # Make a GET request to the view
#         response = self.client.get(f'/farmer/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
        
#     def test_invalid_reservation_id(self):
#         response = self.client.get('/farmer/delete-reservation/1')

#         # Check that the correct template is used
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-show-reservations.html')

#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Reservation not found!')

#     def tearDown(self):
#         items_stored.delete_many({})
