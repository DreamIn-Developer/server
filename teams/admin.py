from django.contrib import admin

from teams.models import Member, TeamProfile, TeamFollowRelation

admin.site.register([TeamProfile, Member, TeamFollowRelation])