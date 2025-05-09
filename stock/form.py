from django import forms
from .models import Entree, EntreeItems, SortieStock, SortieItems


class EntreeForm(forms.ModelForm):
    class Meta:
        model = Entree
        fields = '__all__'
        
class EntreeItemsForm(forms.ModelForm):
    class Meta:
        model = EntreeItems
        fields = ['qty']
        
        
class SortieForm(forms.ModelForm):
    class Meta:
        model = SortieStock
        fields = '__all__'
        
class SortieItemsForm(forms.ModelForm):
    class Meta:
        model = SortieItems
        fields = ['qty', 'motif']