from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Snap_item, Snap_type, Stamp, Stamp_type

id_c_stamp = 3
id_r_stamp = 4

NEW_CHOICE = (('new', 'Новая'),
            ('repeat', 'По оттиску'))

class C_stamp_Form(ModelForm):
    prefix = 'form'


    class Meta:
        model = Stamp
        fields = ['count','snap','new_or_no','express']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snap'] = forms.ModelChoiceField(
                                queryset=Snap_item.objects.filter(type_stamp=id_c_stamp),
                                empty_label=None,
                                initial=Snap_item.objects.get(type_stamp=id_c_stamp,
                                                              snap_type=Snap_type.objects.get(snap_type='norm'))
                                ) 
                                
        self.fields['express'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
        self.fields['new_or_no'] = forms.ChoiceField(choices=NEW_CHOICE, required=False, initial='new', widget=forms.RadioSelect())
        


class R_stamp_Form(ModelForm):
    prefix = 'form'
    
    class Meta:
        model = Stamp
        fields = ['count','snap','new_or_no','express']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snap'] = forms.ModelChoiceField(
                                queryset=Snap_item.objects.filter(type_stamp=id_r_stamp),
                                empty_label=None,
                                initial=Snap_item.objects.get(type_stamp=id_r_stamp,
                                                              snap_type=Snap_type.objects.get(snap_type='norm'))
                                ) 
        
        self.fields['express'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
        self.fields['new_or_no'] = forms.ChoiceField(choices=NEW_CHOICE, required=False, initial='new', widget=forms.RadioSelect())



        

class Confirm_form(forms.Form):
    prefix = 'confirm_form'
    
    id_stamp_obj = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=20)
    # comment = forms.CharField(required=False, widget=forms.Textarea(attrs = {'cols': '50', 'rows': '4'}))
    
    comment = forms.CharField(required=False)
    file = forms.FileField(required=False)
    # delivery = forms.CharField(max_length=100, required=False)

