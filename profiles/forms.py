from .models import Profile, Authority
import datetime
from django import forms
from django.forms import ModelChoiceField
from images.models import Image
from utilities.constants import SALON_CATEGORY, GENDER_TYPE, YES_NO

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
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone number', 'maxlength': '15'}))
    password = forms.CharField(required=False,
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nickname'}))
    real_name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    representative_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'representative name'}))
    corporate_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corporate name'}))
    corporate_tel = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'corporate phone'}))
    address1 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address1'}))
    address2 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address2'}))
    word = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'One word'}))
    authority = NameChoiceField(queryset=None, empty_label=None, required=True,
                                   widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}))
    salon_category = forms.ChoiceField(required=False, choices=SALON_CATEGORY,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(required=False, choices=GENDER_TYPE,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    is_seller = forms.ChoiceField(required=False, choices=YES_NO,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    is_approved = forms.ChoiceField(required=False, choices=YES_NO,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '7'}))
    birthday = forms.DateField(required=False,
                                      widget=forms.DateInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ('tel', 'password', 'nickname', 'real_name', 'corporate_name', 'address1', 'address2', 'word', 'authority',
                    'representative_name', 'corporate_tel', 'salon_category', 'zipcode', 'birthday', 'gender')

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