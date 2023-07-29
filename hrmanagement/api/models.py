from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from phone_field import PhoneField
from .manager import UserManager
import uuid
          
class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=200,unique=True)
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True)
    profile_image=models.ImageField(upload_to='profileimg')
    contact=PhoneField(help_text='Contact phone number')
    department=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['contact','email','is_admin']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Leave(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')
    date_from=models.DateTimeField()
    date_to=models.DateTimeField()
    status=models.CharField(max_length=255,default='Unseen')
    reason=models.CharField(max_length=1000)
    remarks=models.CharField(max_length=1000,blank=True)
    app_date=models.DateField(auto_now_add=True)

class Resume(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    dob=models.DateField()
    address=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    pimage=models.ImageField(upload_to='pimages')
    rdocs=models.FileField(upload_to='rdocs')
    created_by=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    unique_id=models.UUIDField(unique=True)

class Announcement(models.Model):
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING,to_field='username')
    announcement=models.CharField(max_length=5000)
    date=models.DateField(auto_now_add=True)