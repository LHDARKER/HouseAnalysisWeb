# Generated by Django 2.1.5 on 2020-03-30 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0005_community_communityrange'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='num',
            field=models.IntegerField(default=1, verbose_name='数量'),
            preserve_default=False,
        ),
    ]