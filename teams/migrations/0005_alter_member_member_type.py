# Generated by Django 4.0.3 on 2022-04-16 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_alter_member_member_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_type',
            field=models.CharField(choices=[('confirmed', 'Confirmed'), ('pended', 'Pended')], default='pended', max_length=15),
        ),
    ]
