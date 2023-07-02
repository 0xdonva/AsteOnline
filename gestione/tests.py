from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import Articolo

class AnnuncioDetailViewTestCase(TestCase):
    def test_caricamento_pagina_detail(self):
        # Crea un annuncio di prova
        articolo = Articolo.objects.create(
            venditore = 'gianni',
            titolo='Articolo di prova',
            schedaTecnica='Descrizione dell\'annuncio di prova',
            categoria='Elettronica',
            prezzoIniziale=99.99,
            immagine = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg'),
            durataAsta=12
        )

        # Ottieni l'URL della pagina di dettaglio dell'annuncio
        url = reverse('gestione:annuncio-detail', kwargs={'pk': articolo.pk})

        # Effettua una richiesta GET alla pagina di dettaglio dell'articolo
        response = self.client.get(url)

        # Controlla che la risposta abbia un codice HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Controlla che il template utilizzato sia corretto
        self.assertTemplateUsed(response, 'annuncio_detail.html')

        # Controlla che l'articolo visualizzato nella pagina sia quello corretto
        self.assertEqual(response.context['articolo'], articolo)

        # Controlla che il titolo dell'articolo sia presente nel contenuto della risposta
        self.assertContains(response, articolo.titolo)

class ArticoloInputTestCase(TestCase):
    def test_inserimento_articolo(self):
        immagine = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        # Effettua una richiesta POST per l'inserimento di un nuovo articolo
        response = self.client.post(reverse('gestione:annuncio-create'), {
            'titolo': '*^&%#Ciao',
            'schedaTecnica': '!@#$^&*Prova',
            'categoria': 'Elettronica',
            'prezzoIniziale': 50.00,
            'immagine' : immagine,
            'durataAsta': 12
        })

        # Controlla che la risposta abbia un codice HTTP 302 (redirect)
        self.assertEqual(response.status_code, 302)

        articolo = Articolo.objects.filter(titolo='*^&%#Ciao')

        self.assertEqual(articolo.exists(), False)
