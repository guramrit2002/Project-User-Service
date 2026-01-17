from django.contrib import admin
from django.urls import path, include
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('project/', include('project.urls')),
    path('project-owner/',include('project_accounts.urls'))
]

