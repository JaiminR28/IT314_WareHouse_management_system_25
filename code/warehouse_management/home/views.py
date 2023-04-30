from django.shortcuts import render
from warehouse_management import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def sendQuery(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('name') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('query'):
            name = request.POST.get('name')
            phoneNum = request.POST.get('phoneNum')
            email = request.POST.get('email')
            query = request.POST.get('query')
            title = request.POST.get('title')
            
            subject = "Feedback from user"
            new_store = f"Mr/Mrs {name} has raised the issue with title {title} and query {query}.\n\nContact Details:\nPhone Number: {phoneNum}\nEmail: {email}"
            # message = "Hello " + result[0]['first_name'] + "!! \n" +new_store+ "\n\nThanking You\nArth Detroja"        
            from_email = settings.EMAIL_HOST_USER
            to_list = ['daiict.warehouses@gmail.com']
            send_mail(subject, new_store, from_email, to_list, fail_silently=False)  
            return render(request, 'home.html')
        else:
            # messages.error(request, 'Error performing the request')
            return render(request, 'home.html')
    else:
        # messages.error(request, 'Error performing the request')
        return render(request, 'home.html')