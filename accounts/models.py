from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password, description, image, **kwargs):

        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            email=email,
            nickname=nickname,
            description=description,
            image=image,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, nickname, password=None, description=None, image=None, **kwargs):

        user = self.create_user(
            email = email,
            nickname=nickname,
            description='',
            image='',
            password = password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(max_length=255,unique=True,)
    nickname = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='profile', blank=True, default='')
    description = models.TextField(blank=True, default='')
    social_id = models.TextField()
    categories = models.ManyToManyField('accounts.Category')

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
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
        return self.bookmark_set.count()

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
        instance.nickname = f'드림인{instance.id}'
        instance.save()

class Category(models.Model):
    class MainCategoryType(models.TextChoices):
        ART = '미술/디자인'
        MUSIC = '음악/작곡'
        MEDIA = '영상/미디어'
        SHOW = '무용/연극'

    main_category = models.CharField(
        max_length=15,
        choices=MainCategoryType.choices,
        default=MainCategoryType.ART,
    )
    class SubCategoryType(models.TextChoices):
        FINE = '순수예술'
        RIDICULE = '조소/조각'
        CRAFT = '공예'
        ILLUSTRATION = '일러스트'
        INDUSTRIAL_DESIGN = '산업디자인'
        CONSTRUCT = '건축'
        TRADITIONAL = '전통예술'
        CLASSIC = '클래식'
        PIANO = '피아노'
        BAND = '밴드'
        COMPOSITION = '작사/작곡'



    sub_category = models.CharField(
        max_length=15,
        choices=SubCategoryType.choices,
        default=SubCategoryType.FINE,
    )

class FollowRelation(models.Model):
    follower = models.ForeignKey('accounts.User', related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey('accounts.User', related_name='followed_user', on_delete=models.CASCADE)