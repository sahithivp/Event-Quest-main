from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from .models import Hall, Booking
from .models import Appointment
from django.utils.timezone import datetime
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
User = get_user_model()

# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email, phone=phone, address=address)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'events/RegistrationForm.html')

# Login View

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage')  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'events/LoginPage.html')

def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")
    return redirect('homepage')

# Homepage View
def homepage(request):
    return render(request, 'events/homepage.html')

#Hall Booking view
def hall_booking(request):
    if request.method == 'POST':
        hall_name = request.POST.get('hall_name')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')
        purpose = request.POST.get('purpose')
        
        # Fetch hall instance
        hall = Hall.objects.get(id=hall_name)
        
        # Save booking data
        Booking.objects.create(
            hall=hall,
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            duration=duration,
            purpose=purpose
        )

        subject = f"Hall Booking Confirmation for {hall.name}"
        message = f"Dear {name},\n\nYour booking for {hall.name} on {date} at {time} is confirmed.\n\nThank you!"
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        return redirect('check_availability')  # Redirect to check availability page after booking

    halls = Hall.objects.all()
    return render(request, 'events/HallBooking.html', {'halls': halls})

# Check Availability view
def check_availability(request):
    booked_halls = []
    available_halls = []

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']

        # Parse input data
        request_time = datetime.strptime(time, '%H:%M').time()
        request_date = datetime.strptime(date, '%Y-%m-%d').date()

        # Get all halls and check their availability status
        for hall in Hall.objects.all():
            overlapping_bookings = Booking.objects.filter(
                hall=hall,
                date=request_date,
            )
            is_available = True

            for booking in overlapping_bookings:
                booking_start = datetime.combine(booking.date, booking.time)
                booking_end = booking_start + timedelta(hours=booking.duration)
                request_start = datetime.combine(request_date, request_time)
                request_end = request_start + timedelta(hours=1)  # Assuming 1-hour duration for the request

                # Check for time overlap
                if (request_start < booking_end and request_end > booking_start):
                    booked_halls.append(hall)  # Add to booked halls if there's an overlap
                    is_available = False
                    break

            # If no overlapping booking found, mark as available
            if is_available:
                available_halls.append(hall)

        return render(request, 'events/CheckAvailability.html', {
            'available_halls': available_halls,
            'booked_halls': booked_halls,
            'date': date,
            'time': time
        })

    return render(request, 'events/CheckAvailability.html')


@csrf_exempt
def submit_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        purpose = request.POST.get('purpose')

        Appointment.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            date=date,
            time=time,
            purpose=purpose
        )

        subject = f"Appointment Confirmation for {date} at {time}"
        message = f"Dear {name},\n\nYour appointment on {date} at {time} has been successfully booked.\n\nThank you!"
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        
        return redirect('view_appointments')
    return render(request, 'events/ScheduleAppointments.html')

def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})



@login_required
def view_profile(request):

    user = request.user

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "Please select a picture to upload.")

    username = user.username
    email = user.email
    phone = user.phone
    address = user.address

    context = {
        'user': user,
        'username': username,
        'email': email,
        'phone': phone,
        'address': address,
    }

    return render(request, 'View_Profile.html', context)
