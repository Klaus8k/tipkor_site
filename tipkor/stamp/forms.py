from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Snap_item, Snap_type, Stamp, Stamp_type


class C_stamp_Form(ModelForm):
    prefix = 'form'

    class Meta:
        model = Stamp
        fields = ['express', 'count', 'new_or_no']
        widgets = {'new_or_no': forms.RadioSelect()}

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snap'] = forms.ModelChoiceField(
                                queryset=Snap_item.objects.filter(type_stamp=Stamp_type.objects.get(type_stamp='c_stamp')),
                                empty_label=None, initial=Snap_item.objects.get(snap_type=Snap_type.objects.get(snap_type='norm'))) 

class R_stamp_Form(ModelForm):

    class Meta:
        model = Stamp
        fields = ['express', 'count' ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snap'] = forms.ModelChoiceField(
                                queryset=Snap_item.objects.filter(type_stamp=Stamp_type.objects.get(type_stamp='r_stamp')),
                                empty_label=None, initial=Snap_item.objects.get(snap_type=Snap_type.objects.get(snap_type='norm')))



        

class Confirm_form(forms.Form):
    prefix = 'confirm_form'
    
    id_stamp_obj = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    tel = forms.CharField(max_length=15)
    comment = forms.CharField(widget=forms.Textarea(attrs = {'cols': '30', 'rows': '3'}))
    file = forms.FileField(required=False)
    # delivery = forms.CharField(max_length=100, required=False)

