from importlib import reload
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Listing, LikedListing
from django.contrib import messages
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter
from django.core.mail import send_mail



def main_view(request):
    return render(request, 'views/main.html', {"name":"TradeHub"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing')
    liked_listing_ids = [i[0] for i in user_liked_listings]
    context = {
        'listing_filter': listing_filter,
        'liked_listing_ids': liked_listing_ids,
    }
    return render(request, "views/home.html", context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()

                
                messages.info(
                    request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html', {'listing_form': listing_form, 'location_form': location_form, })


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        
        context = {
        'listing': listing,
        'listing_user_id': listing.seller.user.id  # Pass the user ID associated with the listing
        }
        return render(request, 'views/listing.html', context)

    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing...')
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()


                messages.info(
                    request, f'Listing {id} updated Successfully!')
                return redirect('home')
            else:
                messages.error(request, f'An error occured while edit the listing...')
                return reload()
    
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        context = {
            'listing_form': listing_form,
            'location_form': location_form,
        }
        return render(request, 'views/edit.html', context)
            
    except Exception as e:
        messages.error(request, f'An error occured while trying to access the edit page...')
        return redirect('home')
    

@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    #print(request.user)
    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if created:
        liked_listing.save()
        
    else:
        liked_listing.delete()

    return JsonResponse({
        'is_liked_by_user': created,
    })
    

'''def send_mail(request):
    gmail_url = "https://mail.google.com/"
    return redirect(gmail_url)'''

@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.username} is interested in {listing.model}'
        emailMessage = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on TradeHub'
        send_mail(emailSubject, emailMessage, 'noreply@tradehub.com',
                  [listing.seller.user.email, ], fail_silently=True)
        return JsonResponse({
            "success": True,
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "info": e,
        })
    

@login_required
def delete_listing_view(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect('home')
    return render(request, 'views/listing.html')

@login_required
def delete_listing_confirmation_view(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, 'views/listing_delete_confirmation.html', {'listing': listing})