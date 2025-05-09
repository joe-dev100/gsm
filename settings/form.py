from django import forms

from .models import Setting 

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = "__all__"
        

class EmailSettingForm(forms.ModelForm):
    notified = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}),required=False, label="notified")
    class Meta:
        model = Setting
        fields = ['notified']