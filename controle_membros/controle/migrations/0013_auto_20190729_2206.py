# Generated by Django 2.1.5 on 2019-07-30 01:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('controle', '0012_auto_20190729_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='membro',
            name='addInformacoes',
            field=models.TextField(blank=True, verbose_name='Informações Adicionais'),
        ),
        migrations.AddField(
            model_name='membro',
            name='dataBatismoA',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data de Batismo nas Águas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membro',
            name='dataBatismoE',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Data de Batismo com o Espírito Santo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membro',
            name='recebimento',
            field=models.CharField(choices=[('A', ' Por aclamação'), ('M', 'Com carta de mudança'), ('B', 'Por Batismo')], default='B', max_length=5, verbose_name='Recebimento'),
        ),
    ]
