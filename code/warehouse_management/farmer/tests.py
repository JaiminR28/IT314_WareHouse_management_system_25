import requests
from pymongo import MongoClient
from django.test import Client, TestCase
import sys
import os
from unittest import mock
from math import pi, cos, asin, sqrt


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


class ReservationEntryTestCase(TestCase):

    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            email="test@test.com",
            storage_capacity=100
        )

        self.farmer = Farmer.objects.create(
            email="test@test.com",
            first_name="Test",
            last_name="Farmer",
            password="testpassword"
        )

        self.item = Item.objects.create(
            name="Test Item",
            description="Test description",
            price=10.00
        )

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    def test_reservation_entry_success(self):
        reservation_id = str(uuid.uuid4())
        response = self.client.post(reverse('farmer:reservationEntry'), {
            'warehouseEmail': self.warehouse.email,
            'itemName': self.item.name,
            'startDate': self.today,
            'endDate': self.tomorrow,
            'quantity': 10
        }, follow=True)

        self.assertContains(response, 'Reservation successful')
        self.assertTrue(ItemsStored.objects.filter(reservation_id=reservation_id).exists())

    def test_reservation_entry_insufficient_capacity(self):
        response = self.client.post(reverse('farmer:reservationEntry'), {
            'warehouseEmail': self.warehouse.email,
            'itemName': self.item.name,
            'startDate': self.today,
            'endDate': self.tomorrow,
            'quantity': 200
        }, follow=True)

        self.assertContains(response, 'Quantity exceeds the warehouse limit')

    def test_reservation_entry_invalid_dates(self):
        response = self.client.post(reverse('farmer:reservationEntry'), {
            'warehouseEmail': self.warehouse.email,
            'itemName': self.item.name,
            'startDate': self.tomorrow,
            'endDate': self.today,
            'quantity': 10
        }, follow=True)

        self.assertContains(response, 'Invalid start date and end date')

    def test_reservation_entry_missing_fields(self):
        response = self.client.post(reverse('farmer:reservationEntry'), {
            'warehouseEmail': self.warehouse.email,
            'itemName': self.item.name,
            'startDate': self.today,
            'endDate': self.tomorrow,
        }, follow=True)

        self.assertContains(response, 'Enter details in all the fields')

    def test_reservation_entry_unauthenticated(self):
        response = self.client.post(reverse('farmer:reservationEntry'), {
            'warehouseEmail': self.warehouse.email,
            'itemName': self.item.name,
            'startDate': self.today,
            'endDate': self.tomorrow,
            'quantity': 10
        }, follow=True)

        self.assertContains(response, 'You need to Login first!')
        self.assertTemplateUsed(response, 'f-login.html')


# class ModifyReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session.save()

#     def test_modify_reservation_with_logged_in_user(self):
#         # Make a GET request to the modifyReservation view
#         response = self.client.get('/farmer/modify-reservation/1')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-modify-reservation.html')
        
#         # Check that the reservation_id is in the context
#         self.assertEqual(response.context['reservation_id'], '1')
        
#         # Check that the items_list is in the context
#         self.assertQuerysetEqual(response.context['items'], [])
        
#     def test_modify_reservation_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the modifyReservation view
#         response = self.client.get('/farmer/modify-reservation/1')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'f-login.html')
        
#         # Check that the error message is in the response
#         self.assertContains(response, 'You need to Login first!')


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
