from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def bmi(self):
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    def __str__(self):
        return f"{self.user.username} - {self.date}"