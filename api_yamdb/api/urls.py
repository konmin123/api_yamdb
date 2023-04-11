from django.urls import include, path
from rest_framework import routers

from .views import (MakeJwtTokenAPIView, UsersForAdminViewSet, SignUpAPIView,
                    PersonalUserViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/users', UsersForAdminViewSet, basename='')
router_v1.register('v1/users/me', PersonalUserViewSet, basename='')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/token/', MakeJwtTokenAPIView.as_view()),
    path('v1/auth/signup/', SignUpAPIView.as_view()),
]
