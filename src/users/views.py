from django.shortcuts import redirect,render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import UserForm,LocationForm,ProfileForm,ReportForm
from main.models import Listing, LikedListing
from .models import Report
from django.contrib.auth.models import User
import shutil


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, f'An error occured trying to login')
        else:
            messages.error(request, f'An error occured trying to login')
    elif request.method == "GET":
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'login_form': login_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')

class RegisterView(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html', {'register_form': register_form})
    
    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f'User {user.username} registered successfully. Please login to continue..')
            return redirect('login')
        else:
            messages.error(request, f'An error occured trying to register') 
            return render(request, 'views/register.html', {'register_form': register_form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).all()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form,
                                                      'user_listings': user_listings,
                                                      'user_liked_listings': user_liked_listings,
                                                    })

    def post(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).all()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(
            request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error Updating Profile!')
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form,
                                                      'user_listings': user_listings,
                                                      'user_liked_listings': user_liked_listings,
                                                    })



@login_required
def delete_user_view(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        # Get the user's media folder path
        media_folder_path = f'media/user_{user.id}'

        # Delete user and associated listings
        user.delete()
        #Listing.objects.filter(seller=request.user.profile).delete()

        # Delete the user's media folder and its contents
        try:
            shutil.rmtree(media_folder_path)
        except FileNotFoundError:
            pass  # Ignore if the folder doesn't exist

        messages.success(request, "User and associated listings deleted successfully.")
        return redirect('main')

    return render(request, 'views/profile.html', {'user': user})

@login_required
def delete_user_confirmation_view(request, id):
    user = User.objects.get(id=id)
    return render(request, 'views/delete_user_confirmation.html', {'user': user})



@login_required
def report_user(request,reported_user_id):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_user = get_object_or_404(User, id=reported_user_id)  # Assign the reported_user_id from request.POST
            report.reporting_user = request.user
            report.save()
            messages.success(request, "Reported successfully")
            return redirect('home')
    else:
        form = ReportForm()

    return render(request, 'views/report_issue.html', {'form': form,
                                                       'reported_user_id':reported_user_id,
                                                       })



