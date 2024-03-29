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


mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = mongo_client['test']
items_stored = db['Items_Stored']
farmer = db['Farmer']
warehouse = db['Warehouse']
items = db['Items']

# def assertEqual(a, b):
#     if a != b:
#         print('Response: FAIL')
#     else:
#         print("Response: PASS")
# def assertTemplateUsed(response, template):
#     if template not in response.templates[0].name:
#         print('Template: PASS')
#     else:
#         print("Template: PASS")

# class LoginTestCase(TestCase):
#     def setUp(self):
#         # Connect to MongoDB
#         # client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         # db = client['test']
#         # self.farmer = db['Farmer']
#         # self.warehouse = db['Warehouse']
#         new_user1 = {
#             'name': 'test',
#             'latitude': '99',
#             'longitude': '98',
#             'storage_capacity': '94', 
#             'email': 'test1@gmail.com',
#             'verified': True,
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         }

#         new_user2 = {
#             'name': 'test',
#             'latitude': '99',
#             'longitude': '98',
#             'storage_capacity': '94', 
#             'email': 'test2@gmail.com',
#             'verified': False,
#             'password': 'testPass',
#             'phone_number': '8488887253'
#         }

#         warehouse.insert_many([new_user1, new_user2])

        
#     def testValidlogin(self):
#         # print('Test Valid Login')
#         response = self.client.post('/warehouse/login/validate', {'email': 'test1@gmail.com', 'password': 'testPass'})
#         self.assertEqual(response.status_code, 200)
#         messages = list(response.context.get('messages'))
#         # print(str(messages[0]))
#         # self.assertTemplateUsed(response, 'w-home.html')

#     def testUnverifiedLogin(self):
#         # print('Test Unverified Login')
#         response = self.client.post('/warehouse/login/validate', {'email': 'test2@gmail.com', 'password': 'testPass'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-login.html')

#     def testInvalidLogin(self):
#         # print('Test Invalid Login')
#         response = self.client.post('/warehouse/login/validate', {'email': 'test3@gmail.com', 'password': 'testPass'})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-login.html')

#     def tearDown(self):
#         warehouse.delete_many({'name': 'test'})
        

# class RegistrationTestCase(TestCase):
#     def init(self):
#         print("Warehouse Registration Test Case Started ---------------------------------------------\n\n")

#     def setUp(self):
#         # Connect to MongoDB
#         # client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         # db = client['test']
#         # self.warehouse = db['Warehouse']
#         new_user1 = {
#             'name': 'test',
#             'latitude': '99',
#             'longitude': '98',
#             'storage_capacity': '94', 
#             'email': 'test1@gmail.com',
#             'verified': False,
#             'password': 'testPass',
#             'phone_number': '8488887253'    
#         }
#         warehouse.insert_one(new_user1)

#     def testValidRegistration(self):
#         # print('Test Valid Registration')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'passTest1@',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-login.html')

#     def testInvalidPassword1(self):
#         # print('Test Invalid Password 1')

#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': '',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testInvalidPassword2(self):
#         # print('Test Invalid Password 2')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'abcde123',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')


#     def testInvalidPassword3(self):
#         # print('Test Invalid Password 3')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'ABCDE123',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testInvalidPassword4(self):
#         # print('Test Invalid Password 4')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'abcdEFGH1',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testInvalidPassword5(self):
#         # print('Test Invalid Password 5')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'abcdefghi',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testInvalidPassword6(self):
#         # print('Test Invalid Password 6')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'a@A1',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testInvalidPassword7(self):
#         # print('Test Invalid Password 7')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test2@gmail.com',
#                                                                     'password': 'abcde12345$678901',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def testAlreadyRegistered(self):
#         # print('Test Already Registered')
#         response = self.client.post('/warehouse/register/entry', {
#                                                                     'name': 'test',
#                                                                     'latitude': '80',
#                                                                     'longitude': '90',
#                                                                     'storage_capacity': '129', 
#                                                                     'email': 'test1@gmail.com',
#                                                                     'password': '1234',
#                                                                     'phoneNum': '8488887253'})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-register.html')

#     def tearDown(self):
#         warehouse.delete_many({})
# Create your tests here.


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
#         self.session['warehouseEmail'] = 'test2@gmail.com'
#         self.session.save()


#     def test_show_reservations_authenticated(self):
#         response = self.client.get('/warehouse/show-reservations')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-show-reservations.html')
#         self.assertIn('items', response.context)

#     def test_show_reservations_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/warehouse/show-reservations')
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'w-login.html')

# class AddItemTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session.save()

#     def test_add_item_authenticated(self):
#         response = self.client.get('/warehouse/add-just-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-add-just-item.html')

#     def test_add_item_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()
#         response = self.client.get('/warehouse/add-just-item')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'w-login.html')


# class ItemEntryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = True
#         self.session['warehouseEmail'] = 'test2@gmail.com'
#         self.session.save()

#         # mongo_client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
#         # db = mongo_client['test']
#         # self.items = db['Items']
#         warehouse.insert_one({
#             'name': 'test',
#             'latitude': 80,
#             'longitude': 90,
#             'storage_capacity': 129,
#             'email': 'test2@gmail.com',
#             'verified': True,
#             'phone_number': 1234567890,
#             'password': 'temp1234'
#         })
#         items.insert_one({
#             'name': 'test1',
#             'min_temperature': 39,
#             'max_temperature': 67,
#             'storage_life': 35,
#             'is_crop': True
#         })

#     def test_item_entry_authenticated_post(self):
#         response = self.client.post('/warehouse/add-just-item/entry', {
#             'itemName': 'test2',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'storageLife': 30,
#             'isCrop': 'True'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-home.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Item entered successfully')

#     def test_item_entry_authenticated_post_duplicate_item(self):
#         response = self.client.post('/warehouse/add-just-item/entry', {
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
#         self.assertTemplateUsed(response, 'w-add-just-item.html')

#     def test_item_entry_authenticated_post_missing_fields(self):
#         response = self.client.post('/warehouse/add-just-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-add-just-item.html')
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Enter details in all the fields')

#     def test_item_entry_authenticated_get(self):
#         response = self.client.get('/warehouse/add-just-item/entry')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-error.html')

#     def test_item_entry_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()

#         response = self.client.post('/warehouse/add-just-item/entry', {
#             'itemName': 'Test Item',
#             'minTemp': 10,
#             'maxTemp': 20,
#             'isCrop': 'True'
#         })
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'w-login.html')   

#     def tearDown(self):
#         items.delete_many({})
#         warehouse.delete_many({})



# class ModifyReservationEntryTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['warehouseEmail'] = 'test1@gmail.com'
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
#             'quantity': 11.0
#         })
#     def test_reservation_entry_success(self):
#         response = self.client.post(f'/warehouse/modify-reservation/entry/{self.reservation_id}', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-home.html')
#         # for item in self.items_stored.find({}, {}):
#         #     pprint(item)
#         self.assertQuerysetEqual([{
#                 'warehouse_email': 'test1@gmail.com',
#                 'farmer_email': 'test3@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 10.0}], items_stored.find({
#                 'warehouse_email': 'test1@gmail.com',
#                 'farmer_email': 'test3@gmail.com',
#                 'item_name': 'test',
#                 'start_date': self.today,
#                 'end_date': self.tomorrow,
#                 'quantity': 10.0
#             }, {'_id': 0, 'reservation_id': 0}))

#     def test_reservation_entry_insufficient_capacity(self):
#         response = self.client.post(f'/warehouse/modify-reservation/entry/{self.reservation_id}', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 200.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)

#     def test_reservation_entry_invalid_dates(self):
#         response = self.client.post(f'/warehouse/modify-reservation/entry/{self.reservation_id}', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.tomorrow,
#             'endDate': self.today,
#             'quantity': 10.0
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)

#     def test_reservation_entry_missing_fields(self):
#         response = self.client.post(f'/warehouse/modify-reservation/entry/{self.reservation_id}', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Enter details in all the fields')
#         self.assertTemplateUsed(response, 'w-show-reservations.html')

#     def test_reservation_entry_unauthenticated(self):
#         self.client = Client()
#         self.session = self.client.session
#         self.session['isLoggedIn'] = False
#         self.session.save()


#         response = self.client.post(f'/warehouse/modify-reservation/entry/{self.reservation_id}', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#             'quantity': 10
#         }, follow=True)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'You need to Login first!')
#         self.assertTemplateUsed(response, 'w-login.html')


#     def test_method_not_post(self):
#         response = self.client.get(f'/warehouse/modify-reservation/entry/{self.reservation_id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-error.html')

#     def test_invalid_reservation_id(self):
#         response = self.client.post('/warehouse/modify-reservation/entry/1', {
#             'farmerEmail': 'test3@gmail.com',
#             'itemName': 'test',
#             'startDate': self.today,
#             'endDate': self.tomorrow,
#         }, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-show-reservations.html')


#     def tearDown(self):
#         warehouse.delete_many({})
#         farmer.delete_many({})
#         items.delete_many({})
#         items_stored.delete_many({})

    
# class ModifyReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['warehouseEmail'] = 'test1@gmail.com'
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

#         warehouse.insert_one({
#             'name': "test",
#             'latitude': 12.4,
#             'longitude': 12.3,
#             'storage_capacity': 100,
#             'email': "test1@gmail.com",
#             'verified': True,
#             'password': 'password',
#             'phone_number': '1234567890'
#         })

#     def test_modify_reservation_with_logged_in_user(self):
#         # Make a GET request to the modifyReservation view
#         response = self.client.get(f'/warehouse/modify-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-modify-reservation.html')
        
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
#         response = self.client.get(f'/warehouse/modify-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-login.html')
        
#         # Check that the error message is in the response
#         self.assertContains(response, 'You need to Login first!')

#     def test_invalid_reservation_id(self):
#         response = self.client.get('/warehouse/modify-reservation/1')
#         # Not working
#         # self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'w-show-reservations.html')

# #     def tearDown(self):
# #         items_stored.delete_many({})

# class DeleteReservationTestCase(TestCase):
#     def setUp(self):
#         # Create a test client
#         self.client = Client()
        
#         # Set up a session for testing
        

#         session = self.client.session
#         session['isLoggedIn'] = True
#         session['warehouseEmail'] = 'test2@gmail.com'
#         session.save()

#         warehouse.insert_one({
#             'name': 'test',
#             'latitude': 1,
#             'longitude': 1,
#             'phone_num': '1234567890',
#             'email': 'test2@gmail.com',
#             'password': 'password',
#             'storage_capacity': 100,
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
#         response = self.client.get(f'/warehouse/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-show-reservations.html')
        
#     def test_modify_reservation_with_logged_out_user(self):
#         # Remove isLoggedIn from the session
#         session = self.client.session
#         session['isLoggedIn'] = False
#         session.save()
        
#         # Make a GET request to the view
#         response = self.client.get(f'/warehouse/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-login.html')
        
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
#         response = self.client.get(f'/warehouse/delete-reservation/{self.reservation_id}')
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-login.html')
        
#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'You need to Login first!')
        
#     def test_invalid_reservation_id(self):
#         response = self.client.get('/warehouse/delete-reservation/1')

#         # Check that the correct template is used
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, 'w-show-reservations.html')

#         # Check that the error message is in the response
#         messages = list(response.context.get('messages'))
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(str(messages[0]), 'Reservation not found!')

#     def tearDown(self):
#         items_stored.delete_many({})


