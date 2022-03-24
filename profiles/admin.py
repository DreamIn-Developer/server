from django.contrib import admin

from profiles.models import Member, Teamprofile, Profile

admin.site.register([Profile, Teamprofile, Member])