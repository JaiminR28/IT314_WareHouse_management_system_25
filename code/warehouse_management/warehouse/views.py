from django.shortcuts import render, redirect
from django.contrib import messages
import pymongo
from pymongo import MongoClient
import re
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from warehouse_management import settings
from django.core.mail import EmailMessage, send_mail


# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# def check(email):
#     if(re.fullmatch(regex, email)):
#         print("Valid Email") 
#     else:
#         print("Invalid Email")


client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['demo']
warehouse = db['Warehouse']
goods = db['Goods']

EMAIL = ""

def index(request):
    return render(request, 'w-index.html')

def home(request):
    return render(request, 'w-home.html')

def login(request):
    return render(request, 'w-login.html')

def email_confirmation(request):
    return render("w-email_confirmation.html")

def logout(request):
    request.session['isLoggedIn'] = False
    return render(request, 'w-login.html')

def report(request):
    if(request.session['isLoggedIn']):
        return render(request, 'report.html')

def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            query = {'email': email, 'password': password}
            projection = {'email': 1, 'verified': 1}

            users = warehouse.find(query, projection)

            print(users[0]['verified'])
            if len(list(users.clone())) == 1 and users[0]['verified']:
                request.session['isLoggedIn'] = True
                request.session['farmerId'] = users[0]['email']
                context = {
                    'user' : users[0]['email']
                }
                return render(request, 'w-home.html', context=context)
            elif len(list(users.clone())) == 1 and not users[0]['verified']:
                messages.error(request, "You have not verfied your email")
                return render(request, 'w-login.html')
            else:
                messages.error(request, "Email or Password incorrect")
                return render(request, 'w-login.html')
        else:
            messages.error(request, "Please enter credentails")
            return render(request, 'w-login.html')


def register(request):
    return render(request, 'w-register.html')

#Registers new user and saves info in db
def activate(request,uidb64,token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        query = {'email': email}
        projection = {'email': 1, 'verified': 1}
        new_house = warehouse.find(query, projection)
        
    except (TypeError,ValueError,OverflowError):
        new_house = [[]]

    if len(list(new_house.clone())) == 1 and generate_token.check_token(email,token):
        print(new_house[0]['verified'])
        myquery = {'email': email}
        newvalues = { "$set": { "verified": True } }
        warehouse.update_one(myquery, newvalues)
        new_house[0]['verified'] = True
        print(new_house[0]['verified'])
        # user.profile.signup_confirmation = True
        messages.success(request, "Your Account has been activated!!")
        # print("Hereeeeeeeeeeeeeeeeeeeeeeeee")
        return render(request, 'w-login.html')
    else:
        # print("HEEEEEEEEEEEEEEEEErEEEEEEEEEEEEEEEEEe")
        messages.error(request, "Account activation failed!!")
        return render(request,'w-register.html')

def registerEntry(request):
    if request.method == 'POST':
        if request.POST.get('storage_capacity') and request.POST.get('longitude') and request.POST.get('latitude') and request.POST.get('name') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('password'):
        
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
                request.session['isLoggedIn'] = False                
                warehouse.insert_one({
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'storage_capacity': storage_capacity, 
                    'email': email,
                    'verified': False,
                    'password': password,
                    'phone_number': phoneNum,
                })
                EMAIL = email
                messages.success(request, 'Registration successful')
                # Welcome Email
                subject = "Welcome to Warehouse Manager!!"
                message = "Hello " + name + "!! \n" + "Welcome to DAIICT Warehouse Manager!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nArth Detroja"        
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=False)       
                # Email Address Confirmation Email
                current_site = get_current_site(request)
                email_subject = "Confirm your Email @ DAIICT Warehouse manager!!"
                message2 = render_to_string('w-email_confirmation.html',{            
                    'name': email,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(email)),
                    'token': generate_token.make_token(email),
                })
                email_temp = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email_temp.fail_silently = False
                email_temp.send()
                return render(request, 'w-login.html')
        else:
            return render(request, 'w-register.html')
        
def generateReport(request):
    if request.session['isLoggedIn']:
        if request.POST.get('email'):
            email = request.POST.get('email')
            # print(email)
            query = {'warehouse_email': email}
            query1 = {'email': email}
            projection = {'farmer_email': 1, 'crop_name': 1, 'from_date': 1, 'to_date': 1}
            projection1 = {'name': 1, 'latitude': 1, 'longitude': 1, 'storage_capacity': 1, 'phone_number': 1}
            warehouse_details = warehouse.find(query1, projection1)
            crop_details = goods.find(query, projection)
            # print(crop_details[0])
            return render(request, 'report.html', {
                'warehouse_details': warehouse_details,
                'crop_details': crop_details,
            })
        else:
            return render(request, 'w-login.html')
    else:
        messages.error(request, 'Log in First!')
        return render(request, 'w-login.html')
