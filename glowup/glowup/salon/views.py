from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AppointmentForm, ProfileForm, BookingForm
from .models import Appointment, Offer, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserChangeForm
from .forms import OfferForm
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'salon/login.html')

def home_view(request):
    return render(request, 'salon/home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('register')
        
        user = User.objects.create_user(username=email, password=password, first_name=name)
        auth_login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('login')

    return render(request, 'salon/register.html')



def admin_login(request):
    error_message=None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin_user = authenticate(request, username=email, password=password)

        if admin_user is not None and admin_user.is_superuser:
            # auth_login(request, admin_user)
            return redirect('admin_dashboard')
        else:
            error_message="Invalid credentialas"

    return render(request, 'salon/admin_login.html',{'error_message': error_message})


@login_required
def user_dashboard(request):
    return render(request, 'salon/user_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'salon/admin_dashboard.html')

def about(request):
    return render(request, 'salon/about.html')

def book_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('appointment_success.html')
    else:
        form = BookingForm()
    return render(request, 'salon/appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'appointment_success.html')

def facial(request):
    return render(request, 'salon/facial.html')

def haircut(request):
    return render(request, 'salon/haircut.html')

def massage(request):
    return render(request, 'salon/massage.html')

def manicure_pedicure(request):
    return render(request, 'salon/manicure_pedicure.html')

def bridal_makeup(request):
    return render(request, 'salon/bridal_makeup.html')

def waxing(request):
    return render(request, 'salon/waxing.html')

def services(request):
    return render(request, 'salon/services.html')

def appointments_view(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
    else:
        appointments = []
    return render(request, 'salon/appointments.html', {'appointments': appointments})

def booking_history(request):
    print(f"Authenticated user: {request.user}")  # Debug statement
    past_bookings = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'salon/booking_history.html', {'bookings': past_bookings})
@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')

        request.user.first_name = name
        request.user.username = email
        request.user.save()

        if avatar:
            profile.avatar = avatar
            profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

    return render(request, 'salon/profile.html', {'profile': profile})

@login_required
def support_view(request):
    return render(request, 'salon/support.html')


@login_required
def manage_users(request):
    users = User.objects.all()  # Corrected to fetch all users
    context = {'users': users}
    return render(request, 'salon/manage_users.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'salon/edit_user.html', {'form': form})

# Delete user
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')

@login_required
def manage_offers(request):
    offers = Offer.objects.all()

    # Handle offer addition
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_offers')  # Redirect to the same page to see the new offer
    else:
        form = OfferForm()

    context = {
        'offers': offers,
        'form': form  # Include the form in the context
    }
    return render(request, 'salon/manage_offers.html', context)
@login_required
def system_settings(request):
    return render(request, 'salon/system_settings.html')

@login_required
def admin_logout(request):
    logout(request)  # Add logout functionality here
    return redirect('admin_login')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
def manage_appointments(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    context = {'appointments': appointments}
    return render(request, 'salon/manage_appointments.html', context)

# Accept Appointment View
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'Accepted'  # Assuming 'Accepted' is one of your status choices
        appointment.save()
        messages.success(request, f"Appointment with {appointment.name} has been accepted.")
    return redirect('manage_appointments')

# Delete Appointment View
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, f"Appointment with {appointment.name} has been deleted.")
    return redirect('manage_appointments')

# def offer_list(request):
#     offers = Offer.objects.all()  # Get all offers (active and inactive)
    
#     if request.method == 'POST':
#         form = OfferForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('offer_list')  # Redirect to the offer list page after saving
#     else:
#         form = OfferForm()  # Create a new form for adding an offer

#     return render(request, 'salon/offer_list.html', {'offers': offers, 'form': form})

def offer_list(request):
    if request.method == "POST":
        discount_percentage = request.POST.get('discount_percentage')  # Fetch the discount percentage
        
        # Ensure the discount_percentage is not empty
        if discount_percentage:
            try:
                new_offer = Offer(
                    title=request.POST.get('title'),
                    description=request.POST.get('description'),
                    discount_percentage=discount_percentage,  # Use the fetched value
                    active=True  # Set default active state if necessary
                )
                new_offer.save()
                return redirect('offer_list')  # Adjust as needed
            except Exception as e:
                # Handle the exception and inform the user
                print(f"Error creating offer: {e}")
                # Optionally, add a message to inform the user
        else:
            # Handle the case where discount_percentage is not provided
            print("Discount percentage is required.")
    
    offers = Offer.objects.all()
    return render(request, 'salon/offer_list.html', {'offers': offers})


def get_dashboard_counts(request):
    # Replace these queries with your actual database queries
    appointment_count = Appointment.objects.count()
    user_count = User.objects.count()
    offer_count = Offer.objects.count()
    
    # Return data as JSON
    data = {
        'appointment_count': appointment_count,
        'user_count': user_count,
        'offer_count': offer_count,
    }
    return JsonResponse(data)

def exclusive_offers_view(request):
    # Your logic here
    return render(request, 'salon/exclusive_offers.html')

def notifications_view(request):
    # Your logic here
    return render(request, 'salon/notifications.html')