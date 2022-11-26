# Generated by Django 3.2.15 on 2022-09-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crpyto', '0004_auto_20220904_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_ip',
            name='city',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='country',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='loc',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='org',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='postal',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='region',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AddField(
            model_name='user_ip',
            name='timezone',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='user_ip',
            name='ip',
            field=models.CharField(default=None, max_length=500),
        ),
    ]