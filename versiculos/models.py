from django.db import models

class Versiculo(models.Model):
    texto = models.TextField()
    referencia = models.CharField(max_length=100, default='')
    usado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto[:50]} ({self.referencia})"

class Contador(models.Model):
    total = models.IntegerField(default=0)
