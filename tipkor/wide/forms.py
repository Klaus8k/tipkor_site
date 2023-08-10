from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from loguru import logger

from .constants import POST_OBR
from .models import Material, Post_obr, Wide, wide_validator


class Banner_Form(ModelForm):
    MATERIAL = 'banner'

    class Meta:
        model = Wide
        fields = ['wide_size', 'heigth_size']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material_print'] = forms.ModelChoiceField(
                                queryset=Material.objects.filter(type_material=self.MATERIAL),
                                empty_label=None
                                ) 
        self.fields['post_obr'] = forms.ModelChoiceField(
                                queryset=Post_obr.objects.filter(type_wide_production='banner'),
                                empty_label=None
                                )
        



# Сделать форму с выбором форматов, дуплекс, тираж. Форматы из модели должны браться
class Sticker_Form(ModelForm):
    MATERIAL = 'sticker'
    
    class Meta:
        model = Wide
        fields = ['wide_size', 'heigth_size']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material_print'] = forms.ModelChoiceField(
                                queryset=Material.objects.filter(type_material=self.MATERIAL),
                                empty_label=None
                                ) 

        self.fields['post_obr'] = forms.ModelChoiceField(
                                queryset=Post_obr.objects.filter(type_wide_production='sticker'),
                                empty_label=None
                                )
        
        
        
        
class Table_Form(ModelForm):
    MATERIAL = 'table'
    
    class Meta:
        model = Wide
        fields = ['wide_size', 'heigth_size']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material_print'] = forms.ModelChoiceField(
                                queryset=Material.objects.filter(type_material=self.MATERIAL),
                                empty_label=None
                                ) 

        self.fields['post_obr'] = forms.ModelChoiceField(
                                queryset=Post_obr.objects.filter(type_wide_production='table'),
                                empty_label=None
                                )
        

class Confirm_form(forms.Form):
    type_production = forms.CharField(max_length=20, widget=forms.HiddenInput())
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=20)
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs = {'cols': '50', 'rows': '4'}))
    file = forms.FileField(required=False)

