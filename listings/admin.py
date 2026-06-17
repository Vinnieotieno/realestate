from django.contrib import admin
from .models import Listing, Booking
from .forms import ListingAdminForm

class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm
    list_display = ('id', 'title', 'property_type', 'is_published', 'price', 'list_date', 'realtor', 'city', 'state')
    list_display_links = ('id', 'title')
    list_filter = ('property_type', 'realtor', 'city', 'state', 'is_published', 'bedrooms', 'bathrooms')
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
    list_per_page = 25
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'property_type', 'description', 'realtor', 'is_published', 'list_date')
        }),
        ('Location Details', {
            'fields': ('address', 'city', 'state', 'zipcode', 'latitude', 'longitude'),
            'description': 'Enter the property location details. Coordinates are optional but help with map display.'
        }),
        ('Property Details', {
            'fields': ('price', 'bedrooms', 'bathrooms', 'garage', 'sqft', 'lot_size'),
            'description': 'Enter the property specifications and pricing information.'
        }),
        ('Photos', {
            'fields': ('photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'),
            'classes': ('collapse',),
            'description': 'Upload property photos. The main photo is required and will be the primary display image.'
        }),
        ('Amenities & Features', {
            'fields': ('amenities',),
            'classes': ('collapse',),
            'description': 'List nearby amenities and features. Enter each amenity on a new line.'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/amenities-admin.css',)
        }
        js = ('admin/js/amenities-admin.js',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('listing', 'get_booking_type', 'client', 'client_email', 'get_booking_period', 'status', 'created_at')
    list_filter = ('booking_type', 'status', 'created_at')
    search_fields = ('listing__title', 'client__username', 'client_email', 'client_phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'get_booking_details')

    fieldsets = (
        ('Booking Information', {
            'fields': ('listing', 'booking_type', 'client', 'client_email', 'client_phone', 'status', 'created_at')
        }),
        ('Viewing Details', {
            'fields': ('date', 'time'),
            'classes': ('collapse',),
        }),
        ('Airbnb Details', {
            'fields': ('check_in_date', 'check_out_date', 'check_in_time', 'check_out_time'),
            'classes': ('collapse',),
        }),
    )

    def get_booking_type(self, obj):
        """Display booking type with icon"""
        if obj.booking_type == 'airbnb':
            return '🏨 Airbnb Booking'
        return '👁️ Property Viewing'
    get_booking_type.short_description = 'Booking Type'

    def get_booking_period(self, obj):
        """Display booking period based on type"""
        if obj.booking_type == 'airbnb':
            return f"{obj.check_in_date} to {obj.check_out_date}"
        return f"{obj.date} at {obj.time}"
    get_booking_period.short_description = 'Period'

    def get_booking_details(self, obj):
        """Display detailed booking information"""
        if obj.booking_type == 'airbnb':
            return f"Check-in: {obj.check_in_date} at {obj.check_in_time}\nCheck-out: {obj.check_out_date} at {obj.check_out_time}"
        return f"Date: {obj.date}\nTime: {obj.time}"
    get_booking_details.short_description = 'Booking Details'

admin.site.register(Listing, ListingAdmin)
admin.site.register(Booking, BookingAdmin)
