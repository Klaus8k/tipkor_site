from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Snap_item, Snap_type, Stamp, Stamp_type


class C_stamp_Form(ModelForm):
    # FORMAT = 'Визитка' # По русски!

    class Meta:
        model = Stamp
        fields = ['express', 'comment', 'count' ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snap'] = forms.ModelChoiceField(
                                queryset=Snap_item.objects.filter(type_stamp=Stamp_type.objects.get(type_stamp='c_stamp')),
                                empty_label=None, initial=Snap_item.objects.get(snap_type=Snap_type.objects.get(snap_type='norm'))
                                ) 

    



        

class Confirm_form(forms.Form):
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    tel = forms.CharField(max_length=15)
    file = forms.FileField(required=False)

