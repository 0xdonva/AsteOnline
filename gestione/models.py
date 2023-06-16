from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class Utente(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email:',
        max_length=254,
        unique=True)
    username = models.CharField(
        verbose_name='Username:',
        max_length=30,
        unique=True)
    password = models.CharField(
        verbose_name="Password:",
        max_length=20)
    is_venditore = models.BooleanField(
        verbose_name="Venditore:",
        default=False)

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Utente, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Utenti"

class Articolo(models.Model):

    # Qua andrebbe l'ID ma viene messo in automatico
    venditore = models.ForeignKey(Utente, on_delete=models.CASCADE)
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

    acquirente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Offerte"

class Recensione(models.Model):

    acquirente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="acquirente")
    venditore = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name="venditore")
    testo = models.TextField()
    voto = models.IntegerField()

    class Meta:
        verbose_name_plural = "Recensioni"