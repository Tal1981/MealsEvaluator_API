from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Meal(models.Model):
    title = models.CharField(max_length=32, unique=True)
    description = models.TextField(max_length=360, default='No description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useroo', null=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    meal = models.ForeignKey(Meal, related_name='ratingsoo', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)

    class Meta:
        unique_together = (('meal', 'user'),)
        indexes = [
            models.Index(fields=['meal', 'user']),
        ]