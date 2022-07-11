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

    @property
    def like_count(self):
        return self.postlike_set.count()

    @property
    def scrap_count(self):
        return self.stored_post.count()

class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BookMark(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='stored_post')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='mark_user')

    @property
    def id(self):
        return self.post.id

    @property
    def image_list(self):
        return self.post.images.values('image')

    @property
    def title(self):
        return self.post.title

    @property
    def created_at(self):
        return self.post.created_at

    @property
    def updated_at(self):
        return self.post.updated_at

    @property
    def nickname(self):
        return self.post.author.nickname

    @property
    def images(self):
        return self.post.images.image

class TeamBookMark(models.Model):
    post = models.ForeignKey('posts.TeamPost', on_delete=models.CASCADE)
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

    @property
    def like_count(self):
        return self.teampostlike_set.count()

    @property
    def scrap_count(self):
        return self.teambookmark_set.count()

class TeamComment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField()
    post = models.ForeignKey('posts.TeamPost', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class PostLike(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

class TeamPostLike(models.Model):
    team_post = models.ForeignKey('posts.TeamPost', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)