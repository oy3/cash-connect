from django.db import models


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
