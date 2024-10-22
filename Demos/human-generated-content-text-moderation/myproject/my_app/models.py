from django.db import models

# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]  # Display the first 20 characters of the comment