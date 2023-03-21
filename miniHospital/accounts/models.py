from fileinput import filename
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email,state,district,gender,dob,contact, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            state=state,
            dob=dob,
            gender=gender,
            district=district,
            contact = contact,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


# class MyAccountManager(BaseUserManager):
#     def create_user(self,username, email, password=None):
#         if not email:
#             raise ValueError('User must have an email address')

#         if not username:
#             raise ValueError('User must have an username')

#         user = self.model(
#             email = self.normalize_email(email),
#             username = username,
            
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


    
    def create_superuser(self,username,password,email):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            # first_name = first_name,
            # last_name = last_name,
        )
        user.is_admin = True
        user.is_active = False
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


 
class Account(AbstractBaseUser):
    
    state_choices = (('kerala','kerala'),('demo','demo'),('None','None'))
    gender_choices=(('Male','Male'),('Female','Female'),('others','others'), ('None','None'))
    district_choices=(
        ('Kozhikode','Kozhikode'),
        ('Malappuram','Malappuram'),
        ('Kannur','Kannur'),
        ('Trivandrum','Trivandrum'),
        ('Palakkad','Palakkad'),
        ('Thrissur','Thrissur'),
        ('Kottayam','Kottayam'),
        ('Alappuzha','Alappuzha'),
        ('Idukki','Idukki'),
        ('Kollam','Kollam'),
        ('Ernakulam','Ernakulam'),
        ('Wayanad','Wayanad'),
        ('Kasaragod','Kasaragod'),
        ('Pathanamthitta','Pathanamthitta'),
        ('Thiruvananthapuram','Thiruvananthapuram'),
        ('None','None'),
    )

    id            = models.AutoField(primary_key=True)
    first_name      = models.CharField(max_length=50, default='')
    last_name       = models.CharField(max_length=50, default='')
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    contact         = models.BigIntegerField(default=0)
    state           = models.CharField(max_length=50,choices=state_choices,default='kerala')
    # age             = models.IntegerField(default=0)
    district        = models.CharField(max_length=50,choices=district_choices,default='None')
    gender          = models.CharField(max_length=50,choices=gender_choices, default='None')
    dob             =models.DateField(default=datetime.date.today())
    usr_img         = CloudinaryField(blank=True, null=True)


    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_lab          = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_doctor       = models.BooleanField(default=False)
    is_patient      = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','district','state','gender','contact']
    # REQUIRED_FIELDS = ['username','password']




    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    # def clean(self):
    #     if len(self.first_name)!=10:
    #         raise ValidationError("enter above 4 charector")


    
# table for store otp details
import uuid
class Otp(models.Model):
    user_id=models.ForeignKey(Account,on_delete=models.CASCADE)
    otp=models.IntegerField(blank=True,null=True)
    uid=models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    phone=models.BigIntegerField(default=0)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.username