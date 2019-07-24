# Generated by Django 2.1.5 on 2019-01-14 15:41

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membro',
            name='Cep',
            field=models.BigIntegerField(default=123, verbose_name='CEP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membro',
            name='cpf',
            field=models.BigIntegerField(default=1234, verbose_name='CPF'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membro',
            name='estado',
            field=localflavor.br.models.BRStateField(default='SP', max_length=2),
            preserve_default=False,
        ),
    ]
