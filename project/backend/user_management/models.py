from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    # Add any additional fields you want
    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)