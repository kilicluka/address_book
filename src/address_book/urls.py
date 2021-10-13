from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView


from address import views

router = routers.DefaultRouter()
router.register(r'user-addresses', views.UserAddressViewSet, basename='user-addresses')

schema_view = get_schema_view(
    openapi.Info(
      title='Address Book API',
      default_version='v1',
      description='Api for managing your addresses',
      terms_of_service='https://www.google.com/policies/terms/',
      license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
