from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .constants import FORMAT, PAPER_CHOICE, PRESSRUN_OFFSET, BOOKLETS
from .models import Formats, Poly


class Card_Form(ModelForm):
    FORMAT = 'Визитка' # Выбор только форматов с именем 'Визитка'

    class Meta:
        model = Poly
        fields = ['format_p', 'paper', 'pressrun', 'duplex' ]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['format_p'] = forms.ModelChoiceField(
                                queryset=Formats.objects.filter(format_p=self.FORMAT),
                                empty_label=None
                                ) 
        self.fields['paper'] = forms.ChoiceField(initial='300', choices=PAPER_CHOICE)
        self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)


# Сделать форму с выбором форматов, дуплекс, тираж. Форматы из модели должны браться
class Leaflet_Form(ModelForm):
    FORMAT = 'A6' # Выбор только форматов с именем 'Визитка'

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
    FORMAT = 'A4' # Выбор только форматов с именем 'Визитка'

    class Meta:
        model = Poly
        fields = ['format_p', 'paper', 'pressrun', 'duplex', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['format_p'] = forms.ChoiceField(choices=FORMAT)
        self.fields['format_p'] = forms.ModelChoiceField(
                        queryset=Formats.objects.filter(format_p=self.FORMAT),
                        empty_label=None
                        ) 
        
        self.fields['paper'] = forms.ChoiceField(initial='130', choices=PAPER_CHOICE)
        self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)
        self.fields['post_obr'] = forms.ChoiceField(initial='eurobucket', choices=BOOKLETS)
        

class Confirm_form(forms.Form):
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    tel = forms.CharField(max_length=15)
    file = forms.FileField(required=False)

