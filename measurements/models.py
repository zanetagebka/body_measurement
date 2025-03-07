from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    forearm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s measurements on {self.date}"

    