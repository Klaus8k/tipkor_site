from django.forms import ModelForm

from .models import Card_Model


class Card_Form(ModelForm):
    class Meta:
        model = Card_Model
        fields = ['x', 'y', 'pressrun', 'duplex']

        