# Generated by Django 2.1.5 on 2019-07-30 00:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0011_auto_20190726_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membro',
            options={'ordering': ['matricula']},
        ),
        migrations.AlterField(
            model_name='membro',
            name='data_cadastro',
            field=models.DateField(default=datetime.date(2019, 7, 29), max_length=10, verbose_name='Data de Cadastro'),
        ),
    ]
