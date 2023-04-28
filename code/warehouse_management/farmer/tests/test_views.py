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

class IndexTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        

    def test_index(self):
        # Make a GET request to the home view
        response = self.client.get('/farmer/')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-index.html')
        
class LoginTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        # Set up a session for testing
        session = self.client.session
        session['isLoggedIn'] = True
        session.save()

    def test_login_with_logged_in_user(self):
        # Make a GET request to the home view
        response = self.client.get('/farmer/login')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-home.html')

    def test_login_with_not_logged_in_user(self):
        session = self.client.session
        session['isLoggedIn'] = False
        session.save()

        # Make a GET request to the home view
        response = self.client.get('/farmer/login')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'f-login.html')

# class HomeTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_home_with_logged_in_user(self):
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/home')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-home.html')
        
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


# class LogoutTestCase(TestCase):
    # def test_logout(self):
    #     self.client = Client()
    #     # simulate a logged-in user by setting isLoggedIn to True
    #     session = self.client.session
    #     session['isLoggedIn'] = True
    #     session.save()

#         # make a GET request to the logout view
#         response = self.client.get('/farmer/logout')

#         # ensure the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # ensure the isLoggedIn variable in the session is set to False
#         self.assertFalse(self.client.session['isLoggedIn'])

#         # ensure the response uses the f-login.html template
#         self.assertTemplateUsed(response, 'f-login.html')


# class ShowNearbyWarehousesTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.warehouse = db['Warehouse']

#         self.warehouse.insert_many([
#             {
#                 'name': 'test',
#                 'latitude': 40.7128,
#                 'longitude': -74.0060,
#                 'storage_capacity': 80, 
#                 'email': 'test1@gmail.com',
#                 'verified': True,
#                 'password': 'password',
#                 'phone_number': '1234567890',
#             },
#             {
#                 'name': 'test',
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
#                     'name': 'test',
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
#         self.assertContains(response, 'Enter details in all the fields')

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
#         self.assertContains(response, 'You need to Login first!')

#     def test_show_nearby_warehouses_with_invalid_request_method(self):
#         response = self.client.get('/farmer/show-nearby-warehouses')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-error.html')

#     def tearDown(self):
#         self.warehouse.delete_many({'name': 'test'})



# class SearchNearbyWarehousesTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_home_with_logged_in_user(self):
#         # Make a GET request to the home view
#         response = self.client.get('/farmer/search-nearby-warehouses')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-search-nearby-warehouses.html')
        
#     def test_home_with_logged_out_user(self):
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



# class MakeReservationTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session.save()

#     def test_successful_request(self):
#         response = self.client.get('/farmer/make-reservation')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-make-reservation.html')
#         self.assertQuerysetEqual(response.context['items'], [])

#     def test_unauthenticated_request(self):
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/farmer/make-reservation')
#         self.assertTemplateUsed(response, 'f-login.html')
#         self.assertContains(response, 'You need to login first!')


# class ReservationEntryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session['farmerEmail'] = 'test2@gmail.com'
#         self.session.save()

#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.warehouse = db['Warehouse']
#         self.farmer = db['Farmer']
#         self.items = db['Items']
#         self.items_stored = db['Items_Stored']

#         self.warehouse.insert_one({
#             'name': "test",
#             'latitude': 12.4,
#             'longitude': 12.3,
#             'storage_capacity': 100,
#             'email': "test1@gmail.com",
#             'verified': True,
#             'password': 'password',
#             'phone_number': '1234567890'
#         })

#         self.farmer.insert_one({
#             'first_name': 'test',
#             'last_name': 'test',
#             'phone_num': '1234567890',
#             'email': 'test2@gmail.com',
#             'password': 'password',
#             'verified': True
#         })

#         self.items.insert_one({
#             'name': 'test',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # def test_reservation_entry_success(self):
    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 10.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     # self.assertContains(response, 'Reservation successful')
    #     self.assertTemplateUsed(response, 'f-home.html')
    #     # for item in self.items_stored.find({}, {}):
    #     #     pprint(item)
    #     self.assertQuerysetEqual([{
    #             'warehouse_email': 'test1@gmail.com',
    #             'farmer_email': 'test2@gmail.com',
    #             'item_name': 'test',
    #             'start_date': self.today,
    #             'end_date': self.tomorrow,
    #             'quantity': 10.0}], self.items_stored.find({
    #             'warehouse_email': 'test1@gmail.com',
    #             'farmer_email': 'test2@gmail.com',
    #             'item_name': 'test',
    #             'start_date': self.today,
    #             'end_date': self.tomorrow,
    #             'quantity': 10.0
    #         }, {'_id': 0, 'reservation_id': 0}))

    # def test_reservation_entry_insufficient_capacity(self):
    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 10.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Quantity exceeds the warehouse limit')
    #     self.assertTemplateUsed(response, 'f-make-reservation.html')

    # def test_reservation_entry_invalid_dates(self):
    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.tomorrow,
    #         'endDate': self.today,
    #         'quantity': 10.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-make-reservation.html')

    # def test_reservation_entry_missing_fields(self):
    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Enter details in all the fields')
    #     self.assertTemplateUsed(response, 'f-make-reservation.html')

    # def test_reservation_entry_unauthenticated(self):
    #     self.client = Client()
    #     self.session = self.client.session
    #     self.session['isLoggedIn'] = False
    #     self.session.save()


    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 10
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'You need to Login first!')
    #     self.assertTemplateUsed(response, 'f-login.html')


    # def test_method_not_post(self):
    #     response = self.client.get('/farmer/make-reservation/entry')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-error.html')

    # def test_warehouse_not_found(self):
    #     response = self.client.post('/farmer/make-reservation/entry', {
    #         'warehouseEmail': 'test@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-make-reservation.html')

    # def tearDown(self):
    #     self.warehouse.delete_many({'name': 'test'})
    #     self.farmer.delete_many({'first_name': 'test'})
    #     self.items.delete_many({'name': 'test'})
    #     self.items_stored.delete_many({'item_name': 'test'})


# class ShowReservationsTestCase(TestCase):
#     def setUp(self):
#         reservation_id = str(uuid.uuid4())
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.items_stored = db['Items_Stored']
#         self.items_stored.insert_one({
#             'reservation_id': reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 10.0
#         })

#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session['farmerEmail'] = 'test2@gmail.com'
#         self.session.save()


#     def test_show_reservations_authenticated(self):
#         response = self.client.get('/farmer/show-reservations')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-show-reservations.html')
#         self.assertIn('items', response.context)

#     def test_show_reservations_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/farmer/show-reservations')
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'f-login.html')

# class AddItemTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session.save()

#     def test_add_item_authenticated(self):
#         response = self.client.get('/farmer/add-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-add-item.html')

#     def test_add_item_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/farmer/add-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'f-login.html')


# class ItemEntryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session.save()

#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.items = db['Items']

#         self.items.insert_one({
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
#         # Not working
#         self.assertEqual(response.status_code, 302)
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
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()

#         response = self.client.post('/farmer/add-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'f-login.html')   

    # def tearDown(self):
    #     self.items.delete_many({})


# class ModifyReservationEntryTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test3@gmail.com'
#         session.save()
        
#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.warehouse = db['Warehouse']
#         self.farmer = db['Farmer']
#         self.items = db['Items']
#         self.items_stored = db['Items_Stored']
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.reservation_id = str(uuid.uuid4())

#         self.warehouse.insert_many([{
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

#         self.farmer.insert_one({
#             'first_name': 'test',
#             'last_name': 'test',
#             'phone_num': '1234567890',
#             'email': 'test3@gmail.com',
#             'password': 'password',
#             'verified': True
#         })

#         self.items.insert_one({
#             'name': 'test',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#         self.items_stored.insert_one({
#             'reservation_id': self.reservation_id,
#             'item_name': 'test',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 11.0
#         })
    # def test_reservation_entry_success(self):
    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test2@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 10.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     # self.assertContains(response, 'Reservation successful')
    #     self.assertTemplateUsed(response, 'f-home.html')
    #     # for item in self.items_stored.find({}, {}):
    #     #     pprint(item)
    #     # Not working
    #     # self.assertQuerysetEqual([{
    #     #         'warehouse_email': 'test2@gmail.com',
    #     #         'farmer_email': 'test3@gmail.com',
    #     #         'item_name': 'test',
    #     #         'start_date': self.today,
    #     #         'end_date': self.tomorrow,
    #     #         'quantity': 10.0}], self.items_stored.find({
    #     #         'warehouse_email': 'test2@gmail.com',
    #     #         'farmer_email': 'test3@gmail.com',
    #     #         'item_name': 'test',
    #     #         'start_date': self.today,
    #     #         'end_date': self.tomorrow,
    #     #         'quantity': 10.0
    #     #     }, {'_id': 0, 'reservation_id': 0}))

    # def test_reservation_entry_insufficient_capacity(self):
    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test2@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 200.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)

    # def test_reservation_entry_invalid_dates(self):
    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test2@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.tomorrow,
    #         'endDate': self.today,
    #         'quantity': 10.0
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)

    # def test_reservation_entry_missing_fields(self):
    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Enter details in all the fields')
    #     self.assertTemplateUsed(response, 'f-modify-reservation.html')

    # def test_reservation_entry_unauthenticated(self):
    #     self.client = Client()
    #     self.session = self.client.session
    #     self.session['isLoggedIn'] = False
    #     self.session.save()


    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test1@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #         'quantity': 10
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'You need to Login first!')
    #     self.assertTemplateUsed(response, 'f-login.html')


    # def test_method_not_post(self):
    #     response = self.client.get(f'/farmer/modify-reservation/entry/{self.reservation_id}')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-error.html')

    # def test_warehouse_not_found(self):
    #     response = self.client.post(f'/farmer/modify-reservation/entry/{self.reservation_id}', {
    #         'warehouseEmail': 'test@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-modify-reservation.html')

    # def test_invalid_reservation_id(self):
    #     response = self.client.post('/farmer/modify-reservation/entry/1', {
    #         'warehouseEmail': 'test@gmail.com',
    #         'itemName': 'test',
    #         'startDate': self.today,
    #         'endDate': self.tomorrow,
    #     }, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-show-reservations.html')


    # def tearDown(self):
    #     self.warehouse.delete_many({'name': 'test'})
    #     self.farmer.delete_many({'first_name': 'test'})
    #     self.items.delete_many({'name': 'test'})
    #     self.items_stored.delete_many({'item_name': 'test'})

    
# class ModifyReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['farmerEmail'] = 'test2@gmail.com'
#         session.save()
        
#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.items_stored = db['Items_Stored']
#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.reservation_id = str(uuid.uuid4())
#         self.items_stored.insert_one({
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
#         self.assertContains(response, 'You need to Login first!')

    # def test_invalid_reservation_id(self):
    #     response = self.client.get('/farmer/modify-reservation/1')
    #     # Not working
    #     # self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'f-show-reservations.html')

    # def tearDown(self):
    #     self.items_stored.delete_many({})


# class ShowCropSuggestionsTestCase(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session.save()

        
#         mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         db = mongo_client['test']
#         self.items_stored = db['Items_Stored']
#         self.items = db['Items']

#         self.items.insert_many([{
#             'name': 'test1',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         },{
#             'name': 'test2',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         },{
#             'name': 'test3',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': False
#         }
#         ])

#         self.today = datetime.now().strftime('%Y-%m-%d')
#         self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
#         self.items_stored.insert_many([{
#             'reservation_id': str(uuid.uuid4()),
#             'item_name': 'test1',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 11.0
#         }, {
#             'reservation_id': str(uuid.uuid4()),
#             'item_name': 'test1',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 12.0
#         }, {
#             'reservation_id': str(uuid.uuid4()),
#             'item_name': 'test2',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 33.0
#         }, {
#             'reservation_id': str(uuid.uuid4()),
#             'item_name': 'test3',
#             'warehouse_email': 'test1@gmail.com',
#             'farmer_email': 'test2@gmail.com',
#             'start_date': self.today,
#             'end_date': self.tomorrow,
#             'quantity': 50.0
#         }])

#     def test_show_crop_suggestions_success(self):
#         response = self.client.get('/farmer/show-crop-suggestions')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'f-show-crop-suggestions.html')

#         # Not working 
#         # self.assertQuerysetEqual(response.context['items'], [
#         #     {'name': 'test1', 'totQty': 23.0},
#         #     {'name': 'test2', 'totQty': 33.0}
#         # ])
        
#     def test_show_crop_suggestions_not_logged_in(self):
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/farmer/show-crop-suggestions')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')  
#         self.assertTemplateUsed(response, 'f-login.html')

#     def tearDown(self):
#         self.items_stored.delete_many({})
#         self.items.delete_many({})



# class AddItemTestCase(TestCase):
#     def setUp(self):
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_add_item_with_logged_in_user(self):
#         # Make a GET request to the addItem view
#         response = self.client.get('/farmer/add-item')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-add-item.html')
        
#     def test_add_item_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
#         # Make a GET request to the addItem view
#         response = self.client.get('/farmer/add-item')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
