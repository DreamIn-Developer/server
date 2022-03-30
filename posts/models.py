from django.db import models
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='post', blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class PostType(models.TextChoices):
        TEAM = 'Te', _('Team')
        INDIVIDUAL = 'In', _('Individual')

    post_type = models.CharField(
        max_length=2,
        choices=PostType.choices,
        default=PostType.INDIVIDUAL,
    )

    @property
    def comment_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)