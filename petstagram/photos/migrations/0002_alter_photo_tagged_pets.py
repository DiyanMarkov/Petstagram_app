# Generated by Django 5.0.4 on 2024-06-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_alter_pet_slug'),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='tagged_pets',
            field=models.ManyToManyField(blank=True, to='pets.pet'),
        ),
    ]
