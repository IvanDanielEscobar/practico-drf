from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .routers import router

urlpatterns = [
    # Endpoints de Autenticación SimpleJWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Enrutamiento de ViewSets desde routers.py
    path('', include(router.urls)),
]
