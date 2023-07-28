from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Stamp


class C_stamp_Form(ModelForm):
    # FORMAT = 'Визитка' # По русски!

    class Meta:
        model = Stamp
        fields = ['express', 'file', 'comment', 'snap', 'count' ]
        

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['format_p'] = forms.ModelChoiceField(
    #                             queryset=Formats.objects.filter(format_p=self.FORMAT),
    #                             empty_label=None
    #                             ) 
    #     self.fields['paper'] = forms.ChoiceField(initial='300', choices=[("300", "300 г/м")])
    #     self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)


        

class Confirm_form(forms.Form):
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    tel = forms.CharField(max_length=15)
    file = forms.FileField(required=False)

