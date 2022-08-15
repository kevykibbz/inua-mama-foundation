from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.hashers import check_password
from django.core.validators import FileExtensionValidator,URLValidator
from installation.models import SiteConstants
from django.contrib.auth import authenticate

class UserResetPassword(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email address'}),error_messages={'required':'Email address is required'})

    def clean_email(self):
        email=self.cleaned_data['email']
        if  not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address does not exist')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Invalid email address')
        return email


class UsersContactForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Full name','aria-label':'name'}),error_messages={'required':'Full name is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone'},initial="IN"),error_messages={'required':'Phone number is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Email address','aria-label':'email'}),error_messages={'required':'Email address is required'})
    subject=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'subject ','aria-label':'subject'}),error_messages={'required':'Subject is required'})
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':5,'aria-required':'true','class':'form-control','placeholder':'Message','aria-label':'message'}),error_messages={'required':'Message is required','min_length':'enter atleast 6 characters long'})

    class Meta:
        model=ContactModel
        fields=['name','phone','email','subject','message',]


    def clean_name(self):
        name=self.cleaned_data['name']
        if len(name.split(" ")) > 1:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
            elif not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed')
        return name

           

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('invalid email address')
        return email

opt1=[
            ("Sole proprietor","Sole proprietor"),
            ("Partnership","Partnership"),
            ("Corporation","Corporation"),
        ]
opt2=[
            ("Yes","Yes"),
            ("No","No"),
        ]
class ApplicationForm(forms.ModelForm):
    applicant_fname=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'applicant_fname','class':'form-control','placeholder':'Applicant first name'}),error_messages={'required':'First name is required'})
    applicant_mname=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'applicant_mname','class':'form-control','placeholder':'Applicant middle name'}),error_messages={'required':'Middle is required'})
    applicant_lname=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'applicant_lname','class':'form-control','placeholder':'Applicant last name'}),error_messages={'required':'Last name is required'})
    prefix=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'prefix','class':'form-control','placeholder':'Prefix'}),error_messages={'required':'Prefix is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-label':'email','class':'form-control','placeholder':'myname@example.com'}),error_messages={'required':'Email is required'})
    mobile_phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Mobile phone number'},initial="Ke"),error_messages={'required':'Mobile phone number is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-required':'true','class':'form-control','type':'tel','aria-label':'phone','placeholder':'Phone number'},initial="Ke"),error_messages={'required':'Phone number is required'})
    fax=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'fax','class':'form-control','placeholder':'Fax'}),required=False)
    address1=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'address1','class':'form-control','placeholder':'Street address'}),error_messages={'required':'Street address is required'})
    address2=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'address2','class':'form-control','placeholder':'Street address line 2'}),required=False)
    city=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'city','class':'form-control','placeholder':'City'}),required=False)
    state=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'state','class':'form-control','placeholder':'State'}),required=False)
    zip_code=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'zip_code','class':'form-control','placeholder':'zip code'}),required=False)
    dob=forms.DateField(widget=forms.DateInput(attrs={'pattern':'[0-9]{2}-[0-9]{2}-[0-9]{4}','type':'Date','class':'form-control','placeholder':'date of birth'}),error_messages={'required':'DOB is required'})
    biz_location1=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'biz_location1','class':'form-control','placeholder':'Businness Street address'}),error_messages={'required':'Businness Street address is required'})
    biz_location2=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'biz_location2','class':'form-control','placeholder':'Businness Street address line 2'}),required=False)
    biz_city=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'biz_city','class':'form-control','placeholder':'Businness City'}),required=False)
    biz_state=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'biz_state','class':'form-control','placeholder':'Businness State'}),required=False)
    biz_zip_code=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'biz_zip_code','class':'form-control','placeholder':'zip code'}),required=False)
    apply_as=forms.ChoiceField(choices=opt1,widget=forms.RadioSelect(attrs={'aria-label':'apply_as','class':'form-check-input','type':'radio'}),error_messages={'required':'Applying as category is required'})
    marketing_material=forms.FileField(widget=forms.FileInput(attrs={'aria-label':'marketing_material','class':'custom-file-input','id':'customFileInput1'}),required=False)
    marketing_information=forms.FileField(widget=forms.FileInput(attrs={'aria-label':'marketing_information','class':'custom-file-input','id':'customFileInput2'}),required=False)
    statement=forms.ChoiceField(choices=opt2,widget=forms.RadioSelect(attrs={'aria-label':'statement','class':'form-check-input','type':'radio'}),error_messages={'required':'This field is required'})
    statement_information=forms.FileField(widget=forms.FileInput(attrs={'aria-label':'statement_information','class':'custom-file-input','id':'customFileInput3'}),required=False)
    been_financed=forms.ChoiceField(choices=opt2,widget=forms.RadioSelect(attrs={'aria-label':'been_financed','class':'form-check-input','type':'radio'}),error_messages={'required':'This field  is required'})
    lender_name=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'lender_name','class':'form-control','placeholder':'Lender name'}),required=False)
    finance_was_for=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'finance_was_for','class':'form-control','placeholder':'Finnace was for'}),required=False)
    loan_reason=forms.CharField(widget=forms.Textarea(attrs={'cols':20,'rows':5,'aria-label':'loan_reason','class':'form-control','placeholder':'Loan reason'}),required=False)
    project_gross_value=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'project_gross_value','class':'form-control','placeholder':'Project gross value'}),required=False)
    loan_amount=forms.CharField(widget=forms.NumberInput(attrs={'aria-label':'loan_amount','class':'form-control','placeholder':'Loan amount'}),error_messages={'required':'Loan amount  is required'})
    agree=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'agree','class':'form-check-input','type':'checkbox','id':'exampleRadio1'}),error_messages={'required':'This field is required'})
    class Meta:
        model=ApplicationModel
        fields=[
                'applicant_fname',
                'applicant_mname',
                'applicant_lname',
                'mobile_phone','phone','fax',
                'prefix',
                'email',
                'address1','address2',
                'city',
                'state',
                'zip_code',
                'dob',
                'biz_location1',
                'biz_location2',
                'biz_city',
                'biz_state',
                'biz_zip_code','apply_as','marketing_material','marketing_information','statement','been_financed','statement_information','lender_name','finance_was_for','loan_reason','project_gross_value','loan_amount',
            ]