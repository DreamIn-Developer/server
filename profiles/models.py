from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from notifications.models import Notification


class Profile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    email = models.EmailField(max_length=32, unique=True)
    nickname = models.CharField(max_length=16, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='image', blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Member(models.Model, DirtyFieldsMixin):
    team = models.ForeignKey('profiles.Teamprofile', on_delete=models.CASCADE)
    member = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    class MemberType(models.TextChoices):
        LEADER = 'Le', _('Leader')
        NORMAL = 'No', _('Normal')

    member_type = models.CharField(
        max_length=2,
        choices=MemberType.choices,
        default=MemberType.NORMAL,
    )

class Teamprofile(models.Model):
    title = models.CharField(max_length=31)
    description = models.TextField()
    leader = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='team_leader')
    members = models.ManyToManyField(
        'accounts.User',
        through='profiles.Member',
        through_fields=('team', 'member'), )

@receiver(post_save, sender=Teamprofile)
def create_team_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(team=instance, member=instance.leader, member_type='Le')

@receiver(post_save, sender=Member)
def create_member_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.member, messages=f"{instance.team.title}에 초대되었습니다.")

