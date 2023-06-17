from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Articolo(models.Model):

    # Qua andrebbe l'ID ma viene messo in automatico
    venditore = models.ForeignKey(User, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=20)
    schedaTecnica = models.TextField()
    immagine = models.CharField(max_length=20)
    prezzoIniziale = models.DecimalField(max_digits=5, decimal_places=2)
    prezzoRiserva = models.DecimalField(max_digits=5, decimal_places=2)
    prezzoAttuale = models.DecimalField(max_digits=5, decimal_places=2)
    dataInizioAsta = models.DateTimeField(auto_now=False, auto_now_add=False)
    durataAsta = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.venditore.is_venditore == False:
            raise Exception("Non è un venditore")
        super(Articolo, self).save(*args, **kwargs)

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Articoli"

class Offerta(models.Model):

    acquirente = models.ForeignKey(User, on_delete=models.CASCADE)
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Offerte"

class Recensione(models.Model):

    acquirente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acquirente")
    venditore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="venditore")
    testo = models.TextField()
    voto = models.IntegerField()

    class Meta:
        verbose_name_plural = "Recensioni"