from django import forms
from django.forms import ModelForm

from .models import Card_Model, Formats_Poly_Model, Leaflets_Model

DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать"),]


class Card_Form(ModelForm):
    PAPER_CHOICE = [("300", "300 г/м"),]
    FORMAT = [('90x50', '90x50мм'),]

    class Meta:
        model = Card_Model
        fields = ['format', 'paper', 'pressrun', 'duplex' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['format'] = forms.ModelChoiceField(
                                queryset=Formats_Poly_Model.objects.filter(format_paper='Vizitka'),
                                empty_label=None
                                ) 
        self.fields['paper'] = forms.ChoiceField(initial='300', choices=self.PAPER_CHOICE)
    

    # card_format = forms.ChoiceField(initial='90x50', choices=CARD_FORMAT)
    # duplex = forms.ChoiceField(initial=True, choices=DUPLEX)
    # paper = forms.ChoiceField(initial='300', choices=PAPER_CHOICE)
    # pressrun = forms.IntegerField(help_text="Тираж")


# Сделать форму с выбором форматов, дуплекс, тираж. Форматы из модели должны браться
class Leaflet_Form(forms.Form):
    PAPER_CHOICE = Leaflets_Model.PAPER_CHOICE
    
    format = forms.ModelChoiceField(
                                queryset=Formats_Poly_Model.objects.all(),
                                empty_label=None
                                )                
    duplex = forms.ChoiceField(initial=True, choices=DUPLEX)
    paper = forms.ChoiceField(initial='300', choices=PAPER_CHOICE)
    pressrun = forms.IntegerField(help_text="Тираж")
