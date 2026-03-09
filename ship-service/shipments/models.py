from django.db import models

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]
    order_id = models.IntegerField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment for order #{self.order_id} - {self.status}"
