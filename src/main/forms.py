from django import forms

from .models import Listing
from .widgets import CustomListImageFieldWidget

class ListingForm(forms.ModelForm):
    brand_manual = forms.CharField(max_length=24, required=False,)
    image = forms.ImageField(widget=CustomListImageFieldWidget)
    #widget=CustomListImageFieldWidget
    class Meta:
        model = Listing
        fields = {'brand', 'brand_manual', 'model', 'vin', 'mileage',
                  'color', 'description', 'engine', 'transmission', 'price', 'image'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brand = self.fields.pop('brand')
        brand_manual = self.fields.pop('brand_manual')
        model = self.fields.pop('model')
        engine = self.fields.pop('engine')
        mileage = self.fields.pop('mileage')
        vin = self.fields.pop('vin')
        color = self.fields.pop('color')
        description = self.fields.pop('description')
        price = self.fields.pop('price')
        transmission = self.fields.pop('transmission')
        self.fields = {'brand': brand, 'brand_manual': brand_manual, 'model': model, 
                       'engine': engine, 'mileage': mileage,
                       'vin': vin, 'color': color, 
                       'transmission': transmission,
                       'price': price,
                       'description': description,
                       **self.fields}

        
        
        if self.data.get('brand') == 'other':
            self.fields['brand_manual'].widget.attrs['style'] = 'display:block;'   
        else:
            self.fields['brand_manual'].widget.attrs['style'] = 'display:none;'