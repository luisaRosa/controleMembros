# Generated by Django 2.1.5 on 2019-01-14 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0003_auto_20190114_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='membro',
            name='conjuge',
            field=models.CharField(blank=True, max_length=100, verbose_name='Conjugue'),
        ),
        migrations.AlterField(
            model_name='membro',
            name='estado_civil',
            field=models.CharField(choices=[('S', 'Solteiro(a)'), ('C', 'Casado(a)'), ('V', 'Viúvo(a)')], default='S', max_length=5, verbose_name='Estado Civil'),
        ),
    ]
