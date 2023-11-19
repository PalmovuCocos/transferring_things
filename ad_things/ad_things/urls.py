from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from bulletin_board.views import RegisterAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bulletin_board.urls')),
    # создание
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # обновление
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # проверка
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/register', RegisterAPI.as_view())
]
