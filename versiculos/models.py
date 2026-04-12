from django.db import models


class Versiculo(models.Model):
    texto = models.TextField()
    referencia = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.texto[:50]} ({self.referencia})"


class ControleDiario(models.Model):
    data = models.DateField(unique=True)
    contador = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.data} - {self.contador}"


class VersiculoUsado(models.Model):
    data = models.DateField()
    versiculo = models.ForeignKey(Versiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data} - {self.versiculo.referencia}"