from django.db import models



class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=True)
    confirm_password = models.CharField(max_length=100, blank=True)

    # Admin field
    is_admin = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=20, default='email')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    def is_oauth_user(self):
        return self.auth_provider == 'google'
