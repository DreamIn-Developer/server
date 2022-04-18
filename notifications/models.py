from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import User
from teams.models import Member


class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    messages = models.CharField(max_length=32)
    is_read = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance, messages="가입을 축하합니다.")

@receiver(post_save, sender=Member)
def change_member_notification(sender, instance, **kwargs):
    if instance.is_dirty:
        Notification.objects.create(user=instance.member, messages=f"{instance.team.title}팀원으로 합류되었습니다.")

@receiver(post_delete, sender=Member)
def delete_member_notification(sender, instance, **kwargs):
    Notification.objects.create(user=instance.member, messages=f"아쉽게도 {instance.team.title}팀원으로 합류지 못하게 되었습니다.")