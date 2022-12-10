from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import AuthUser, CompanyUser


@receiver(post_save, sender=AuthUser)
def create_company_user_for_auth_user(created: bool, instance: AuthUser, *args, **kwargs):
    if not created:
        return
    CompanyUser.objects.create(user=instance, email_address=instance.email)
