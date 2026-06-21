from django.shortcuts import render, redirect
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices, state_choices
from listings.models import Listing, ListingSubscription
from realtors.models import Realtor
from services.models import Service
from django.contrib import messages
from blog.models import BlogSubscription

def index(request):
    listings = Listing.objects.public().order_by('-list_date')[:3]
    featured_services = Service.objects.filter(is_featured=True, is_active=True).order_by('order')[:4]

    context = {
        'listings': listings,
        'featured_services': featured_services,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }

    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.verified().order_by('-hire_date')
    mvp_realtors = Realtor.objects.verified().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)

def footer_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscription_type = request.POST.get('type', 'both')  # both, blog, listing
        
        if email:
            blog_created = False
            listing_created = False
            blog_reactivated = False
            listing_reactivated = False
            
            if subscription_type in ['both', 'blog']:
                blog_subscription, blog_created = BlogSubscription.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                if not blog_created and not blog_subscription.is_active:
                    blog_subscription.is_active = True
                    blog_subscription.save()
                    blog_reactivated = True
            
            if subscription_type in ['both', 'listing']:
                listing_subscription, listing_created = ListingSubscription.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                if not listing_created and not listing_subscription.is_active:
                    listing_subscription.is_active = True
                    listing_subscription.save()
                    listing_reactivated = True
            
            # Provide appropriate feedback
            if blog_created or listing_created:
                messages.success(request, 'Successfully subscribed to updates!')
            elif blog_reactivated or listing_reactivated:
                messages.success(request, 'Welcome back! You are now subscribed again.')
            else:
                messages.info(request, 'You are already subscribed to our updates.')
        
        return redirect(request.META.get('HTTP_REFERER', '/'))

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'pages/terms_of_service.html')

def contact(request):
    return render(request, 'pages/contact.html')
