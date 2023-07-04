from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import Articolo

class AnnuncioDetailViewTestCase(TestCase):
    """
    Test che crea un articolo nel database, controlla che la pagina detail venga visualizzata,
    che esista e che abbia i campi corretti.
    """

    def test_caricamento_pagina_detail(self):
        # Creazione di un annuncio di prova
        articolo = Articolo.objects.create(
            venditore = 'gianni',
            titolo='Articolo di prova',
            schedaTecnica='Descrizione dell\'annuncio di prova',
            categoria='Elettronica',
            prezzoIniziale=99.99,
            immagine = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg'),
            durataAsta=12
        )

        # Ottienimento dell'URL della pagina di dettaglio dell'annuncio
        url = reverse('gestione:annuncio-detail', kwargs={'pk': articolo.pk})

        # Viene effettuata una richiesta GET alla pagina di dettaglio dell'articolo
        response = self.client.get(url)

        # Controllo sulla risposta che abbia un codice HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Controllo del template corretto
        self.assertTemplateUsed(response, 'annuncio_detail.html')

        # Controllo che l'articolo visualizzato nella pagina sia quello corretto
        self.assertEqual(response.context['articolo'], articolo)

        # Controllo che il titolo dell'articolo sia presente nel contenuto della risposta
        self.assertContains(response, articolo.titolo)

class ArticoloInputTestCase(TestCase):
    """
    Test che tenta l'inserimento di un articolo con campi non accettabili tramite POST
    e venga rifiutato dalla piattaforma.
    """
    def test_inserimento_articolo(self):
        # Creazione di un'immagine falsa per il test
        immagine = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        # Viene effettuata una richiesta POST per l'inserimento di un nuovo articolo
        response = self.client.post(reverse('gestione:annuncio-create'), {
            'titolo': '*^&%#Ciao',
            'schedaTecnica': '!@#$^&*Prova',
            'categoria': 'Elettronica',
            'prezzoIniziale': 50.00,
            'immagine' : immagine,
            'durataAsta': 12
        })

        # Controllo  sulla risposta che abbia un codice HTTP 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Ricerca di un articolo con lo stesso titolo del tentato inserimento
        articolo = Articolo.objects.filter(titolo='*^&%#Ciao')

        # L'articolo non esiste
        self.assertEqual(articolo.exists(), False)
