# Generated by Django 4.2.2 on 2023-06-30 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0008_articolo_datafineasta'),
    ]

    operations = [
        migrations.AddField(
            model_name='articolo',
            name='terminato',
            field=models.BooleanField(default=False),
        ),
    ]