from django.contrib import admin
from django.urls import path, include

from movies.urls import urlpatterns as movies_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include(movies_urlpatterns)),
]
