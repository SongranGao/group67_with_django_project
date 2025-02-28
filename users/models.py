from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    USER_GENDER_TYPE = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    owner = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='user')
    nike_name = models.CharField('Name',max_length=23,blank=True,default='')
    desc = models.TextField('Personal Description',max_length=200,blank=True,default='')
    character_signature = models.CharField('Character Signature',max_length=100,blank=True,default='')
    birthday = models.DateField('Birthday',null=True,blank=True)
    gender = models.CharField('Gender',max_length=6,choices=USER_GENDER_TYPE, default = '')
    address = models.CharField('Address', max_length=100, blank=True, default = '')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png',max_length=100,verbose_name='user photo')

    class Meta:
        verbose_name = 'user data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username

class EmailVerifyRecord(models.Model):
    """Record of the email verification code"""

    SEND_TYPE_CHOICES = (
        ('register','register'),
        ('forget','retrieve password')
    )

    code = models.CharField('verification code',max_length=20)
    email = models.EmailField('email',max_length=35)
    send_type = models.CharField(choices = SEND_TYPE_CHOICES, default = 'register',max_length=20)

    class Meta:
        verbose_name='Email Verification Code'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code