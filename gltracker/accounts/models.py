from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    height = models.IntegerField(null=True)
    target_weight = models.DecimalField(max_digits=7, decimal_places=2, null=True)


class WeightRecord(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.entry_date}"