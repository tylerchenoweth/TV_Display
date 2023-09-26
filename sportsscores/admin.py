from django.contrib import admin
from .models import League, Team, TeamLeague

# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(TeamLeague)