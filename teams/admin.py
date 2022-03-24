from django.contrib import admin

from teams.models import Member, TeamProfile

admin.site.register([TeamProfile, Member])