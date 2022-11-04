# Generated by Django 3.2.8 on 2021-12-20 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crpyto', '0027_alter_userwallet_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='roi',
            field=models.CharField(default='8%', max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermembership',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]
