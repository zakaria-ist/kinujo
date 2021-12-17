from .models import Profile, Authority
import datetime
from django.utils import translation
from django import forms
from django.forms import ModelChoiceField
from images.models import Image
from utilities.constants import SALON_CATEGORY, GENDER_TYPE, YES_NO, SALON_CATEGORY_JA, GENDER_TYPE_JA, YES_NO_JA

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
                            widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off", 
                                    'placeholder': '', 'maxlength': '15'}))
    # password = forms.CharField(required=False,
    #                         widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'new-password'}))
    nickname = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    real_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    user_code = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id':'id_user_code', 'autocomplete':'newCode'}))
    representative_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    corporate_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    corporate_tel = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    address1 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    address2 = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    shop_name = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    word = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ひとこと'}))
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

    class Meta:
        model = Profile
        fields = ('tel', 'nickname', 'real_name', 'corporate_name', 'address1', 'address2', 'word', 'authority',
                    'representative_name', 'corporate_tel', 'salon_category', 'zipcode', 'gender', 'shop_name', 'user_code')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['authority'].queryset = Authority.objects.filter(is_hidden=False, is_enable=True)
        language = translation.get_language()
        if language == 'ja':
            self.fields['salon_category'].choices = SALON_CATEGORY_JA
            self.fields['is_seller'].choices = YES_NO_JA
            self.fields['is_approved'].choices = YES_NO_JA
            self.fields['gender'].choices = GENDER_TYPE_JA


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image') 