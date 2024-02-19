from django import forms
from .models import Location, Profile, Report
from django.contrib.auth.models import User
from .widgets import CustomImageFieldWidget

class UserForm(forms.ModelForm):

    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        username_field = self.fields.pop('username')
        firstname_field = self.fields.pop('first_name')
        self.fields = {'username': username_field, 'first_name': firstname_field, **self.fields}

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomImageFieldWidget)
    #photo = forms.ImageField()
    class Meta:
        model = Profile
        fields = {'photo', 'bio', 'phone_number'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        photo = self.fields.pop('photo')
        bio_field = self.fields.pop('bio')
        
        self.fields = {'photo': photo, 'bio': bio_field, **self.fields}


class LocationForm(forms.ModelForm):
    city_manual = forms.CharField(max_length=24, required=False,)
    address_1 = forms.CharField(required=True)
    zip_code = forms.CharField(required=True)

    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'city_manual', 'state', 'zip_code'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        address_1 = self.fields.pop('address_1')
        address_2 = self.fields.pop('address_2')
        city = self.fields.pop('city')
        city_manual = self.fields.pop('city_manual')
        state = self.fields.pop('state')
        
        self.fields = {'address_1': address_1, 'address_2': address_2, 'city': city, 'city_manual': city_manual,
                       'state': state, **self.fields}

        if self.data.get('city') == 'other':
            self.fields['city_manual'].widget.attrs['style'] = 'display:block;'   
        else:
            self.fields['city_manual'].widget.attrs['style'] = 'display:none;'


class ReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = ['reason']

    
    