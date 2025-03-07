from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_('Data'))
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Waga'))
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Talia'))
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Biodra'))
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Klatka piersiowa'))
    thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Udo'))
    calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Łydka'))
    forearm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Przedramię'))

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s measurements on {self.date}"

    