from django.contrib import admin
from .models import Users, ProjectUserMapping
from project.models import Project
# Register your models here.

admin.site.register(Users)
admin.site.register(Project)
admin.site.register(ProjectUserMapping)
