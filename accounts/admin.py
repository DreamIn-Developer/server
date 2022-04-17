from django.contrib import admin
from accounts.models import User, FollowRelation

admin.site.register([User, FollowRelation])
