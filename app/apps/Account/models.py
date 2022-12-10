from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings

from utils import generate_key


class Company(models.Model):
    key = models.CharField(
        max_length=4,
        unique=True,
        editable=False,
    )
    name = models.CharField(
        max_length=128,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key(4)
        return super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def create_user(self, email, company, password=None):
        """
        Creates and saves a normal user.
        """

        user = self.model(
            email=self.normalize_email(email),
            company=company,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, company: int, password=None):
        """
        Creates and saves a superuser.
        """
        company_obj = Company.objects.get(id=company)
        user = self.create_user(
            email,
            company=company_obj,
            password=password
        )
        user.is_admin = True
        user.save()
        return user


class AuthUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        related_name="users"
    )
    is_admin = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    registration_date = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company', ]
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, Auth):
        # "Does the user have permissions to view the app Auth?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CompanyUser(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user",
    )
    first_name = models.CharField(
        max_length=128,
    )
    last_name = models.CharField(
        max_length=128,
    )
    email_address = models.EmailField()
    phone_number_1 = models.CharField(
        max_length=18,
        blank=True,
    )
    phone_number_2 = models.CharField(
        max_length=18,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def company(self):
        return self.user.company
