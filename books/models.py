from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Define roles as integers
class Role(models.IntegerChoices):
    SUPERADMIN = 0, 'Super Admin'
    OEM_ADMIN = 1, 'OEM Admin'
    OEM_USER = 2, 'OEM User'
    DEALER_ADMIN = 3, 'Dealer Admin'
    DEALER_USER = 4, 'Dealer User'
    CUSTOMER = 5, 'Customer'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPERADMIN)  # Ensure SuperAdmin role
        return self.create_user(email, password, **extra_fields)

class Oem(models.Model):
    oem_name = models.CharField(max_length=255)
    oem_number = models.CharField(max_length=50, unique=True)  # OemNo should be unique for each OEM

    def __str__(self):
        return self.oem_name

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=255)
    dealer_number = models.CharField(max_length=50, unique=True)  # DealerNo should be unique for each Dealer
    oem = models.ForeignKey(Oem, on_delete=models.CASCADE, related_name='dealers')  # Link dealer to an OEM

    def __str__(self):
        return self.dealer_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=Role.choices, default=Role.CUSTOMER)
    oem = models.ForeignKey(Oem, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')  # OemNo
    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')  # DealerNo
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    dealer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')  # Reference to the CustomUser (dealer)

    def __str__(self):
        return self.title
