from django import forms

DUPLEX = [(True, "Двухсторонняя печать"), (False, "Односторонняя печать")]


class Card_Form(forms.Form):
    x = forms.IntegerField(max_value=100, disabled=True, initial=90)
    y = forms.IntegerField(max_value=100, disabled=True, initial=50)
    duplex = forms.ChoiceField(initial=True, choices=DUPLEX)
    pressrun = forms.IntegerField(help_text="Тираж")
