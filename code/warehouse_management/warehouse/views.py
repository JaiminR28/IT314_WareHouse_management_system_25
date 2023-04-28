from django.shortcuts import render, redirect
from django.contrib import messages
import pymongo
from pymongo import MongoClient
import re
import os
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from warehouse_management import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


# Create your views here.
# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# def check(email):
#     if(re.fullmatch(regex, email)):
#         print("Valid Email") 
#     else:
#         print("Invalid Email")

# client = MongoClient()
client = MongoClient('mongodb+srv://arth01:passadmin@cluster0.z4s5bj0.mongodb.net/?retryWrites=true&w=majority')
db = client['demo']
warehouse = db['Warehouse']
goods = db['Goods']
farmer = db['Farmer']
items_stored = db['Items_Stored']
items = db['Items']

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
        return render(request, 'w-report.html')
    
def performVideoCall(request):
    return render(request, 'w-video.html')

def videoCall(request):
    if request.method == 'POST':
        if request.POST.get('userEmail') and request.POST.get('managerEmail'):
            userEmail = request.POST.get('userEmail')
            managerEmail = request.POST.get('managerEmail')
            # print(userEmail)
            query = {'email': managerEmail}
            projection = {'email': 1, 'name': 1}
            managers = warehouse.find(query, projection)

            room_name = ""
            for i in userEmail:
                if i.isalpha():
                    room_name += i

            template_path = os.path.join(settings.BASE_DIR, 'base', 'templates', 'base', 'lobby.html')
            return render(request, template_path, {
                'room': room_name,
                'name': managers[0]['name']
            })

def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            query = {'email': email, 'password': password}
            projection = {'email': 1, 'verified': 1, 'name': 1}

            users = warehouse.find(query, projection)

            # print(users[0]['verified'])
            if len(list(users.clone())) == 1 and users[0]['verified']:
                request.session['isLoggedIn'] = True
                request.session['farmerId'] = users[0]['email']
                context = {
                    'user' : users[0]['email'],
                    'name' : users[0]['name']
                }
                request.session['warehouseEmail'] = email
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

            pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$")

            if len(list(users.clone())) != 0:
                messages.error(request, 'Email already registered!')
                return render(request, 'w-register.html')

            elif pattern.match(password) is None:
                messages.error(request, 'Your password should be of length between 8 and 12 including atleast one uppercase, one lowercase, one number and one special character (@$!%*?&)')
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



def generatePDF(request):
    # request.session['isLoggedIn']
    if request.session['isLoggedIn']:
        if True:         
            email = request.session['warehouseEmail']
            query = {'warehouse_email': email}
            query1 = {'email': email}
            projection = {'farmer_email': 1, 'item_name': 1, 'start_date': 1, 'end_date': 1, 'quantity': 1}
            projection1 = {'name': 1, 'latitude': 1, 'longitude': 1, 'storage_capacity': 1, 'phone_number': 1}
            
            # Retrieve data from the database
            warehouse_details = warehouse.find(query1, projection1)
            crop_details = items_stored.find(query, projection)
            
            # Create a list to hold the crop data
            crop_data = []
            for crop in crop_details:
                farmer_email = crop['farmer_email']
                crop_name = crop['item_name']
                start_date = crop['start_date']
                end_date = crop['end_date']
                item_name = crop['item_name']
                quantity = crop['quantity']
                crop_data.append([farmer_email, crop_name, start_date, end_date, item_name, quantity])
            
            # Create a list to hold the crop header row
            crop_header = ['Farmer Email', 'Crop Name', 'From Date', 'To Date', 'Item Name', 'quantity']
            
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
                name = warehouse_detail['name']
                latitude = warehouse_detail['latitude']
                longitude = warehouse_detail['longitude']
                storage_capacity = warehouse_detail['storage_capacity']
                phone_number = warehouse_detail['phone_number']
                warehouse_data.append(['Warehouse Name', name])
                warehouse_data.append(['Latitude', str(latitude)])
                warehouse_data.append(['Longitude', str(longitude)])
                warehouse_data.append(['Storage Capacity', str(storage_capacity)])
                warehouse_data.append(['Phone Number', phone_number])
            
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
            header = Table([[Image('C:/Users/Tom/Desktop/IT314_WareHouse_management_system_25/code/warehouse_management/warehouse/static/Images/dalogo.png', width=1*inch, height=1*inch)], [Paragraph('<strong>DA Warehouse</strong>', center_style)]], colWidths=[7.5*inch])
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
            return render(request, 'w-login.html')
    else:
        messages.error(request, 'Log in First!')
        return render(request, 'w-login.html')

def generate_pdf(email):
    if True:
        if True:      
            # email = request.session['warehouseEmail']
            query = {'warehouse_email': email}
            query1 = {'email': email}
            projection = {'farmer_email': 1, 'item_name': 1, 'start_date': 1, 'end_date': 1, 'quantity': 1}
            projection1 = {'name': 1, 'latitude': 1, 'longitude': 1, 'storage_capacity': 1, 'phone_number': 1}
            
            # Retrieve data from the database
            warehouse_details = warehouse.find(query1, projection1)
            crop_details = items_stored.find(query, projection)
            
            # Create a list to hold the crop data
            crop_data = []
            for crop in crop_details:
                farmer_email = crop['farmer_email']
                crop_name = crop['item_name']
                start_date = crop['start_date']
                end_date = crop['end_date']
                item_name = crop['item_name']
                quantity = crop['quantity']
                crop_data.append([farmer_email, crop_name, start_date, end_date, item_name, quantity])
            
            # Create a list to hold the crop header row
            crop_header = ['Farmer Email', 'Crop Name', 'From Date', 'To Date', 'Item Name', 'quantity']
            
            
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
                name = warehouse_detail['name']
                latitude = warehouse_detail['latitude']
                longitude = warehouse_detail['longitude']
                storage_capacity = warehouse_detail['storage_capacity']
                phone_number = warehouse_detail['phone_number']
                warehouse_data.append(['Warehouse Name', name])
                warehouse_data.append(['Latitude', str(latitude)])
                warehouse_data.append(['Longitude', str(longitude)])
                warehouse_data.append(['Storage Capacity', str(storage_capacity)])
                warehouse_data.append(['Phone Number', phone_number])
            
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
            header = Table([[Image('C:/Users/Tom/Desktop/IT314_WareHouse_management_system_25/code/warehouse_management/warehouse/static/Images/dalogo.png', width=1*inch, height=1*inch)], [Paragraph('<strong>DA Warehouse</strong>', center_style)]], colWidths=[7.5*inch])
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
            # response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="details.pdf"'
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            doc.build(elements)
            
            pdf_data = buffer.getvalue()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            response.write(pdf_data)
            return response

def mailPDF(request):
    # request.session['isLoggedIn']
    if request.session['isLoggedIn']:
        email = request.session['warehouseEmail']
        pdf = generate_pdf(email)
        send_email = EmailMessage('Warehouse Report', 'Here is your warehouse report.', settings.EMAIL_HOST_USER, [email])
        send_email.attach('report.pdf', pdf.getvalue(), 'application/pdf')
        send_email.send()
        messages.success(request, "Email sent successfully")
        query = {'email': email}
        projection = {'name': 1}
        result = warehouse.find(query, projection)
        context = {
            'name': result[0]['name'],
            'user': email
        }
        return render(request, 'w-home.html', context=context)
    else:
        # return render(request, 'w-login.html')
        messages.error(request, 'Log in First!')
        return render(request, 'w-login.html')
    

def showReservations(request):
    if request.session['isLoggedIn'] == True:
        query = {
            'warehouse_email': request.session['warehouseEmail']
        }
        projection = {}
        items_stored_list = items_stored.find(query, projection)
        data_list = []
        print(items_stored_list)
        for i in items_stored_list:
            data_list.append(i)
        context = {
            'items': data_list,
        }

        return render(request, 'w-show-reservations.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')

def addJustItem(request):
    if request.session['isLoggedIn'] == True:
        return render(request, 'w-add-just-item.html')
    return render(request, 'w-login.html')
    
def addItem(request):
    if request.session['isLoggedIn'] == True:
        return render(request, 'w-add-item.html')
    else:
        return render(request, 'w-login.html')

def itemJustEntry(request):
    if request.session['isLoggedIn'] == True:
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
                    return render(request, 'w-add-item.html')
                
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
                return redirect('warehouse:home')
            else:
                messages.error(request, "Enter details in all the fields")
                return render(request, 'w-add-item.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')

def itemEntry(request):
    if request.session['isLoggedIn'] == True:
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
                    return render(request, 'w-add-item.html')
                
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
                return redirect('warehouse:showReservation')
            else:
                messages.error(request, "Enter details in all the fields")
                return render(request, 'w-add-item.html')
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')
    
def modifyReservation(request, reservation_id):
    if request.session['isLoggedIn'] == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)        
        data_list = []
        for i in items_list:
            data_list.append(i)
        query = {'reservation_id': reservation_id}
        projection = {'farmer_email': 1, 'quantity': 1}
        farmer_mail = items_stored.find(query, projection)
        # print(data_list)
        context = {
            'reservation_id': reservation_id,
            'items': data_list,
            'farmer_mail': farmer_mail[0]['farmer_email'],
            'quantity': farmer_mail[0]['quantity']
        }
        return render(request, 'w-modify-reservation.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')
    
def deleteReservation(request, reservation_id):
    if request.session['isLoggedIn'] == True:
        query = {}
        projection = {}

        items_list = items.find(query, projection)

        context = {
            'reservation_id': reservation_id,
            'items': items_list,
        }       

        query = {'reservation_id': reservation_id}
        projection = {'reservation_id': 1, 'farmer_email': 1, 'start_date': 1, 'end_date': 1, 'quantity': 1, 'item_name': 1}
        stores = items_stored.find(query, projection)
        # print(items_list.item_name)
        query = {'email': stores[0]['farmer_email']}
        projection = {'email': 1, 'first_name': 1}
        result = farmer.find(query, projection)
        subject = "Reservation Cancellation!!"
        new_store = f"Item Name: {stores[0]['item_name']} \nStart Date: {stores[0]['start_date']}\nEnd Date: {stores[0]['end_date']}\nQuantity: {stores[0]['quantity']}" 
        message = "Hello " + result[0]['first_name'] + "!! \n" + "Your reservation with following details have been successfully deleted! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [stores[0]['farmer_email']]
        send_mail(subject, message, from_email, to_list, fail_silently=False) 
        items_stored.delete_one({'reservation_id': reservation_id})
        messages.success(request, 'Item deleted successfully')
        return render(request, 'w-home.html', context=context)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')

def modifyReservationEntry(request, reservation_id):
    if request.session['isLoggedIn'] == True:
        if request.method == 'POST':
            if request.POST.get('farmerEmail') and request.POST.get('itemName') and request.POST.get('startDate') and request.POST.get('endDate') and request.POST.get('quantity'):
                farmer_email = request.POST.get('farmerEmail')
                item_name = request.POST.get('itemName')
                start_date = request.POST.get('startDate')
                end_date = request.POST.get('endDate')  
                quantity = float(request.POST.get('quantity'))

                # print(start_date)
                # print(end_date)

                query = {}
                projection = {}
                items_stored_list = items_stored.find(query, projection)

                query = {
                    'email': request.session['warehouseEmail']
                }
                
                projection = {}

                warehouse_details = warehouse.find(query, projection)

                if len(list(warehouse_details.clone())) == 0:
                    messages.error(request, 'Farmer not found!')
                    return redirect('warehouse:modifyReservation', reservation_id=reservation_id)

                
                quantity_stored = 0
                format = '%Y-%m-%d'

                start_date_obj = datetime.strptime(start_date, format) 
                end_date_obj = datetime.strptime(end_date, format) 

                # print(start_date_obj)
                # print(end_date_obj)

                if start_date_obj > end_date_obj:
                    messages.error(request, 'Invalid start date and end date')
                    return redirect('warehouse:modifyReservation', reservation_id=reservation_id)

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
                            'farmer_email': farmer_email,
                            'start_date': start_date,
                            'end_date': end_date,
                            'quantity': quantity
                        }
                    }

                    query = {'email': farmer_email}
                    projection = {'email': 1, 'first_name': 1}
                    result = farmer.find(query, projection)
                    subject = "Your Items are updated!!"
                    new_store = f"Item Name: {item_name} \nStart Date: {start_date}\nEnd Date: {end_date}\nQuantity: {quantity}" 
                    message = "Hello " + result[0]['first_name'] + "!! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [farmer_email]
                    send_mail(subject, message, from_email, to_list, fail_silently=False)  

                    items_stored.update_one(query, newvalues)


                    query = {'email': request.session['warehouseEmail']}
                    projection = {'name': 1}
                    result = warehouse.find(query, projection)
                    
                    context = {
                        'user': request.session['warehouseEmail'],
                        'name': result[0]['name']
                    }

                    return render(request, 'w-home.html', context=context)
                else:
                    messages.error(request, 'Quantity exceeds the warehouse limit')
                    return redirect('warehouse:modifyReservation', reservation_id=reservation_id)
            else:
                messages.error(request, "Enter details in all the fields")
                # return render(request, 'w-modify-reservation.html')
                return redirect('warehouse:modifyReservation', reservation_id=reservation_id)
    else:
        messages.error(request, 'You need to Login first!')
        return render(request, 'w-login.html')