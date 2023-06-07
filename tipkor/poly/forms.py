from django import forms

from .models import Leaflets_Model, Formats_Poly_Model

DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать"),]


class Card_Form(forms.Form):
    PAPER_CHOICE = [("300", "300 г/м"),]
    CARD_FORMAT = [('90x50', '90x50мм'),]
    
    card_format = forms.ChoiceField(initial='90x50', choices=CARD_FORMAT)
    duplex = forms.ChoiceField(initial=True, choices=DUPLEX)
    paper = forms.ChoiceField(initial='300', choices=PAPER_CHOICE)
    pressrun = forms.IntegerField(help_text="Тираж")




# Сделать форму с выбором форматов, дуплекс, тираж. Форматы из модели должны браться
class Leaflet_Form(forms.Form):
    # https://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform





# class Leaflet_Form(forms.ModelForm):
    # class Meta:
        # model = Leaflets_Model
        # fields = ['paper', 'format_choice', 'duplex', 'pressrun']
