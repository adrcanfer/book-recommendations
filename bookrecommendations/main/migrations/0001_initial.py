# Generated by Django 2.1.5 on 2019-01-17 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('bookURL', models.URLField()),
                ('author', models.IntegerField()),
                ('coverURL', models.URLField()),
                ('npages', models.IntegerField()),
                ('editorial', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=50)),
                ('binding', models.CharField(choices=[('B', 'Tapa blanda'), ('D', 'Tapa dura')], max_length=50)),
                ('category', models.CharField(choices=[('Contemporánea', 'Contenporánea')], max_length=50)),
            ],
        ),
    ]
