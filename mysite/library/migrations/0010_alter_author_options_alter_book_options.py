# Generated by Django 4.1.1 on 2022-10-09 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_bookinstance_book'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Autorius', 'verbose_name_plural': 'Autoriai'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Knyga', 'verbose_name_plural': 'Knygos'},
        ),
    ]
