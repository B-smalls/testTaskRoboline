from django.urls import path, include

#documantions
from api.spectacular.urls import urlpatterns as doc_urls

#apps_url


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'))
]


