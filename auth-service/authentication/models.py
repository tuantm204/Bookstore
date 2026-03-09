from django.db import models
import hashlib
import os


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    salt = models.CharField(max_length=64)
    full_name = models.CharField(max_length=255, blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        """Hash password with salt using SHA-256."""
        self.salt = os.urandom(32).hex()
        self.password_hash = hashlib.sha256(
            (raw_password + self.salt).encode('utf-8')
        ).hexdigest()

    def check_password(self, raw_password):
        """Verify password against stored hash."""
        return self.password_hash == hashlib.sha256(
            (raw_password + self.salt).encode('utf-8')
        ).hexdigest()

    def __str__(self):
        return f'{self.username} ({self.role})'

    class Meta:
        db_table = 'auth_users'
