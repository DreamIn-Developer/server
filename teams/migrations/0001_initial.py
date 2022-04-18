# Generated by Django 4.0.3 on 2022-04-18 03:39

import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_type', models.CharField(choices=[('confirmed', 'Confirmed'), ('pended', 'Pended')], default='pended', max_length=15)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name='TeamProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, default='', upload_to='team')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_leader', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(through='teams.Member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamFollowRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_follower', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_team', to='teams.teamprofile')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joined_team', to='teams.teamprofile'),
        ),
    ]
