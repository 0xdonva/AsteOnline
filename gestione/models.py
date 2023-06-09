from django.db import models

# Create your models here.

class Venditore(models.Model):

    username = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    via = models.CharField(max_length=20)
    numCivico = models.CharField(max_length=20)
    CAP = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Venditori"

class Acquirente(models.Model):

    username = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    via = models.CharField(max_length=20)
    numCivico = models.CharField(max_length=20)
    CAP = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Acquirenti"

class Articolo(models.Model):

    # Qua andrebbe l'ID ma viene messo in automatico
    venditore = models.ForeignKey(Venditore, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=20)
    schedaTecnica = models.TextField()
    immagine = models.CharField(max_length=20)
    prezzoIniziale = models.DecimalField(max_digits=5, decimal_places=2)
    prezzoRiserva = models.DecimalField(max_digits=5, decimal_places=2)
    prezzoAttuale = models.DecimalField(max_digits=5, decimal_places=2)
    dataInizioAsta = models.DateTimeField(auto_now=False, auto_now_add=False)
    durataAsta = models.IntegerField()

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Articoli"

class Offerta(models.Model):

    acquirente = models.ForeignKey(Acquirente, on_delete=models.CASCADE)
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Offerte"

class Recensione(models.Model):

    acquirente = models.ForeignKey(Acquirente, on_delete=models.CASCADE)
    venditore = models.ForeignKey(Venditore, on_delete=models.CASCADE)
    testo = models.TextField()
    voto = models.IntegerField()

    class Meta:
        verbose_name_plural = "Recensioni"