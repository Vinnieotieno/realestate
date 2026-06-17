from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from .models import Contact
import logging

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id', '')
        listing = request.POST.get('listing', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        realtor_email = request.POST.get('realtor_email', '')

        # Convert listing_id to int if possible, else set to 0
        try:
            listing_id_int = int(listing_id) if listing_id else 0
        except ValueError:
            listing_id_int = 0

        # Check if user has made inquiry already (only for property inquiries)
        if listing_id_int and request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(listing_id=listing_id_int, user=request.user)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+str(listing_id_int))

        # Save contact to database first
        contact = Contact(
            listing=listing,
            listing_id=listing_id_int,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user=request.user if request.user.is_authenticated else None
        )
        contact.save()

        # Try to send email
        try:
            subject = 'Property Listing Inquiry' if listing_id_int else 'New Contact Inquiry'
            email_message = (
                f'There has been an inquiry for {listing or "General Contact"}.'
                f'\n\nMessage: {message}\nFrom: {name} ({email}, {phone})'
            )
            send_mail(
                subject,
                email_message,
                'vincentotienoakuku@gmail.com',
                [realtor_email or 'vincentotienoakuku@gmail.com'],
                fail_silently=True,  # Don't raise exceptions
            )
            logger.info(f"Email sent successfully for contact inquiry from {name}")
        except (BadHeaderError, Exception) as e:
            # Log the error but don't break the user experience
            logger.error(f"Failed to send email for contact inquiry: {str(e)}")
            # Continue with success message since contact was saved

        # Success message
        if listing_id_int:
            messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
            return redirect('/listings/'+str(listing_id_int))
        else:
            messages.success(request, 'Thank you for contacting us! We have received your message and will get back to you soon.')
            return redirect('/contacts/contact')
    
    # For GET requests, render the contact page
    return render(request, 'contacts/contact.html')

