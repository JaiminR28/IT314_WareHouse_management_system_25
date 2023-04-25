import pymongo
import requests
from pymongo import MongoClient
from django.test import Client
from django.test import TestCase
import sys
import os

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

# class LoginTestCase(TestCase):
#     def init(self):
#         print("farmer Login Test Case Started ---------------------------------------------\n\n")
        

#     def setUp(self):
#         # Connect to MongoDB
#         client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = client['demo']
#         self.farmer = db['Farmer']
#         self.farmer = db['farmer']
#         new_user1 = {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         }

#         new_user2 = {
#             'first_name': 'test1',
#             'last_name': 'test1',
#             'email': 'test2@gmail.com',
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         }

#         self.farmer.insert_many([new_user1, new_user2])

        
#     def testValidlogin(self):
#         print('Test Valid Login')
#         response = self.client.post('/farmer/login/validate', {'email': 'test1@gmail.com', 'password': 'testPass'})
#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-home.html')

#     def testUnverifiedLogin(self):
#         print('Test Unverified Login')
#         response = self.client.post('/farmer/login/validate', {'email': 'test2@gmail.com', 'password': 'testPass'})
#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-login.html')

#     def testInvalidLogin(self):
#         print('Test Invalid Login')
#         response = self.client.post('/farmer/login/validate', {'email': 'test3@gmail.com', 'password': 'testPass'})
#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-login.html')

#     def tearDown(self):
#         self.farmer.delete_many({'name': 'test'})



# class RegistrationTestCase(TestCase):
#     def init(self):
#         print("farmer Registration Test Case Started ---------------------------------------------\n\n")

#     def setUp(self):
#         # Connect to MongoDB
#         client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = client['demo']
#         self.farmer = db['farmer']
#         new_user1 = {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         }
#         self.farmer.insert_one(new_user1)

#     def testValidRegistration(self):
#         print('Test Valid Registration')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-login.html')

#     def testInvalidPassword1(self):
#         print('Test Invalid Password 1')

#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'test',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testInvalidPassword2(self):
#         print('Test Invalid Password 2')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': '',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')


#     def testInvalidPassword3(self):
#         print('Test Invalid Password 3')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPasssample',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testInvalidPassword4(self):
#         print('Test Invalid Password 4')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'afad',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testInvalidPassword5(self):
#         print('Test Invalid Password 5')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'tsafadf',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testInvalidPassword6(self):
#         print('Test Invalid Password 6')
#         response = self.client.post('/farmer/register/entry',{
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'tefhgdh',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testInvalidPassword7(self):
#         print('Test Invalid Password 7')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass141342312',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def testAlreadyRegistered(self):
#         print('Test Already Registered')
#         response = self.client.post('/farmer/register/entry', {
#             'first_name': 'test',
#             'last_name': 'test',
#             'email': 'test1@gmail.com',
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         })

#         assertEqual(response.status_code, 200)
#         assertTemplateUsed(response, 'f-register.html')

#     def tearDown(self):
#         self.farmer.delete_many({'name':'test'})

class ModifyReservationTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Set up a session for testing
        session = self.client.session
        session['isLoggedIn'] = True
        session.save()

    def test_modify_reservation_with_logged_in_user(self):
        # Make a GET request to the modifyReservation view
        response = self.client.get('/farmer/modify-reservation/1')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-modify-reservation.html')
        
        # Check that the reservation_id is in the context
        self.assertEqual(response.context['reservation_id'], '1')
        
        # Check that the items_list is in the context
        self.assertQuerysetEqual(response.context['items'], [])
        
    def test_modify_reservation_with_logged_out_user(self):
        # Remove isLoggedIn from the session
        session = self.client.session
        session['isLoggedIn'] = False
        session.save()
        
        # Make a GET request to the modifyReservation view
        response = self.client.get('/farmer/modify-reservation/1')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-login.html')
        
        # Check that the error message is in the response
        self.assertContains(response, 'You need to Login first!')


class AddItemTestCase(TestCase):
    def setUp(self):
        # Set up a session for testing
        session = self.client.session
        session['isLoggedIn'] = True
        session.save()

    def test_add_item_with_logged_in_user(self):
        # Make a GET request to the addItem view
        response = self.client.get('/farmer/add-item')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-add-item.html')
        
    def test_add_item_with_logged_out_user(self):
        # Remove isLoggedIn from the session
        session = self.client.session
        session['isLoggedIn'] = False
        session.save()
        # Make a GET request to the addItem view
        response = self.client.get('/farmer/add-item')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-login.html')
