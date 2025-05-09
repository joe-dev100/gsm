import datetime
from django import forms

from product.models import Product 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        fields = '__all__'
        
    def clean_expiried_on(self):
        expiried_on = self.cleaned_data.get('expiried_on')
        if expiried_on is not None:
            if expiried_on == datetime.date.today() or expiried_on < datetime.date.today() :
                raise forms.ValidationError("La date d'expiration doit être supérieure à la date actuelle.")
        return expiried_on
    
    