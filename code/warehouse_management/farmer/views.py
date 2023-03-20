from pymongo import MongoClient
import pprint
from django.shortcuts import render
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, 'f-home.html')

def login(request):
    return render(request, 'f-login.html')

def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')

            client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
            db = client['warehouse']
            farmer = db['farmer']
            
            query = {'email': email, 'password': password}
            projection = {'first_name': 1}

            users = farmer.find(query, projection)
            if len(list(users.clone())) == 1:
                context = {
                    'user' : users[0]['first_name']
                }
                return render(request, 'f-home.html', context=context)
            else:
                messages.error(request, "Email or Password incorrect")
                return render(request, 'f-login.html')
        else:
            messages.error(request, "Please enter credentails")
            return render(request, 'f-login.html')

def register(request):
    return render(request, 'f-register.html')


def registerEntry(request):
    if request.method == 'POST':
        if request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('password'):
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            phone_num = request.POST.get('phoneNum')
            email = request.POST.get('email')
            password = request.POST.get('password')

            client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
            db = client['warehouse']
            farmer = db['farmer']


            query = {'email': email}
            projection = {'_id': 1}

            users = farmer.find(query, projection)

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'f-register.html')

            else:
                farmer.insert_one({
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_num': phone_num,
                    'email': email,
                    'password': password
                })

                messages.success(request, 'Registration successful')
                return render(request, 'f-login.html')

        else:
            messages.error(request, "Enter details in all the fields")
            return render(request, 'f-register.html')