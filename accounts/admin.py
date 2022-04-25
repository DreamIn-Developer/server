from django.contrib import admin
from accounts.models import User, FollowRelation, MainCategory, SubCategory

admin.site.register([User, FollowRelation, MainCategory, SubCategory])
