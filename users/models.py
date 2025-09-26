from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True  
        kwargs['is_agent'] = False 

        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.save(using=self._db)
        return user


    

class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)

    # Optional fields
    address = models.CharField(max_length=500, null=True, blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+263774556973'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )
    whatsapp_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )

    date_of_birth = models.DateField(null=True, blank=True)
    national_id_number = models.CharField(max_length=100, null=True, blank=True)
    citizenship = models.CharField(max_length=50, null=True, blank=True)
    country_of_residence = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)

    # dealer-specific fields
    company_name = models.CharField(max_length=255, null=True, blank=True)
      # --- ADDED: Fields for dealer ratings and reviews ---
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=4.5)
    reviews = models.PositiveIntegerField(default=0, null=True, blank=True)

    category = models.CharField(max_length=255, blank=True, null=True)
    is_dealer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_agent = models.BooleanField(default=False) 

    
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now) # <-- ADD THIS LINE
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    def __str__(self):
    
        if self.is_agent and self.company_name:
            return self.company_name
        return self.email

    def save(self, *args, **kwargs):
   
        if not self.is_agent:
            self.company_name = None
            self.category = None
        super().save(*args, **kwargs)
