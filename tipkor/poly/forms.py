from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .constants import BOOKLETS, FORMAT, PAPER_CHOICE, PRESSRUN_OFFSET
from .models import Formats, Poly


class Card_Form(ModelForm):
    FORMAT = 'Визитка' # По русски!

    class Meta:
        model = Poly
        fields = ['format_p', 'paper', 'pressrun', 'duplex' ]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['format_p'] = forms.ModelChoiceField(
                                queryset=Formats.objects.filter(format_p=self.FORMAT),
                                empty_label=None
                                ) 
        self.fields['paper'] = forms.ChoiceField(initial='300', choices=[("300", "300 г/м")])
        self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)


class Leaflet_Form(ModelForm):
    FORMAT = 'А6' # По русски!

    class Meta:
        model = Poly
        fields = ['format_p', 'paper', 'pressrun', 'duplex' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['format_p'] = forms.ChoiceField(choices=FORMAT)
        self.fields['format_p'] = forms.ModelChoiceField(
                        queryset=Formats.objects.all(),
                        empty_label=None, initial=Formats.objects.get(format_p=self.FORMAT),
                        ) 
        
        self.fields['paper'] = forms.ChoiceField(initial='130', choices=PAPER_CHOICE)
        self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)
        
class Booklet_Form(ModelForm):
    FORMAT = 'А4' # По русски!
    
    class Meta:
        model = Poly
        fields = ['format_p', 'paper', 'pressrun', 'duplex', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['format_p'] = forms.ModelChoiceField(
                        queryset=Formats.objects.filter(format_p=self.FORMAT),
                        empty_label=None
                        ) 
        
        self.fields['paper'] = forms.ChoiceField(initial='130', choices=PAPER_CHOICE)
        self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)
        self.fields['post_obr'] = forms.ChoiceField(initial='eurobucket', choices=BOOKLETS)
        

class Confirm_form(forms.Form):
    
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=20)
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs = {'cols': '50', 'rows': '4'}))
    file = forms.FileField(required=False)
    

