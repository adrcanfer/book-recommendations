# Generated by Django 2.1.5 on 2019-01-20 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190118_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Contemporánea', 'Contemporánea'), ('Negra', 'Negra'), ('Romántica', 'Romántica'), ('Cómics', 'Cómics'), ('Historia', 'Historia'), ('Adolescentes', 'Adolescentes'), ('Infantil', 'Infantil')], max_length=50),
        ),
    ]
