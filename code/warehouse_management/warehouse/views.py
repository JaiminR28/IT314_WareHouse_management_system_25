from django.shortcuts import render
from django.contrib import messages
import pymongo
from pymongo import MongoClient
import re

# Create your views here.
# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# def check(email):
#     if(re.fullmatch(regex, email)):
#         print("Valid Email") 
#     else:
#         print("Invalid Email")

client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['demo']
warehouse = db['Warehouse']
manager = db['Manager']

def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'w-login.html')


def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            query = {'email': email, 'password': password}
            projection = {'email': 1}

            users = manager.find(query, projection)
            if len(list(users.clone())) == 1:
                context = {
                    'user' : users[0]['email']
                }
                return render(request, 'w-home.html', context=context)
            else:
                messages.error(request, "Email or Password incorrect")
                return render(request, 'w-login.html')
        else:
            messages.error(request, "Please enter credentails")
            return render(request, 'w-login.html')


def register(request):
    return render(request, 'w-register.html')

def registerEntry(request):
    if request.method == 'POST':
        if request.POST.get('storage_capacity') and request.POST.get('longitude') and request.POST.get('latitude') and request.POST.get('name') and request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('password'):
            
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            phoneNum = request.POST.get('phoneNum')
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            storage_capacity = request.POST.get('storage_capacity')

            # if(not check(email)):
            #     messages.error(request, "Invalid E-mail address")
            #     return render(request, 'w-register.html')
            
            query = {'email': email}
            projection = {'_id': 1}

            users = warehouse.find(query, projection)

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'w-register.html')
            
            else:
                warehouse.insert_one({
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'storage_capacity': storage_capacity, 
                    'email': email,
                })
                manager.insert_one({
                    'first_name': firstName, 
                    'last_name': lastName,
                    'phone_number': phoneNum,
                    'email': email,
                    'password': password,
                    'latitude': latitude,
                    'longitude': longitude,
                })
                messages.success(request, 'Registration successful')
                return render(request, 'w-login.html')
        else:
            return render(request, 'w-register.html')