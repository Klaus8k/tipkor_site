from django import forms
from django.forms import ModelForm

from .constants import PAPER_CHOICE
from .models import Poly, Formats

# DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать"),]


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


# Сделать форму с выбором форматов, дуплекс, тираж. Форматы из модели должны браться
# class Leaflet_Form(ModelForm):
#     FORMAT = 'Визитка' # Выбор только форматов с именем 'Визитка'

#     class Meta:
#         model = Leaflets_Model
#         fields = ['format', 'paper', 'pressrun', 'duplex' ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['format'] = forms.ModelChoiceField(
#                                 queryset=Formats_Model.objects.exclude(format_paper=self.FORMAT),
#                                 empty_label=None
#                                 ) 

# class Confirm_form(forms.Form):
    
#     name = forms.CharField(max_length=20, required=False)
#     email = forms.EmailField()
