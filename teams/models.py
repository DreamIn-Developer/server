from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from notifications.models import Notification

class Member(models.Model, DirtyFieldsMixin):
    team = models.ForeignKey('teams.TeamProfile', on_delete=models.CASCADE, related_name='joined_team')
    member = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='joined_user')

    class MemberType(models.TextChoices):
        CONFIRMED = 'confirmed', _('Confirmed')
        PENDED = 'pended', _('Pended')

    member_type = models.CharField(
        max_length=15,
        choices=MemberType.choices,
        default=MemberType.PENDED,
    )

    @property
    def nickname(self):
        return self.member.nickname

    @property
    def post_count(self):
        return self.member.post_count

    @property
    def image(self):
        return self.member.image.url


class TeamProfile(models.Model):
    title = models.CharField(max_length=31)
    description = models.TextField()
    image = models.ImageField(upload_to='team', blank=True, default='')
    leader = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='team_leader')
    members = models.ManyToManyField(
        'accounts.User',
        through='teams.Member',
        through_fields=('team', 'member'), )

    @property
    def member_count(self):
        return self.joined_team.count()

    @property
    def post_count(self):
        return self.teampost_set.count()

    @property
    def team_follow_count(self):
        return self.followed_team.count()

class TeamFollowRelation(models.Model):
    follower = models.ForeignKey('accounts.User', related_name='team_follower', on_delete=models.CASCADE)
    team = models.ForeignKey('teams.TeamProfile', related_name='followed_team', on_delete=models.CASCADE)

@receiver(post_save, sender=TeamProfile)
def create_team_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(team=instance, member=instance.leader, member_type='Le')

@receiver(post_save, sender=Member)
def create_member_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.member, messages=f"{instance.team.title}에 초대되었습니다.")