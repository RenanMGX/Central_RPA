# Generated by Django 5.1 on 2025-02-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidar_dados_multiplas_planilhas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaminhoAutomacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField()),
            ],
        ),
    ]
