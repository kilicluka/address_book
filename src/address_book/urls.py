from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from address import views

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
