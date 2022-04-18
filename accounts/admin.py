from django.contrib import admin
from accounts.models import User, FollowRelation, Category

admin.site.register([User, FollowRelation, Category])
