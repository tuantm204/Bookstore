from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    # Address - tách riêng thành các trường
    street = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    @property
    def full_address(self):
        """Trả về địa chỉ đầy đủ ghép từ các trường"""
        parts = [self.street, self.city, self.state, self.zip_code]
        return ', '.join(p for p in parts if p)
