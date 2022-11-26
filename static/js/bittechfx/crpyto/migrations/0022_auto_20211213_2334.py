# Generated by Django 3.2.8 on 2021-12-13 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crpyto', '0021_alter_userwallet_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='membership',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='membership',
            field=models.ManyToManyField(null=True, related_name='user_membership', to='crpyto.Membership'),
        ),
    ]