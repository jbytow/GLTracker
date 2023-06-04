from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2)

    def bmi(self):
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    def __str__(self):
        return f"{self.user.username} - {self.date}"