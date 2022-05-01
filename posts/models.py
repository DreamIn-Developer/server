from django.db import models

class Post(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField()
    images = models.ManyToManyField('images.Image')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def comment_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BookMark(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='stored_post')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

class TeamPost(models.Model):
    team = models.ForeignKey('teams.TeamProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField()
    images = models.ManyToManyField('images.Image')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.teamcomment_set.count()

class TeamComment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    post = models.ForeignKey('posts.TeamPost', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description