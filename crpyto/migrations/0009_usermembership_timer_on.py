# Generated by Django 3.2.15 on 2022-09-25 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crpyto', '0008_auto_20220922_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='timer_on',
            field=models.BooleanField(default=False),
        ),
    ]