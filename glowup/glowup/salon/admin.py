from django.contrib import admin
from .models import Appointment, Profile, Offer
from django.utils.html import format_html
from django.urls import reverse

# Custom admin class for the Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'date', 'time', 'status']
    list_filter = ['service', 'date', 'status']
    search_fields = ['name', 'email', 'phone']

# Custom admin class for the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')

# Register Profile model with custom admin class
admin.site.register(Profile, ProfileAdmin)

# Custom admin class for the Offer model
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'discount_percentage', 'edit_action', 'delete_action')
    list_filter = []  # Temporarily empty to avoid errors
    search_fields = ('title',)

    # Custom action for editing an offer
    def edit_action(self, obj):
        url = reverse('admin:salon_offer_change', args=[obj.pk])  # Use reverse for dynamic URL generation
        return format_html(f'<a href="{url}">Edit</a>')
    edit_action.short_description = 'Edit'
    
    # Custom action for deleting an offer
    def delete_action(self, obj):
        url = reverse('admin:salon_offer_delete', args=[obj.pk])  # Use reverse for dynamic URL generation
        return format_html(f'<a href="{url}">Delete</a>')
    delete_action.short_description = 'Delete'

    # Enable actions to activate/deactivate selected offers
    actions = ['activate_offers', 'deactivate_offers']

    def activate_offers(self, request, queryset):
        """Activate selected offers."""
        queryset.update(active=True)
        self.message_user(request, "Selected offers have been activated.")

    def deactivate_offers(self, request, queryset):
        """Deactivate selected offers."""
        queryset.update(active=False)
        self.message_user(request, "Selected offers have been deactivated.")

    activate_offers.short_description = "Activate selected offers"
    deactivate_offers.short_description = "Deactivate selected offers"
