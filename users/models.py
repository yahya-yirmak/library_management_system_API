from django.db import models
from django.contrib.auth.models import AbstractUser


# CREATE A CUSTOM USER MODEL
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now_add=True)



# CREATE A USER'S PROFILE MODEL
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
