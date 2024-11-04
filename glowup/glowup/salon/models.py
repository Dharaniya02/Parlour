from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Appointment Model
class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('Facial Treatment', 'Facial Treatment'),
        ('Haircut', 'Haircut'),
        ('Massage', 'Massage'),
        ('Nails', 'Nails'),
        ('Makeup', 'Makeup'),
        ('Waxing', 'Waxing'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    ]

    # Links Appointment to User and provides a related name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    name = models.CharField(max_length=100)  # Optional name field
    email = models.EmailField()  # Optional email field
    phone = models.CharField(max_length=15)  # Optional phone field
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.service} appointment for {self.name} on {self.date} at {self.time}"

# Profile Model linked to User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Field for avatar upload

    def __str__(self):
        return f'{self.user.username} Profile'

# Offer Model with additional validity period and validation
# class Offer(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
#     active = models.BooleanField(default=True)  # Indicates if the offer is active

#     def __str__(self):
#         return self.title

#     def is_active(self):
#         """Returns True if the offer is active based on the active flag."""
#         return self.active

# class Offer(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return self.title

class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)  # Ensure this field is defined

    def __str__(self):
        return self.title


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Create profile if user is new
    instance.profile.save()