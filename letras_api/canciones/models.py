from django.db import models

class LetraCancion(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    letra = models.TextField(blank=True)
    emocion = models.CharField(max_length=50, blank=True)
    puntaje = models.FloatField(null=True, blank=True)
    portada_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
