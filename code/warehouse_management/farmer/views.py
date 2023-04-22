from pymongo import MongoClient
import pprint
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from warehouse_management import settings
from django.core.mail import EmailMessage, send_mail
from math import cos, asin, sqrt, pi
from datetime import datetime
import re
import uuid
import os

EMAIL = ""
# client = MongoClient()
client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['demo']
farmer = db['Farmer']
warehouse = db['Warehouse']
items_stored = db['Items_Stored']
items = db['Items']


# Create your views here.

def index(request):
    return render(request, 'f-index.html')

def home(request):
    if request.session['isLoggedIn'] == True:
        return render(request, 'f-home.html')
    else:
        messages.error(request, 'You need to login first!')
        return render(request, 'f-login.html')

def login(request):
    return render(request, 'f-login.html')

def videoCall(request):
    # print(email)
    email = request.session['farmerEmail']
    query = {'email': email}
    projection = {'email': 1, 'first_name': 1}
    users = farmer.find(query, projection)

    room_name = ""
    for i in email:
        if i.isalpha():
            room_name += i

    template_path = os.path.join(settings.BASE_DIR, 'base', 'templates', 'base', 'lobby.html')
    return render(request, template_path, {
        'room': room_name,
        'name': users[0]['first_name'],
    })

def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            query = {'email': email, 'password': password}
            projection = {'first_name': 1, 'verified': 1}

            print(request)
            users = farmer.find(query, projection)
            if len(list(users.clone())) == 1 and users[0]['verified']:
                request.session['isLoggedIn'] = True
                request.session['farmerEmail'] = email
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

            pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$")

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'f-register.html')

            elif pattern.match(password) is None:
                messages.error(request, 'Your password should be of length between 8 and 12 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')
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

def computeDistance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def sortFunc(e):
    return e['distance']

def showNearbyWarehouses(request):
    if request.session['isLoggedIn'] == True:
        if request.method == 'POST':
            if request.POST.get('latitude') and request.POST.get('longitude') and request.POST.get('distance'):
                latitude = float(request.POST.get('latitude'))
                longitude = float(request.POST.get('longitude'))
                target_distance = float(request.POST.get('distance'))
                query = {}
                projection = {}
                warehouse_list = warehouse.find(query, projection)

                nearby_warehouse_list = []
                
                for w in warehouse_list:
                    curr_dist = computeDistance(float(w['latitude']), float(w['longitude']), latitude, longitude)
                    if curr_dist <= target_distance:
                        w['distance'] = round(curr_dist, 2)
                        nearby_warehouse_list.append(w)

                nearby_warehouse_list.sort(key=sortFunc)
                context = {
                    'warehouse_list': nearby_warehouse_list,
                    'distance': target_distance,
                }

                return render(request, 'f-show-nearby-warehouses.html', context=context)
            else:
                messages.error(request, "Enter details in all the fields")
                return render(request, 'f-search-nearby-warehouses.html')
        else:
            return render(request, 'f-error.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def searchNearbyWarehouses(request):
    if request.session['isLoggedIn'] == True:
        return render(request, 'f-search-nearby-warehouses.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def storedGoods(request):
    if request.session['isLoggedIn'] == True:
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


def makeReservation(request):
    if request.session['isLoggedIn'] == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)

        context = {
            'items': items_list,
        }
        return render(request, 'f-make-reservation.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')


def reservationEntry(request):
    if request.session['isLoggedIn'] == True:
        if request.method == 'POST':
            if request.POST.get('warehouseEmail') and request.POST.get('itemName') and request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get('quantity'):
                warehouse_email = request.POST.get('warehouseEmail')
                item_name = request.POST.get('itemName')
                start_date = request.POST.get('startDate')
                end_date = request.POST.get('endDate')  
                quantity = request.POST.get('quantity')
                reservation_id = str(uuid.uuid4())

                # print(start_date)
                # print(end_date)

                query = {}
                projection = {}
                items_stored_list = items_stored.find(query, projection)

                query = {
                    'email': warehouse_email
                }
                
                projection = {}

                warehouse_details = warehouse.find(query, projection)

                if len(list(warehouse_details.clone())) == 0:
                    messages.error(request, 'Warehouse not found!')
                    return redirect('farmer:makeReservation')

                
                quantity_stored = 0
                format = '%Y-%m-%d'

                start_date_obj = datetime.strptime(start_date, format) 
                end_date_obj = datetime.strptime(end_date, format) 

                print(start_date_obj)
                print(end_date_obj)

                if start_date_obj > end_date_obj:
                    messages.error(request, 'Invalid start date and end date')
                    return redirect('farmer:makeReservation')

                for i in items_stored_list:
                    t_start_date = datetime.strptime(i['start_date'], format) 
                    t_end_date = datetime.strptime(i['end_date'], format) 
                    if (t_start_date >= start_date_obj and t_start_date <= end_date_obj) or (t_end_date >= start_date_obj and t_end_date <= end_date_obj) or (t_start_date <= start_date_obj and t_end_date >= end_date_obj):
                        quantity_stored += float(i['quantity'])
                
                if quantity_stored + float(quantity) <= float(warehouse_details[0]['storage_capacity']):
                    messages.success(request, 'Reservation successful')
                    items_stored.insert_one({
                        'reservation_id': reservation_id,
                        'item_name': item_name,
                        'warehouse_email': warehouse_email,
                        'farmer_email': request.session.get('farmerEmail'),
                        'start_date': start_date,
                        'end_date': end_date,
                        'quantity': quantity
                    })
                    return render(request, 'f-home.html')
                else:
                    messages.error(request, 'Quantity exceeds the warehouse limit')
                    return redirect('farmer:makeReservation')
            else:
                messages.error(request, "Enter details in all the fields")
                return redirect('farmer:makeReservation')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')


def showReservations(request):
    if request.session['isLoggedIn'] == True:
        query = {
            'farmer_email': request.session.get('farmerEmail')
        }
        projection = {}
        items_stored_list = items_stored.find(query, projection)

        context = {
            'items': items_stored_list,
        }

        return render(request, 'f-show-reservations.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def addItem(request):
    if request.session['isLoggedIn'] == True:
        return render(request, 'f-add-item.html')
    else:
        return render(request, 'f-login.html')

def itemEntry(request):
    if request.session['isLoggedIn'] == True:
        if request.method == 'POST':
            if request.POST.get('itemName') and request.POST.get('minTemp') and request.POST.get('maxTemp') and request.POST.get('storageLife') and request.POST.get('isCrop'):
                item_name = request.POST.get('itemName')
                min_temp = request.POST.get('minTemp')
                max_temp = request.POST.get('maxTemp')
                storage_life = request.POST.get('storageLife')  
                is_crop = request.POST.get('isCrop') 

                query = {'name': item_name}
                projection = {}

                items_list = items.find(query, projection)

                if len(list(items_list.clone())) != 0:
                    messages.error(request, 'Item Name already present in the system')
                    return render(request, 'f-add-item.html')
                
                if is_crop == 'True':
                    is_crop_bool = True
                else:
                    is_crop_bool = False

                
                items.insert_one({
                    'name': item_name,
                    'min_temperature': min_temp,
                    'max_temperature': max_temp,
                    'storage_life': storage_life,
                    'is_crop': is_crop_bool
                })

                messages.success(request, 'Item entered successfully')
                return redirect('farmer:makeReservation')
            else:
                messages.error(request, "Enter details in all the fields")
                return render(request, 'f-add-item.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')


def modifyReservation(request, reservation_id):
    if request.session['isLoggedIn'] == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)

        context = {
            'reservation_id': reservation_id,
            'items': items_list,
        }
        return render(request, 'f-modify-reservation.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def modifyReservationEntry(request, reservation_id):
    if request.session['isLoggedIn'] == True:
        if request.method == 'POST':
            if request.POST.get('warehouseEmail') and request.POST.get('itemName') and request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get('quantity'):
                warehouse_email = request.POST.get('warehouseEmail')
                item_name = request.POST.get('itemName')
                start_date = request.POST.get('startDate')
                end_date = request.POST.get('endDate')  
                quantity = request.POST.get('quantity')

                # print(start_date)
                # print(end_date)

                query = {}
                projection = {}
                items_stored_list = items_stored.find(query, projection)

                query = {
                    'email': warehouse_email
                }
                
                projection = {}

                warehouse_details = warehouse.find(query, projection)

                if len(list(warehouse_details.clone())) == 0:
                    messages.error(request, 'Warehouse not found!')
                    return redirect('farmer:modifyReservation', reservation_id=reservation_id)

                
                quantity_stored = 0
                format = '%Y-%m-%d'

                start_date_obj = datetime.strptime(start_date, format) 
                end_date_obj = datetime.strptime(end_date, format) 

                # print(start_date_obj)
                # print(end_date_obj)

                if start_date_obj > end_date_obj:
                    messages.error(request, 'Invalid start date and end date')
                    return redirect('farmer:modifyReservation', reservation_id=reservation_id)

                for i in items_stored_list:
                    if i['reservation_id'] != reservation_id:
                        t_start_date = datetime.strptime(i['start_date'], format) 
                        t_end_date = datetime.strptime(i['end_date'], format) 
                        if (t_start_date >= start_date_obj and t_start_date <= end_date_obj) or (t_end_date >= start_date_obj and t_end_date <= end_date_obj) or (t_start_date <= start_date_obj and t_end_date >= end_date_obj):
                            quantity_stored += float(i['quantity'])
                
                if quantity_stored + float(quantity) <= float(warehouse_details[0]['storage_capacity']):
                    messages.success(request, 'Reservation modified successfully')
                    query = {'reservation_id': reservation_id}
                    newvalues = {
                        '$set': {
                            'item_name': item_name,
                            'warehouse_email': warehouse_email,
                            'start_date': start_date,
                            'end_date': end_date,
                            'quantity': quantity
                        }
                    }
                    items_stored.update_one(query, newvalues)
                    return render(request, 'f-home.html')
                else:
                    messages.error(request, 'Quantity exceeds the warehouse limit')
                    return redirect('farmer:modifyReservation', reservation_id=reservation_id)
            else:
                messages.error(request, "Enter details in all the fields")
                # return render(request, 'f-modify-reservation.html')
                return redirect('farmer:modifyReservation', reservation_id=reservation_id)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

