from pymongo import MongoClient
import pprint
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from warehouse_management import settings
from django.core.mail import EmailMessage, send_mail


EMAIL = ""
client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['demo']
farmer = db['Farmer']

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
            
            query = {'email': email, 'password': password}
            projection = {'first_name': 1, 'verified': 1}

            users = farmer.find(query, projection)
            if len(list(users.clone())) == 1 and users[0]['verified']:
                request.session['isLoggedIn'] = True
                request.session['farmerId'] = users[0]['_id']
                context = {
                    'user' : users[0]['first_name']
                }
                return render(request, 'f-home.html', context=context)
            elif len(list(users.clone())) == 1 and not users[0]['verified']:
                messages.error(request, "You have not verfied your email")
                return render(request, 'f-login.html')
            else:
                messages.error(request, "Email or Password incorrect")
                return render(request, 'f-login.html')
        else:
            messages.error(request, "Please enter credentails")
            return render(request, 'f-login.html')

def register(request):
    # current_site = get_current_site(request)
    # print("*********" + str(current_site.domain))
    return render(request, 'f-register.html')

def activate(request,uidb64,token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        query = {'email': email}
        projection = {'email': 1, 'verified': 1}
        new_house = farmer.find(query, projection)
        
    except (TypeError,ValueError,OverflowError):
        new_house = [[]]

    if len(list(new_house.clone())) == 1 and generate_token.check_token(email,token):
        print(new_house[0]['verified'])
        myquery = {'email': email}
        newvalues = { "$set": { "verified": True } }
        farmer.update_one(myquery, newvalues)
        new_house[0]['verified'] = True
        print(new_house[0]['verified'])
        # user.profile.signup_confirmation = True
        messages.success(request, "Your Account has been activated!!")
        # print("Hereeeeeeeeeeeeeeeeeeeeeeeee")
        return render(request, 'f-login.html')
    else:
        # print("HEEEEEEEEEEEEEEEEErEEEEEEEEEEEEEEEEEe")
        messages.error(request, "Account activation failed!!")
        return render(request,'f-register.html')

def registerEntry(request):
    if request.method == 'POST':
        if request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('password'):
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            phone_num = request.POST.get('phoneNum')
            email = request.POST.get('email')
            password = request.POST.get('password')
            query = {'email': email}
            projection = {'_id': 1}

            users = farmer.find(query, projection)

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'f-register.html')

            else:
                request.session['isLoggedIn'] = False
                farmer.insert_one({
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_num': phone_num,
                    'email': email,
                    'password': password,
                    'verified': False
                })
                EMAIL = email
                messages.success(request, 'Registration successful')
                # Welcome Email
                subject = "Welcome to farmer Manager!!"
                message = "Hello " + first_name + "!! \n" + "Welcome to DAIICT Warehouse Manager!! \nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nArth Detroja"        
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=False)       
                # Email Address Confirmation Email
                current_site = get_current_site(request)
                # print("*********" + str(current_site.domain))
                email_subject = "Hello Farmer confirm your Email!!"
                message2 = render_to_string('f-email_confirmation.html',{            
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
                messages.success(request, 'Registration successful')
                return render(request, 'f-login.html')

        else:
            messages.error(request, "Enter details in all the fields")
            return render(request, 'f-register.html')


def logout(request):
    request.session['isLoggedIn'] = False
    return render(request, 'f-login.html')

def storedGoods(request):
    if request.session['isLoggedIn'] == True:
        client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
        db = client['warehouse_management']
        warehouse = db['warehouse']

        query = {
            'crops_stored': {
                'farmer_id': request.session['farmerId']
            }
        }

        projection = {}

        warehouse_list = warehouse.find(query, projection)
        farmer_id = request.session['farmerId']

        context = {
            'warehouse_list': warehouse_list,
            'farmer_id': farmer_id,
        }
        return render(request, 'f-stored-goods.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')