# Generated by Django 3.2.5 on 2021-09-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_watchlist_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
