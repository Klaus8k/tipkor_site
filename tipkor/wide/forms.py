from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm



from .constants import POST_OBR
from .models import Material, Wide, Post_obr


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
    # FORMAT = 'A4' # Выбор только форматов с именем 'Визитка'
    pass
    # class Meta:
    #     model = Wide
    # #     fields = ['format_p', 'paper', 'pressrun', 'duplex', ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.fields['format_p'] = forms.ChoiceField(choices=FORMAT)
    #     self.fields['format_p'] = forms.ModelChoiceField(
    #                     queryset=Formats.objects.filter(format_p=self.FORMAT),
    #                     empty_label=None
    #                     ) 
        
    #     self.fields['paper'] = forms.ChoiceField(initial='130', choices=PAPER_CHOICE)
    #     self.fields['pressrun'] = forms.ChoiceField(initial=1000, choices=PRESSRUN_OFFSET)
    #     self.fields['post_obr'] = forms.ChoiceField(initial='eurobucket', choices=BOOKLETS)
        

class Confirm_form(forms.Form):
    name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    tel = forms.CharField(max_length=15)
    file = forms.FileField(required=False)

