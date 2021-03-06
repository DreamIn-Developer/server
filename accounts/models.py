from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, nickname, password=None, **kwargs):

        if not nickname:
            raise ValueError('must have user nickname')

        user = self.model(
            nickname=nickname,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **kwargs):

        user = self.create_user(
            nickname=nickname,
            description='',
            password = password,
            **kwargs,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    nickname = models.CharField(max_length=15, unique=True)
    profile_image = models.URLField(max_length=511, blank=True, default='')
    background_image = models.URLField(max_length=511, blank=True, default='')
    description = models.TextField(blank=True, default='')
    social_id = models.TextField()
    categories = models.ManyToManyField('accounts.SubCategory')

    class SocialType(models.TextChoices):
        KAKAO = 'Ka', _('Kakao')
        GOOGLE = 'Go', _('Google')

    social_type = models.CharField(
        max_length=2,
        choices=SocialType.choices,
        default=SocialType.KAKAO,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def post_count(self):
        return self.post_set.count()

    @property
    def scrap_count(self):
        return self.mark_user.count()

    @property
    def following_count(self):
        return self.follower.count()

    @property
    def follower_count(self):
        return self.followed_user.count()

    class Meta:
        ordering = ['-id']

@receiver(post_save, sender=User)
def create_user(sender, instance, created, *args, **kwargs):
    if created:
        instance.nickname = f'?????????{instance.id}'
        instance.save()

class MainCategory(models.Model):
    class MainCategoryType(models.TextChoices):
        ART = '??????/?????????'
        MUSIC = '??????/??????'
        MEDIA = '??????/?????????'
        SHOW = '??????/??????'

    name = models.CharField(
        max_length=15,
        choices=MainCategoryType.choices,
        default=MainCategoryType.ART,
    )
    def __str__(self):
        return self.name

    @property
    def main_category(self):
        return self.name

class SubCategory(models.Model):
    main = models.ForeignKey('accounts.MainCategory', on_delete=models.CASCADE, related_name='subcategory')
    class SubCategoryType(models.TextChoices):
        FINE = '????????????'
        RIDICULE = '??????/??????'
        CRAFT = '??????'
        ILLUSTRATION = '????????????'
        INDUSTRIAL_DESIGN = '???????????????'
        CONSTRUCT = '??????'
        TRADITIONAL_ART = '????????????'

        CLASSIC = '?????????'
        PIANO = '?????????'
        BAND = '??????'
        COMPOSITION = '??????/??????'
        TRADITIONAL_MUSIC = '????????????'
        K_POP = 'K-POP'

        MOTION_GRAPHIC = '???????????????'
        PD = 'pd'
        MOVIE = 'movie'
        ANIMATION = 'animation'
        THREE_D = '3D??????'
        GAME_GRAPHIC = '???????????????'
        PICTURE = '??????'

        PERFORMANCE = '????????????'
        MODERN_DANCE = '????????????'
        ACTING = '??????'
        SCENARIO = '??????/??????'

    name = models.CharField(
        max_length=15,
        choices=SubCategoryType.choices,
        default=SubCategoryType.FINE,
    )

    def __str__(self):
        return self.name

class FollowRelation(models.Model):
    follower = models.ForeignKey('accounts.User', related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey('accounts.User', related_name='followed_user', on_delete=models.CASCADE)