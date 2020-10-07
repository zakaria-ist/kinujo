from .models import Profile, Authority
import datetime
from django import forms
from django.forms import ModelChoiceField
from images.models import Image

class CodeNameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            return obj.name + " (" + str(obj.code) + ") "
        except AttributeError:
            return obj.name

class NameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            return obj.name
        except AttributeError:
            return obj.name



class ProfileForm(forms.ModelForm):
    tel = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone number'}))
    password = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    nickname = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nickname'}))
    user_code = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'user_code'}))
    real_name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    corporate_name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corporate name'}))
    address1 = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address1'}))
    address2 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address2'}))
    word = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'One word'}))
    authority = NameChoiceField(queryset=None, empty_label=None, required=True,
                                   widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))
    class Meta:
        model = Profile
        fields = ('tel', 'password', 'nickname', 'user_code', 'real_name', 'corporate_name', 'address1', 'address2', 'word', 'authority')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['authority'].queryset = Authority.objects.filter(is_hidden=False, is_enable=True)


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image') 