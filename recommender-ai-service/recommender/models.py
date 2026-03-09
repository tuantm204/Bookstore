from django.db import models

class Recommendation(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommend book {self.book_id} for customer {self.customer_id}"
