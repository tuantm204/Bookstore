from django.db import models

class Comment(models.Model):
    customer_id = models.IntegerField()
    book_id = models.IntegerField()
    content = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by customer {self.customer_id} on book {self.book_id}"
