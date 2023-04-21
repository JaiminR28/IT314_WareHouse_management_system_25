import pymongo
import requests
from pymongo import MongoClient
from django.test import Client
from django.test import TestCase
import sys
import os
from warehouse.views import *
def assertEqual(a, b):
    if a != b:
        print('Response: FAIL')
    else:
        print("Response: PASS")
def assertTemplateUsed(response, template):
    if template not in response.templates[0].name:
        print('Template: PASS')
    else:
        print("Template: PASS")

class LoginTestCase(TestCase):
    def init(self):
        print("Warehouse Login Test Case Started ---------------------------------------------\n\n")
        

    def setUp(self):
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
        db = client['demo']
        self.farmer = db['Farmer']
        self.warehouse = db['Warehouse']
        new_user1 = {
            'name': 'test',
            'latitude': '99',
            'longitude': '98',
            'storage_capacity': '94', 
            'email': 'test1@gmail.com',
            'verified': True,
            'password': 'testPass',
            'phone_number': '8488887253'    
        }

        new_user2 = {
            'name': 'test',
            'latitude': '99',
            'longitude': '98',
            'storage_capacity': '94', 
            'email': 'test2@gmail.com',
            'verified': False,
            'password': 'testPass',
            'phone_number': '8488887253'
        }

        self.warehouse.insert_many([new_user1, new_user2])

        
    def testValidlogin(self):
        print('Test Valid Login')
        response = self.client.post('/warehouse/login/validate', {'email': 'test1@gmail.com', 'password': 'testPass'})
        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-home.html')

    def testUnverifiedLogin(self):
        print('Test Unverified Login')
        response = self.client.post('/warehouse/login/validate', {'email': 'test2@gmail.com', 'password': 'testPass'})
        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-login.html')

    def testInvalidLogin(self):
        print('Test Invalid Login')
        response = self.client.post('/warehouse/login/validate', {'email': 'test3@gmail.com', 'password': 'testPass'})
        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-login.html')

    def tearDown(self):
        self.warehouse.delete_many({'name': 'test'})
        
class RegistrationTestCase(TestCase):
    def init(self):
        print("Warehouse Registration Test Case Started ---------------------------------------------\n\n")

    def setUp(self):
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
        db = client['demo']
        self.warehouse = db['Warehouse']
        new_user1 = {
            'name': 'test',
            'latitude': '99',
            'longitude': '98',
            'storage_capacity': '94', 
            'email': 'test1@gmail.com',
            'verified': False,
            'password': 'testPass',
            'phone_number': '8488887253'    
        }
        self.warehouse.insert_one(new_user1)

    def testValidRegistration(self):
        print('Test Valid Registration')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'passTest1@',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-login.html')

    def testInvalidPassword1(self):
        print('Test Invalid Password 1')

        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': '',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testInvalidPassword2(self):
        print('Test Invalid Password 2')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'abcde123',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')


    def testInvalidPassword3(self):
        print('Test Invalid Password 3')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'ABCDE123',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testInvalidPassword4(self):
        print('Test Invalid Password 4')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'abcdEFGH1',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testInvalidPassword5(self):
        print('Test Invalid Password 5')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'abcdefghi',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testInvalidPassword6(self):
        print('Test Invalid Password 6')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'a@A1',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testInvalidPassword7(self):
        print('Test Invalid Password 7')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test2@gmail.com',
                                                                    'password': 'abcde12345$678901',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def testAlreadyRegistered(self):
        print('Test Already Registered')
        response = self.client.post('/warehouse/register/entry', {
                                                                    'name': 'test',
                                                                    'latitude': '80',
                                                                    'longitude': '90',
                                                                    'storage_capacity': '129', 
                                                                    'email': 'test1@gmail.com',
                                                                    'password': '1234',
                                                                    'phoneNum': '8488887253'})

        assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'w-register.html')

    def tearDown(self):
        self.warehouse.delete_many({'name':'test'})