from django.shortcuts import render
from farmer.models import Farmer

# Create your views here.

def login(request):
    return render(request, 'login.html')


def loginValidate(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = Farmer.objects.filer(email__exact=email, password__exact=password)
            if user:
                return render(request, 'home.html')


def register(request):
    return render(request, 'register.html')


def registerEntry(request):
    if request.method == 'POST':
        if request.POST.get('firstName') and request.POST.get('lastName') and request.POST.get('phoneNum') and request.POST.get('email') and request.POST.get('password'):
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            phoneNum = request.POST.get('phoneNum')
            email = request.POST.get('email')
            password = request.POST.get('password')

            record = Farmer(
                first_name = firstName, 
                last_name = lastName,
                phone_number = phoneNum,
                email = email,
                password = password
                )

            record.save()

            return render(request, 'login.html')