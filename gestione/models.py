from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.

class Articolo(models.Model):
    CATEGORIE = [
        ('Elettronica','Elettronica'),
        ('Informatica','Informatica'),
        ('CD e Vinili', 'CD e Vinili'),
        ('Videogiochi','Videogiochi'),
        ('Strumenti musicali', 'Strumenti musicali'),
        ('Film e DVD', 'Film e DVD')
    ]
    ORE = [
        (12, 12),
        (24, 24),
        (48, 48),
        (72, 72)
    ]

    # Qua andrebbe l'ID ma viene messo in automatico
    venditore = models.CharField(max_length=20)
    titolo = models.CharField(max_length=20)
    schedaTecnica = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIE, default='Elettronica')
    immagine = models.ImageField(upload_to="articoli/", height_field=None, width_field=None, max_length=None)
    prezzoIniziale = models.DecimalField(max_digits=5, decimal_places=2)
    prezzoRiserva = models.DecimalField(max_digits=5, decimal_places=2)
    dataInizioAsta = models.DateTimeField(auto_now=False, auto_now_add=True)
    durataAsta = models.IntegerField(choices=ORE, default=12)
    dataFineAsta = models.DateTimeField(auto_now=False, auto_now_add=False)
    terminato = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.dataFineAsta = timezone.now() + timedelta(hours=self.durataAsta)
        super(Articolo, self).save(*args, **kwargs)

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Articoli"

class Offerta(models.Model):

    acquirente = models.ForeignKey(User, on_delete=models.CASCADE)
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.elimina_offerte_precedenti()

    def elimina_offerte_precedenti(self):
        offerte_precedenti = Offerta.objects.filter(articolo=self.articolo, saldo__lt=self.saldo)
        offerte_precedenti.delete()

    class Meta:
        verbose_name_plural = "Offerte"

class Recensione(models.Model):

    acquirente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acquirente")
    venditore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="venditore")
    testo = models.TextField()
    voto = models.IntegerField()

    class Meta:
        verbose_name_plural = "Recensioni"