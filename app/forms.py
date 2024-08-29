from django import forms
from .models import Melody, Image, Tab, URL, Type

class MelodyForm(forms.ModelForm):
    class Meta:
        model = Melody
        fields = ('name', 'type','comment', 'date')

    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        to_field_name='type',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
        )

class TabForm(forms.ModelForm):
    class Meta:
        model = Tab
        fields = ('tab',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('order_num', 'path', 'image_comment')

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('url',)