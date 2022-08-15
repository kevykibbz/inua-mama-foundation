from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from manager.addons import send_email
import random
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
import environ
env=environ.Env()
environ.Env.read_env()

class ExtendedAdmin(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    location=models.CharField(null=True,blank=True,max_length=100)
    main=models.BooleanField(default=False)
    is_installed=models.BooleanField(default=False)

    class Meta:
        db_table='extended_admin'
        verbose_name_plural='extended_admins'

    def __str__(self):
        return f'{self.user.username} site extended admin'


        
#generate random
def generate_id():
    return get_random_string(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')




@receiver(post_save, sender=ExtendedAdmin)
def send_installation_email(sender, instance, created, **kwargs):
    if created:
        if instance.is_installed:
            #site is installed
            subject='Congragulations:Site installed successfully.'
            email=instance.user.email
            message={
                        'user':instance.user,
                        'site_name':instance.user.siteconstants.site_name,
                        'site_url':instance.user.siteconstants.site_url
                    }
            template='emails/installation.html'
            send_email(subject,email,message,template)





def bgcolor():
    hex_digits=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    digit_array=[]
    for i in range(6):
        digits=hex_digits[random.randint(0,15)]
        digit_array.append(digits)
    joined_digits=''.join(digit_array)
    color='#'+joined_digits
    return color





user_roles=[
            ('Tertiary','View only'),
            ('Secondary','View | Edit'),
            ('Admin','View | Edit  | Admin'),
        ]





class ExtendedAuthUser(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',unique=True,max_length=13)
    initials=models.CharField(max_length=10,blank=True,null=True)
    bgcolor=models.CharField(max_length=10,blank=True,null=True,default=bgcolor)
    company=models.CharField(max_length=100,null=True,blank=True,default=env('SITE_NAME'))
    profile_pic=models.ImageField(upload_to='profiles/',null=True,blank=True,default="placeholder.jpg")
    role=models.CharField(choices=user_roles,max_length=200,null=True,blank=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='extended_auth_user'
        verbose_name_plural='extended_auth_users'
        permissions=(
            ("can_view","Can view"),
            ("can_edit","Can edit"),
            ("can_see_invoice","Can see invoice"),
        )
    def __str__(self)->str:
        return f'{self.user.username} extended auth profile'




#generate random
def generate_serial():
    return get_random_string(12,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')
 

 




class ContactModel(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',max_length=13)
    subject=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,blank=True,null=True)
    is_read=models.BooleanField(default=False,blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    reply=models.TextField(blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='contact_tbl'
        verbose_name_plural='contact_tbl'
    def __str__(self)->str:
        return f'{self.name} contact message'

class ApplicationModel(models.Model):
    application_serial=models.CharField(max_length=255,default=generate_serial)
    applicant_fname=models.CharField(max_length=100,blank=True,null=True)
    applicant_mname=models.CharField(max_length=100,blank=True,null=True)
    applicant_lname=models.CharField(max_length=100,blank=True,null=True)
    prefix=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    mobile_phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',max_length=13) 
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',max_length=13)
    fax=models.CharField(max_length=100,null=True,blank=True)
    address1=models.CharField(max_length=100,null=True,blank=True)
    address2=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    zip_code=models.CharField(max_length=100,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    apply_as=models.CharField(max_length=100,null=True,blank=True)
    biz_location1=models.CharField(max_length=100,null=True,blank=True)
    biz_location2=models.CharField(max_length=100,null=True,blank=True)
    biz_city=models.CharField(max_length=100,null=True,blank=True)
    biz_state=models.CharField(max_length=100,null=True,blank=True)
    biz_zip_code=models.CharField(max_length=100,null=True,blank=True)
    marketing_material=models.FileField(upload_to='uploads/',null=True,blank=True,default='')
    marketing_information=models.FileField(upload_to='uploads/',null=True,blank=True,default='')
    statement=models.CharField(max_length=100,null=True,blank=True)
    statement_information=models.FileField(upload_to='uploads/',null=True,blank=True,default='')
    been_financed=models.CharField(max_length=100,null=True,blank=True)
    lender_name=models.CharField(max_length=100,null=True,blank=True)
    finance_was_for=models.CharField(max_length=100,null=True,blank=True)
    loan_reason=models.CharField(max_length=100,null=True,blank=True)
    project_gross_value=models.CharField(max_length=100,null=True,blank=True)
    loan_amount=models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(default=now)
    class Meta:
        db_table='application_table'
        verbose_name_plural='application_table'
        ordering=('created_at',)

    def delete(self, using=None,keep_parents=False):
        if self.marketing_material or self.statement_information or self.marketing_information:
            self.marketing_material.storage.delete(self.marketing_material.name)
            self.marketing_information.storage.delete(self.marketing_information.name)
            self.statement_information.storage.delete(self.statement_information.name)
        super().delete()