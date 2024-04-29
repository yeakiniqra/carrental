from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .models import Owner, UploadCar, Booking, ContactMessage
from django.shortcuts import get_object_or_404
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'home.html')
def ownersignup(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if username and contact_no and email and password:
           
            new_owner = Owner(
                username=username,
                contact_no=contact_no,
                email=email,
                password=password
            )
            
            new_owner.save()
            
            
            request.session['owner_username'] = username
            request.session['owner_contact_no'] = contact_no
            request.session['owner_email'] = email
            request.session['owner_password'] = password
            
            
            return redirect('ownerlogin')  
        else:
            messages.error(request, 'All fields are required.')
            return redirect('ownersignup')  
    return render(request, 'ownersignup.html')
    
def owner_profile(request):
    owner_username = request.session.get('owner_username')
    owner_contact_no = request.session.get('owner_contact_no')
    owner_email = request.session.get('owner_email')
    owner_password = request.session.get('owner_password')
    
    if owner_username and owner_contact_no and owner_email:
        context = {
            'owner_username': owner_username,
            'owner_contact_no': owner_contact_no,
            'owner_email': owner_email,
            'owner_password': owner_password 
        }
        return render(request, 'ownerprofile.html', context)
    else:
        
        return HttpResponse('Please Log in first.')
    
def ownerlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if Owner.objects.filter(username=username).exists():
            owner = Owner.objects.get(username=username)
            if owner.password == password:
                
                
                request.session['owner_username'] = owner.username
                request.session['owner_contact_no'] = owner.contact_no
                request.session['owner_email'] = owner.email
                request.session['owner_password'] = owner.password
                
                
                return redirect('owner_profile')
            else:
                
                messages.error(request, 'Invalid password.')
                return redirect('ownerlogin')
        else:
            
            messages.error(request, 'Invalid username.')

    return render(request, 'ownerlogin.html') 


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       
        user = User.objects.create_user(username=username, email=email, password=password)

        
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  

    return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('booking_car')  
         
        else:
            
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')



@login_required
def user_profile(request):
    
    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'userprofile.html', {'bookings': bookings})


def logout(request):
    django_logout(request)
    return redirect('home')

def booking_car(request):
    if request.method == 'POST':
        location = request.POST.get('location', '')
        pickup_date = request.POST.get('pickup-date', '')
        return_date = request.POST.get('return-date', '')

        if location and pickup_date and return_date:
            
            pickup_date_dt = datetime.strptime(pickup_date, '%Y-%m-%dT%H:%M')
            return_date_dt = datetime.strptime(return_date, '%Y-%m-%dT%H:%M')

            
            available_cars = []
            booked_cars = Booking.objects.filter(
                pickup_date__lte=return_date_dt,
                return_date__gte=pickup_date_dt
            ).values_list('car_id', flat=True)

            for car in UploadCar.objects.all():
                if car.id not in booked_cars:
                    
                    days = (return_date_dt - pickup_date_dt).days
                    total_price = car.PricePerDay * days
                    car.total_price = total_price
                    available_cars.append(car)

            context = {
                'cars': available_cars,
                'location': location,
                'pickup_date': pickup_date,
                'return_date': return_date,
            }
            return render(request, 'bookingcar.html', context)
        else:
            error_message = "Please fill up the form completely"
            return render(request, 'bookingcar.html', {'error_message': error_message})
    else:
        return render(request, 'bookingcar.html')
    

def booking_review(request, car_id, location, pickup_date, return_date):
    try:
        
        car = UploadCar.objects.get(pk=car_id)
    except UploadCar.DoesNotExist:
        return redirect('booking_car')  

    
    pickup_date_dt = datetime.strptime(pickup_date, '%Y-%m-%dT%H:%M')
    return_date_dt = datetime.strptime(return_date, '%Y-%m-%dT%H:%M')

    
    days = (return_date_dt - pickup_date_dt).days

    
    total_price = car.PricePerDay * days

    context = {
        'car': car,
        'pickup_date': pickup_date,
        'return_date': return_date,
        'location': location,
        'total_price': total_price,
    }
    return render(request, 'booking_review.html', context)

def upload_car(request):
    if request.method == 'POST':
        
        car_name = request.POST.get('carName')
        car_no = request.POST.get('carNumber')
        mileage = request.POST.get('mileage')
        capacity = request.POST.get('capacity') 
        car_type = request.POST.get('carType')  
        car_condition = request.POST.get('carCondition')
        PricePerDay = request.POST.get('pricePerDay')
        car_image = request.FILES.get('carImage')  

        
        for owner in Owner.objects.all():
            if owner.username == request.user.username:
                break
       
        
        
        
               
        
        new_car = UploadCar(
            owner=owner,  
            car_name=car_name,
            car_no=car_no,
            mileage=mileage,
            capacity=capacity,
            car_type=car_type,
            car_condition=car_condition,
            PricePerDay=PricePerDay,
            car_image=car_image  
        )
        new_car.save()

        
        messages.success(request, 'Car uploaded successfully.')
        return redirect('listed_car',car_id=new_car.id)  

    else:
        capacity_choices = UploadCar.CAPACITY_CHOICES
        car_type_choices = UploadCar.CAR_TYPE_CHOICES

        context = {
            'capacity_choices': capacity_choices,
            'car_type_choices': car_type_choices,
        }
    return render(request, 'uploadcar.html', context)

def update_car(request, car_id):
    car = get_object_or_404(UploadCar, id=car_id)
    
    if request.method == 'POST':
        
        car.car_name = request.POST.get('carName')
        car.car_no = request.POST.get('carNumber')
        car.mileage = request.POST.get('mileage')
        car.capacity = request.POST.get('capacity')
        car.car_type = request.POST.get('carType')
        car.car_condition = request.POST.get('carCondition')
        car.PricePerDay = request.POST.get('pricePerDay')
        
        
        if 'carImage' in request.FILES:
            car.car_image = request.FILES['carImage']
        
        car.save()  
        return redirect('listed_car', car_id=car_id) 
    
    return render(request, 'updatecar.html', {'car': car})

def delete_car(request, car_id):
    car = get_object_or_404(UploadCar, id=car_id)
    
    if request.method == 'POST':
        
        car.delete()
        return redirect('upload_car')  
    
    return render(request, 'delete_car.html', {'car': car})

def owner_cars(request):
    
    if 'owner_username' in request.session:
        owner_username = request.session['owner_username']
        
       
        owner = get_object_or_404(Owner, username=owner_username)

        
        cars = UploadCar.objects.filter(owner=owner)

        context = {
            'owner': owner,
            'cars': cars
        }

        return render(request, 'nowrunning.html', context)




@login_required
def checkout(request, car_id, location, pickup_date, return_date):
    car = UploadCar.objects.get(pk=car_id)

    
    pickup_date_dt = datetime.strptime(pickup_date, '%Y-%m-%dT%H:%M')
    return_date_dt = datetime.strptime(return_date, '%Y-%m-%dT%H:%M')

    
    days = (return_date_dt - pickup_date_dt).days
    total_price = car.PricePerDay * days

    
    booking = Booking.objects.create(
        user=request.user,
        car=car,
        location=location,
        pickup_date=pickup_date_dt,
        return_date=return_date_dt,
        total_price=total_price,
    )

    context = {
        'car_id': car_id,
        'car': car,
        'location': location,
        'pickup_date': pickup_date,
        'return_date': return_date,
        'booking': booking,
    }

    return render(request, 'checkout.html', context)


def generate_pdf(request, car_id, location, pickup_date, return_date):
    
    car = UploadCar.objects.get(pk=car_id)

    
    user = request.user

    
    pickup_date_dt = datetime.strptime(pickup_date, '%Y-%m-%dT%H:%M')
    return_date_dt = datetime.strptime(return_date, '%Y-%m-%dT%H:%M')

    
    days = (return_date_dt - pickup_date_dt).days

    
    total_price = car.PricePerDay * days

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Booking Receipt.pdf"'

    
    p = canvas.Canvas(response, pagesize=letter)

    
    p.setFont("Helvetica", 12)

    
    p.drawString(100, 770, "Receipt for Car Booking")
    p.drawString(100, 750, f"Rented Car: {car.car_name}")
    p.drawString(100, 730, f"Pickup & Return Location: {location}")
    p.drawString(100, 710, f"Pickup Date: {pickup_date_dt.strftime('%d-%m-%Y %H:%M')}")
    p.drawString(100, 690, f"Return Date: {return_date_dt.strftime('%d-%m-%Y %H:%M')}")
    p.drawString(100, 670, f"Total Price: ${total_price}")
    p.drawString(100, 650, f"User Name: {user.username}")
    p.drawString(100, 630, f"User Email: {user.email}")


    
    p.showPage()
    p.save()

    
    return response 


def listed_car(request, car_id):
    car = get_object_or_404(UploadCar, id=car_id)
    return render(request, 'listedcars.html', {'car': car})

def send_message(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        message = request.POST.get('message')

        
        email_message = f"Name: {first_name} {last_name}\nPhone Number: {phone_number}\nEmail: {email}\nMessage: {message}"

        try:
            
            send_mail(
                subject='New Message from Contact Form',
                message=email_message,
                from_email=email,  
                recipient_list=[settings.EMAIL_HOST_USER],  
                fail_silently=False,
            )
            
            return redirect('success_page')  
        except Exception as e:
            messages.error(request, 'Failed to send message. Please try again.')
            return redirect('contact_page') 

    return render(request, 'contact.html')

def contact_page(request):
    return render(request, 'contact.html')

def success_page(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')