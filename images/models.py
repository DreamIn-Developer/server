from django.db import models

class Image(models.Model):
    image = models.URLField()

    def __str__(self):
        self.image