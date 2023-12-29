from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class user(AbstractBaseUser,PermissionsMixin):

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)

    fullname = models.CharField(max_length=50, blank=True, null=True)  
    gender = models.CharField(max_length=10, blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    phoneNo = models.CharField(max_length=13, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def create(self, validated_data):
        user = user(**validated_data)
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

class CardDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    cardNo = models.CharField(max_length=16)
    nameOnCard = models.CharField(max_length=50)
    expiryDate = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.user.email

class otp(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiryDate = models.DateTimeField()

    def __str__(self):
        return self.user.email 