from django.db import models

class Image(models.Model):
    image = models.URLField(max_length=511)