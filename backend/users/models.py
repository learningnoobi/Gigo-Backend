from secrets import choice
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email,username, password=None, **extra_fields):
        """
          Create and save a SuperUser with the given email,first name , lastname and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        # if not password:
        #     raise ValueError(_('Password must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email,first name , lastname and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,username, password, **extra_fields)



class User(AbstractUser):

    R_TYPE = (
        ("Admin","Admin"),
        ("Customer","Customer"),
        ("Enterprise","Enterprise"),
    )

    username = models.CharField(max_length=200,unique=True)
    iroha_name = models.CharField(max_length=200,unique=True,null=True,blank=True) #unique name of iroha network
    email = models.EmailField(max_length=200, unique=True)
    bio = models.TextField(blank=True ,default="")
    avatar = models.ImageField(default='default.jpg', upload_to='avatars')
    qr_code = models.ImageField(null=True,blank=True,upload_to='qrcode')
    role = models.CharField(choices=R_TYPE, max_length=20,default='Customer')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
   
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural="Custom Users"

    def __str__(self):
        return f'{self.username}'
