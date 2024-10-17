from django.urls import path, include

#documantions
from api.spectacular.urls import urlpatterns as doc_urls

#apps_url
from product.urls import urlpatterns as product_urls 

app_name = 'api'

urlpatterns = []


urlpatterns += doc_urls

#apps_url
urlpatterns += product_urls 

