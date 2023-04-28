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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

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
    if request.session.get('isLoggedIn', False) == True:
        query = {'email': request.session.get('farmerEmail')}
        projection = {'first_name': 1, 'verified': 1, 'email': 1}

        users = farmer.find(query, projection)

        context = {
            'first_name': users[0]['first_name'],
            'email': users[0]['email']
        }
        return render(request, 'f-home.html', context=context)
    else:
        messages.error(request, 'You need to login first!')
        return render(request, 'f-login.html')

def contact(request):
    return render(request, 'contact.html')

def aboutus(request):
    return render(request, 'aboutUs.html')

def login(request):
    if request.session.get('isLoggedIn', False) == True:
        query = {'email': request.session.get('farmerEmail')}
        projection = {'first_name': 1, 'verified': 1, 'email': 1}

        users = farmer.find(query, projection)
        
        context = {
            'first_name': users[0]['first_name'],
            'email': users[0]['email']
        }
        return render(request, 'f-home.html', context=context)
    else:
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

            users = farmer.find(query, projection)
            if len(list(users.clone())) == 1 and users[0]['verified']:
                request.session['isLoggedIn'] = True
                request.session['farmerEmail'] = email
                context = {
                    'first_name' : users[0]['first_name'],
                    'email': email
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
    else:
        return render(request, 'f-error.html')

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

            pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$")

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'f-register.html')

            elif pattern.match(password) is None:
                messages.error(request, 'Your password should be of length between 8 and 20 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')
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
                messages.success(request, 'Registration successfull !! please check your email for verification.')
                return render(request, 'f-login.html')

        else:
            messages.error(request, "Enter details in all the fields")
            return render(request, 'f-register.html')
    else:
        return render(request, 'f-error.html')

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
    if request.session.get('isLoggedIn', False) == True:
        if request.method == 'POST':
            if request.POST.get('latitude') and request.POST.get('longitude') and request.POST.get('distance'):
                latitude = float(request.POST.get('latitude'))
                longitude = float(request.POST.get('longitude'))
                target_distance = float(request.POST.get('distance'))

                print("Reached here")
                if target_distance < 0:
                    messages.error(request, 'Distance value invalid')
                    return render(request, 'f-search-nearby-warehouses.html')

                query = {}
                projection = {'_id': 0}
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
    if request.session.get('isLoggedIn', False) == True:
        return render(request, 'f-search-nearby-warehouses.html')
    else:
        messages.error(request, 'You need to login first!')
        return render(request, 'f-login.html')

# def storedGoods(request):
#     if request.session['isLoggedIn'] == True:
#         query = {
#             'crops_stored': {
#                 'farmer_id': request.session['farmerId']
#             }
#         }

#         projection = {}

#         warehouse_list = warehouse.find(query, projection)
#         farmer_id = request.session['farmerId']

#         context = {
#             'warehouse_list': warehouse_list,
#             'farmer_id': farmer_id,
#         }
#         return render(request, 'f-stored-goods.html', context=context)
#     else:
#         messages.error(request, 'You need to Login first!')
#         return render(request, 'f-login.html')


def makeReservation(request):
    if request.session.get('isLoggedIn', False) == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)

        context = {
            'items': items_list,
        }
        return render(request, 'f-make-reservation.html', context=context)
    else:
        messages.error(request, 'You need to login first!')
        return render(request, 'f-login.html')


def reservationEntry(request):
    if request.session.get('isLoggedIn', False) == True:
        if request.method == 'POST':
            if request.POST.get('warehouseEmail') and request.POST.get('itemName') and request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get('quantity'):
                warehouse_email = request.POST.get('warehouseEmail')
                item_name = request.POST.get('itemName')
                start_date = request.POST.get('startDate')
                end_date = request.POST.get('endDate')  
                quantity = float(request.POST.get('quantity'))
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

                # print(start_date_obj)
                # print(end_date_obj)

                if start_date_obj > end_date_obj:
                    messages.error(request, 'Invalid start date and end date')
                    return redirect('farmer:makeReservation')

                for i in items_stored_list:
                    t_start_date = datetime.strptime(i['start_date'], format) 
                    t_end_date = datetime.strptime(i['end_date'], format) 
                    if (t_start_date >= start_date_obj and t_start_date <= end_date_obj) or (t_end_date >= start_date_obj and t_end_date <= end_date_obj) or (t_start_date <= start_date_obj and t_end_date >= end_date_obj):
                        quantity_stored += float(i['quantity'])
                
                if quantity_stored + quantity <= float(warehouse_details[0]['storage_capacity']):
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
                    query = {'email': request.session['farmerEmail']}
                    projection = {'email': 1, 'first_name': 1}
                    result = farmer.find(query, projection)
                    subject = "Your Items are updated!!"
                    new_store = f"Reservation ID: {reservation_id} \nWarehouse Email: {warehouse_email} \nItem Name: {item_name} \nStart Date: {start_date}\nEnd Date: {end_date}\nQuantity: {quantity}" 
                    message = "Hello " + result[0]['first_name'] + "!! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [request.session['farmerEmail']]
                    send_mail(subject, message, from_email, to_list, fail_silently=False) 
                    return render(request, 'f-home.html')
                else:
                    messages.error(request, 'Quantity exceeds the warehouse limit')
                    return redirect('farmer:makeReservation')
            else:
                messages.error(request, "Enter details in all the fields")
                return redirect('farmer:makeReservation')
        else:
            return render(request, 'f-error.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')


def showReservations(request):
    if request.session.get('isLoggedIn', False) == True:
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
    if request.session.get('isLoggedIn', False) == True:
        return render(request, 'f-add-item.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def itemEntry(request):
    if request.session.get('isLoggedIn', False) == True:
        if request.method == 'POST':
            if request.POST.get('itemName') and request.POST.get('minTemp') and request.POST.get('maxTemp') and request.POST.get('storageLife') and request.POST.get('isCrop'):
                item_name = request.POST.get('itemName')
                min_temp = request.POST.get('minTemp')
                max_temp = request.POST.get('maxTemp')
                storage_life = int(request.POST.get('storageLife'))
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
                messages.error(request, 'Enter details in all the fields')
                return render(request, 'f-add-item.html')
        else:
            return render(request, 'f-error.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')


def modifyReservation(request, reservation_id):
    if request.session.get('isLoggedIn', False) == True:

        query = {'reservation_id': reservation_id}
        projection = {}

        reservation_check = items_stored.find(query, projection)
        
        if len(list(reservation_check.clone())) == 0:
            messages.error(request, 'Reservation not found!')
            return redirect('farmer:showReservations')

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

def deleteReservation(request, reservation_id):
    if request.session.get('isLoggedIn', False) == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)

        context = {
            'reservation_id': reservation_id,
            'items': items_list,
        }
        

        query = {'reservation_id': reservation_id}
        projection = {'reservation_id': 1, 'warehouse_email': 1, 'start_date': 1, 'end_date': 1, 'quantity': 1, 'item_name': 1}
        stores = items_stored.find(query, projection)
        # print(items_list.item_name)
        query = {'email': request.session['farmerEmail']}
        projection = {'email': 1, 'first_name': 1}
        result = farmer.find(query, projection)
        subject = "Reservation Cancellation!!"
        new_store = f"Item Name: {stores[0]['item_name']} \nStart Date: {stores[0]['start_date']}\nEnd Date: {stores[0]['end_date']}\nQuantity: {stores[0]['quantity']}" 
        message = "Hello " + result[0]['first_name'] + "!! \n" + "Your reservation with following details have been successfully deleted! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.session['farmerEmail']]
        send_mail(subject, message, from_email, to_list, fail_silently=False) 
        items_stored.delete_one({'reservation_id': reservation_id})
        messages.success(request, 'Item deleted successfully')
        return render(request, 'f-home.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def modifyReservationEntry(request, reservation_id):
    if request.session.get('isLoggedIn', False) == True:
        if request.method == 'POST':
            if request.POST.get('warehouseEmail') and request.POST.get('itemName') and request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get('quantity'):
                warehouse_email = request.POST.get('warehouseEmail')
                item_name = request.POST.get('itemName')
                start_date = request.POST.get('startDate')
                end_date = request.POST.get('endDate')  
                quantity = float(request.POST.get('quantity'))


                query = {'reservation_id': reservation_id}
                projection = {}

                reservation_check = items_stored.find(query, projection)
                

                if len(list(reservation_check.clone())) == 0:
                    messages.error(request, 'Reservation not found!')
                    return redirect('farmer:showReservations')
                    
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
                
                if quantity_stored + quantity <= float(warehouse_details[0]['storage_capacity']):
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
                    query = {'email': request.session['farmerEmail']}
                    projection = {'email': 1, 'first_name': 1}
                    result = farmer.find(query, projection)
                    subject = "Your Items are updated!!"
                    new_store = f"Item Name: {item_name} \nStart Date: {start_date}\nEnd Date: {end_date}\nQuantity: {quantity}" 
                    message = "Hello " + result[0]['first_name'] + "!! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [request.session['farmerEmail']]
                    send_mail(subject, message, from_email, to_list, fail_silently=False) 
                    return render(request, 'f-home.html')
                else:
                    messages.error(request, 'Quantity exceeds the warehouse limit')
                    return redirect('farmer:modifyReservation', reservation_id=reservation_id)
            else:
                messages.error(request, "Enter details in all the fields")
                # return render(request, 'f-modify-reservation.html')
                return redirect('farmer:modifyReservation', reservation_id=reservation_id)
        else:
            return render(request, 'f-error.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def showCropSuggestions(request):
    if request.session.get('isLoggedIn', False) == True:
        items_list = items_stored.aggregate([
			{
				'$lookup':
		        {
		           'from': 'Items',
		           'localField': 'item_name',
		           'foreignField': 'name',
		           'as': "item"
		        }
			},
			{
				'$match': {'item.is_crop': True}
			},
            {
                '$group':{
                    '_id': '$item_name',
                    'totQty': {'$sum': '$quantity'}
                },
            },
            {
                '$sort': {'totQty': 1}
            },
            { 
            	'$project': {  
					'_id': 0,
					'name': "$_id",
					'totQty': 1
		   		}
			}
        ])


        context = {
            'items': items_list,
        }

        return render(request, 'f-show-crop-suggestions.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'f-login.html')

def generateReport(request):
    if request.session.get('isLoggedIn', False):
        if True:         
            email = request.session['farmerEmail']
            query = {'farmer_email': email}
            query1 = {'email': email}
            projection = {'warehouse_email': 1, 'item_name': 1, 'start_date': 1, 'end_date': 1, 'quantity': 1}
            projection1 = {'first_name': 1, 'last_name': 1, 'phone_num': 1}
            
            # Retrieve data from the database
            warehouse_details = farmer.find(query1, projection1)
            crop_details = items_stored.find(query, projection)
            
            # Create a list to hold the crop data
            crop_data = []
            for crop in crop_details:
                warehouse_email = crop['warehouse_email']
                crop_name = crop['item_name']
                start_date = crop['start_date']
                end_date = crop['end_date']
                item_name = crop['item_name']
                quantity = crop['quantity']
                crop_data.append([warehouse_email, crop_name, start_date, end_date, item_name, quantity])
            
            # Create a list to hold the crop header row
            crop_header = ['Warehouse Email', 'Crop Name', 'From Date', 'To Date', 'Item Name', 'quantity']
            
            # Create a table object for the crop data and set its style
            crop_table = Table([crop_header] + crop_data, colWidths=[2.5*inch, 1.5*inch, 1.25*inch, 1.25*inch], hAlign='CENTER')
            crop_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 16),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 13),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            
            # Create a list to hold the warehouse data
            warehouse_data = []
            for warehouse_detail in warehouse_details:
                first_name = warehouse_detail['first_name']
                last_name = warehouse_detail['last_name']
                phone_num = warehouse_detail['phone_num']
                farmer_mail = email
                warehouse_data.append(['Farmer first Name', first_name])
                warehouse_data.append(['Farmer last Name', last_name])
                warehouse_data.append(['Phone Number', phone_num])
                warehouse_data.append(['Email ', farmer_mail])
            
            # Create a list to hold the warehouse header row
            warehouse_header = ['Item', 'Value']
            
            # Create a table object for the warehouse data and set its style
            warehouse_table = Table([warehouse_header] + warehouse_data, colWidths=[2.5*inch, 5*inch], hAlign='CENTER')
            warehouse_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.royalblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 18),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.peachpuff),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            # Create a list to hold the elements of the PDF
            elements = []
            styles = getSampleStyleSheet()
            center_style = styles['Heading1']
            center_style.alignment = 1 

            # Header
            space = Spacer(1, 0.2*inch)
            header = Table([[Image('warehouse/static/Images/dalogo.png', width=1*inch, height=1*inch)], [Paragraph('<strong>DA Warehouse</strong>', center_style)]], colWidths=[7.5*inch])
            header.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightskyblue),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 16),
            ]))
            elements.append(header)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            # Add the warehouse heading to the list of elements
             # adjust the height as needed
            warehouse_heading = Paragraph('Warehouse Details', center_style)
            elements.append(warehouse_heading)
            elements.append(space)
            elements.append(space)
            elements.append(space)

            # Add the warehouse table to the list of elements
            elements.append(warehouse_table)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            elements.append(space)
            # Add the crop heading to the list of elements
            crop_heading = Paragraph('Crop Details', center_style)
            elements.append(crop_heading)
            elements.append(space)
            # Add the crop table to the list of elements
            elements.append(crop_table)

            # Create the PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="details.pdf"'
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))
            doc.build(elements)
            return response
        else:
            return render(request, 'f-login.html')
    else:
        messages.error(request, 'Log in First!')
        return render(request, 'f-login.html')
    