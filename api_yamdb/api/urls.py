from django.urls import include, path
from rest_framework import routers

from reviews.views import MakeJwtTokenAPIView, UsersViewSet, SignUpAPIView

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/users', UsersViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/token/', MakeJwtTokenAPIView.as_view()),
    path('v1/auth/signup/', SignUpAPIView.as_view()),
]
